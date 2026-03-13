from django.contrib.auth.decorators import login_required
from django.shortcuts import render


@login_required
def apply_view(request):
    """Stub — application form will be built in a future prompt."""
    return render(request, 'applications/apply.html')


@login_required
def application_status_view(request):
    """Stub — application status page will be built in a future prompt."""
    return render(request, 'applications/status.html')
