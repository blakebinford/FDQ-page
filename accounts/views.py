from django.contrib.auth import logout
from django.contrib.auth.views import LoginView, PasswordResetConfirmView
from django.shortcuts import redirect, render
from django.urls import reverse_lazy
from django.views.decorators.http import require_http_methods

from accounts.forms import CustomLoginForm


@require_http_methods(["POST", "GET"])
def custom_logout_view(request):
    logout(request)
    return redirect('home')


class CustomLoginView(LoginView):
    authentication_form = CustomLoginForm
    template_name = 'accounts/login.html'


class PasswordSetView(PasswordResetConfirmView):
    """
    Used for new users setting their password after purchase.
    On success, sets email_verified = True.
    Template: accounts/password_set.html
    """
    template_name = 'accounts/password_set.html'
    success_url = reverse_lazy('accounts:password_set_done')
    post_reset_login = True

    def form_valid(self, form):
        response = super().form_valid(form)
        # Mark email as verified since they clicked the link from their inbox
        user = form.save()
        user.email_verified = True
        user.save(update_fields=['email_verified'])
        return response


def password_set_done(request):
    return render(request, 'accounts/password_set_done.html')
