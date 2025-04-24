from django.contrib.auth import logout
from django.contrib.auth.views import LoginView
from django.shortcuts import redirect
from django.views.decorators.http import require_http_methods

from accounts.forms import CustomLoginForm


@require_http_methods(["POST", "GET"])
def custom_logout_view(request):
    logout(request)
    return redirect('home')  # or wherever you'd like

class CustomLoginView(LoginView):
    authentication_form = CustomLoginForm
    template_name = 'accounts/login.html'
