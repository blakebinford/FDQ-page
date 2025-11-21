# courses/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('quiz/<int:quiz_id>/submit/', views.submit_quiz, name='quiz-submit'),
    path('cert/verify/<uuid:cert_id>/', views.cert_verify, name='cert-verify'),
]
