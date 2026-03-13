from django.urls import path
from . import views

app_name = 'lms'

urlpatterns = [
    path('', views.tier_list, name='tier_list'),
    path('<slug:tier_slug>/learn/', views.learn, name='learn'),
    path('<slug:tier_slug>/lessons/<int:lesson_order>/', views.lesson_view, name='lesson'),
    path('<slug:tier_slug>/quiz/', views.quiz_view, name='quiz'),
    path('<slug:tier_slug>/quiz/results/', views.quiz_results, name='quiz_results'),
    path('<slug:tier_slug>/certificate/', views.certificate_view, name='certificate'),
    path('<slug:tier_slug>/certificate/pdf/', views.certificate_pdf, name='certificate_pdf'),
    path('verify/<str:certificate_number>/', views.certificate_verify, name='certificate_verify'),
    path('checkout/<slug:tier_slug>/', views.create_checkout_session, name='checkout'),
    path('checkout/success/', views.checkout_success, name='checkout_success'),
    path('checkout/cancel/', views.checkout_cancel, name='checkout_cancel'),
    path('webhooks/stripe/', views.stripe_webhook, name='stripe_webhook'),
    path('dashboard/', views.dashboard, name='dashboard'),
]
