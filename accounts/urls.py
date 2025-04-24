from django.urls import path
from django.contrib.auth.views import LoginView, LogoutView
from . import views
from .views import custom_logout_view

urlpatterns = [
    path('login/', LoginView.as_view(template_name='accounts/login.html'), name='login'),
    path('logout/', custom_logout_view, name='logout'),
]
