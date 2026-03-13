from django.urls import path
from . import views

app_name = 'lms'

urlpatterns = [
    path('certifications/', views.tier_list, name='tier_list'),
    path('certifications/<slug:slug>/checkout/', views.create_checkout_session, name='checkout'),
    path('checkout/success/', views.checkout_success, name='checkout_success'),
    path('checkout/cancel/', views.checkout_cancel, name='checkout_cancel'),
    path('webhooks/stripe/', views.stripe_webhook, name='stripe_webhook'),
    path('dashboard/', views.dashboard, name='dashboard'),
]
