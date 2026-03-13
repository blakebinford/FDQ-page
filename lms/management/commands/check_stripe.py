import stripe
from django.conf import settings
from django.core.management.base import BaseCommand

from lms.models import Tier


class Command(BaseCommand):
    help = 'Verify Stripe configuration is correct'

    def handle(self, *args, **options):
        stripe.api_key = settings.STRIPE_SECRET_KEY

        # Check API key works
        try:
            account = stripe.Account.retrieve()
            self.stdout.write(self.style.SUCCESS(
                f'Stripe API key valid. Account: {account.id}'
            ))
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'Stripe API key invalid: {e}'))
            return

        # Check webhook secret format
        webhook_secret = settings.STRIPE_WEBHOOK_SECRET
        if webhook_secret.startswith('whsec_'):
            self.stdout.write(self.style.SUCCESS(
                f'Webhook secret present: {webhook_secret[:14]}...'
            ))
        else:
            self.stdout.write(self.style.ERROR(
                'Webhook secret missing or malformed. '
                'Run: stripe listen --forward-to localhost:8000/certifications/webhooks/stripe/ '
                'and copy the whsec_ value to STRIPE_WEBHOOK_SECRET in .env'
            ))

        # Check tiers have real price IDs
        for tier in Tier.objects.all():
            if tier.stripe_price_id.startswith('price_'):
                self.stdout.write(self.style.SUCCESS(
                    f'Tier "{tier.name}": price_id OK ({tier.stripe_price_id})'
                ))
            else:
                self.stdout.write(self.style.ERROR(
                    f'Tier "{tier.name}": invalid price_id "{tier.stripe_price_id}"'
                ))
