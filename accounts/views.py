from django.contrib.auth import authenticate, login, logout, get_user_model
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import (
    PasswordResetConfirmView,
    PasswordResetView,
    PasswordResetDoneView,
    PasswordResetCompleteView,
)
from django.shortcuts import redirect, render
from django.urls import reverse_lazy

from .models import CERTIFICATION_CHOICES, WorkHistory

User = get_user_model()


def login_view(request):
    if request.user.is_authenticated:
        return redirect('lms:dashboard')
    if request.method == 'POST':
        email = request.POST.get('email', '').strip().lower()
        password = request.POST.get('password')
        user = authenticate(request, username=email, password=password)
        if user:
            login(request, user)
            return redirect(request.GET.get('next') or 'lms:dashboard')
        return render(request, 'accounts/login.html', {'error': 'Invalid email or password.'})
    return render(request, 'accounts/login.html')


def logout_view(request):
    if request.method == 'POST':
        logout(request)
    return redirect('accounts:login')


def register_view(request):
    if request.user.is_authenticated:
        return redirect('lms:dashboard')
    if request.method == 'POST':
        first_name = request.POST.get('first_name', '').strip()
        last_name = request.POST.get('last_name', '').strip()
        email = request.POST.get('email', '').strip().lower()
        password = request.POST.get('password')
        password2 = request.POST.get('password2')

        errors = []
        if not first_name:
            errors.append('First name is required.')
        if not last_name:
            errors.append('Last name is required.')
        if not email:
            errors.append('Email is required.')
        if not password:
            errors.append('Password is required.')
        elif len(password) < 8:
            errors.append('Password must be at least 8 characters.')
        if password != password2:
            errors.append('Passwords do not match.')
        if not errors and User.objects.filter(email=email).exists():
            errors.append('An account with that email already exists.')

        if errors:
            return render(request, 'accounts/register.html', {
                'errors': errors,
                'first_name': first_name,
                'last_name': last_name,
                'email': email,
            })

        user = User.objects.create_user(
            email=email,
            password=password,
            first_name=first_name,
            last_name=last_name,
        )
        login(request, user)
        return redirect('applications:apply')
    return render(request, 'accounts/register.html')


class PasswordSetView(PasswordResetConfirmView):
    """
    Used for new users setting their password after purchase.
    On success, sets email_verified = True.
    If profile is incomplete, redirects to profile_edit instead of password_set_done.
    """
    template_name = 'accounts/password_set.html'
    post_reset_login = True

    def form_valid(self, form):
        response = super().form_valid(form)
        self.user.email_verified = True
        self.user.save(update_fields=['email_verified'])
        return response

    def get_success_url(self):
        if not self.user.profile_complete:
            return reverse_lazy('accounts:profile_edit')
        return reverse_lazy('accounts:password_set_done')


def password_set_done(request):
    return render(request, 'accounts/password_set_done.html')


class CustomPasswordResetView(PasswordResetView):
    template_name = 'accounts/password_reset.html'
    email_template_name = 'emails/password_reset_email.txt'
    subject_template_name = 'emails/password_reset_subject.txt'
    success_url = reverse_lazy('accounts:password_reset_done')


class CustomPasswordResetDoneView(PasswordResetDoneView):
    template_name = 'accounts/password_reset_done.html'


class CustomPasswordResetConfirmView(PasswordResetConfirmView):
    template_name = 'accounts/password_reset_confirm.html'
    success_url = reverse_lazy('accounts:password_reset_complete')


class CustomPasswordResetCompleteView(PasswordResetCompleteView):
    template_name = 'accounts/password_reset_complete.html'


@login_required
def profile_view(request):
    try:
        application = request.user.application
    except Exception:
        application = None
    return render(request, 'accounts/profile_view.html', {'application': application})


@login_required
def profile_edit_view(request):
    user = request.user

    if request.method == 'POST':
        action = request.POST.get('action', '')

        if action == 'add_work_history':
            WorkHistory.objects.create(
                user=user,
                company_name=request.POST.get('wh_company', '').strip(),
                position_name=request.POST.get('wh_position', '').strip(),
                industry=request.POST.get('wh_industry', ''),
                start_date=request.POST.get('wh_start_date'),
                end_date=request.POST.get('wh_end_date') or None,
                is_current=request.POST.get('wh_is_current') == 'on',
                contact_name=request.POST.get('wh_contact_name', '').strip(),
                contact_position=request.POST.get('wh_contact_position', '').strip(),
                contact_phone=request.POST.get('wh_contact_phone', '').strip(),
                contact_email=request.POST.get('wh_contact_email', '').strip(),
            )
            return redirect('accounts:profile_edit')

        if action == 'delete_work_history':
            wh_id = request.POST.get('wh_id')
            WorkHistory.objects.filter(id=wh_id, user=user).delete()
            return redirect('accounts:profile_edit')

        # Default: save profile fields
        user.first_name = request.POST.get('first_name', '').strip()
        user.last_name = request.POST.get('last_name', '').strip()
        user.company_name = request.POST.get('company_name', '').strip()
        user.profession = request.POST.get('profession', '')
        user.industry = request.POST.get('industry', '')
        user.state = request.POST.get('state', '')
        years = request.POST.get('years_experience', '')
        user.years_experience = int(years) if years else None
        user.project_types = ','.join(request.POST.getlist('project_types'))
        user.certifications_held = ','.join(request.POST.getlist('certifications_held'))
        user.linkedin_url = request.POST.get('linkedin_url', '').strip()
        user.profile_complete = True
        user.save()
        return redirect('accounts:profile')

    return render(request, 'accounts/profile_edit.html', {
        'profession_choices': User.PROFESSION_CHOICES,
        'industry_choices': User.INDUSTRY_CHOICES,
        'project_type_choices': User.PROJECT_TYPE_CHOICES,
        'certification_choices': CERTIFICATION_CHOICES,
        'work_history': user.work_history.all(),
    })
