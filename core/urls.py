from django.urls import path
from .views import home, about, contact_view, contact_thanks

urlpatterns = [
    path('', home, name='home'),
    path('about/', about, name='about'),
    path('contact/', contact_view, name='contact'),
    path('contact/thanks/', contact_thanks, name='contact_thanks'),
]

