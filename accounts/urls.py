from django.urls import path
from django.contrib.auth.views import LoginView, LogoutView
from . import views
from .views import custom_logout_view

app_name = 'accounts'

urlpatterns = [
    path('login/', LoginView.as_view(template_name='accounts/login.html'), name='login'),
    path('logout/', custom_logout_view, name='logout'),
    path(
        'set-password/<uidb64>/<token>/',
        views.PasswordSetView.as_view(),
        name='password_set'
    ),
    path('set-password/done/', views.password_set_done, name='password_set_done'),
]
