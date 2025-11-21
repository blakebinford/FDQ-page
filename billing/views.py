# billing/views.py
import stripe
from django.conf import settings
from django.shortcuts import get_object_or_404
from django.http import JsonResponse, HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.utils import timezone
from .models import Organization, OrganizationSubscription

stripe.api_key = settings.STRIPE_SECRET_KEY

def create_checkout_session(request, org_id, plan="small"):
    """Create a Stripe Checkout session for an organization subscription (returns JSON sessionId)."""
    org = get_object_or_404(Organization, id=org_id)
    domain = settings.SITE_URL.rstrip('/')
    # Map plan -> price id (set in env)
    price_id = settings.STRIPE_PRICE_ID_SMALL
    checkout = stripe.checkout.Session.create(
        customer_email=request.user.email if request.user.is_authenticated else None,
        success_url=f"{domain}/billing/success?session_id={{CHECKOUT_SESSION_ID}}",
        cancel_url=f"{domain}/billing/cancel",
        payment_method_types=["card"],
        mode="subscription",
        line_items=[{"price": price_id, "quantity": 1}],
        metadata={"organization_id": str(org.id)}
    )
    return JsonResponse({"sessionId": checkout["id"]})

@csrf_exempt
def stripe_webhook(request):
    payload = request.body
    sig_header = request.META.get("HTTP_STRIPE_SIGNATURE", "")
    endpoint_secret = settings.STRIPE_WEBHOOK_SECRET
    try:
        event = stripe.Webhook.construct_event(payload, sig_header, endpoint_secret)
    except Exception as e:
        return HttpResponse(status=400)

    # Handle subscription created event
    if event["type"] == "customer.subscription.created" or event["type"] == "invoice.payment_succeeded":
        data = event["data"]["object"]
        # When subscription.created, try to read metadata or invoice lines
        metadata_org_id = None
        if "metadata" in data and data["metadata"].get("organization_id"):
            metadata_org_id = data["metadata"].get("organization_id")
        # If we have metadata, associate subscription
        if metadata_org_id:
            org = Organization.objects.filter(id=metadata_org_id).first()
            if org:
                # store subscription record if not exists
                stripe_sub_id = data.get("id") or data.get("subscription")
                if stripe_sub_id:
                    OrganizationSubscription.objects.get_or_create(
                        organization=org,
                        stripe_subscription_id=stripe_sub_id,
                        defaults={
                            "plan": data.get("plan", {}).get("id") if data.get("plan") else "",
                            "status": data.get("status", "active"),
                            "current_period_end": timezone.datetime.fromtimestamp(data.get("current_period_end")) if data.get("current_period_end") else None
                        }
                    )
    if event["type"] == "checkout.session.completed":
        # optional: record checkout completed
        pass
    return HttpResponse(status=200)
