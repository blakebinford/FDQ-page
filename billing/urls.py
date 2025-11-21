# billing/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('create-checkout/<int:org_id>/', views.create_checkout_session, name='billing-create-checkout'),
    path('webhook/', views.stripe_webhook, name='billing-stripe-webhook'),
]
