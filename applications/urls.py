from django.urls import path
from . import views

app_name = 'applications'

urlpatterns = [
    path('', views.apply_view, name='apply'),
    path('status/', views.application_status_view, name='status'),
]
