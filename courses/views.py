from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse, HttpResponse
from django.views.decorators.http import require_POST
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings
from django.db import models
from django.utils import timezone

from .models import Quiz, QuizAttempt, Course, CourseProgress, Certificate
from .utils import generate_certificate_pdf

# Create your views here.

@require_POST
def submit_quiz(request, quiz_id):
    """POST endpoint: selected=<choice>. Records an attempt and returns JSON {correct: bool}."""
    if not request.user.is_authenticated:
        return JsonResponse({"error": "authentication_required"}, status=403)
    quiz = get_object_or_404(Quiz, id=quiz_id)
    selected = request.POST.get("selected")
    correct = (selected == quiz.correct_answer)
    attempt = QuizAttempt.objects.create(user=request.user, quiz=quiz, selected_answer=selected or "", correct=correct)
    # After recording an attempt, check if user is eligible for cert for the parent course
    # Quick heuristic: find the course via module -> course
    course = quiz.module.course
    issue_certificate_if_eligible(request.user, course)
    return JsonResponse({"correct": correct})

def user_completed_course(user, course):
    # All lessons watched?
    total_lessons = course.modules.all().aggregate(total=models.Count('lessons'))['total'] or 0
    watched = CourseProgress.objects.filter(user=user, lesson__module__course=course, watched=True).count()
    if total_lessons and watched < total_lessons:
        return False
    # Ensure all quizzes for the course have at least one correct attempt
    quiz_ids = []
    for module in course.modules.all():
        quiz_ids += list(module.quizzes.all().values_list('id', flat=True))
    if quiz_ids:
        # For each quiz, ensure a correct attempt exists
        for qid in quiz_ids:
            if not QuizAttempt.objects.filter(user=user, quiz_id=qid, correct=True).exists():
                return False
    return True

def issue_certificate_if_eligible(user, course):
    if Certificate.objects.filter(user=user, course=course).exists():
        return None
    if user_completed_course(user, course):
        cert = Certificate.objects.create(user=user, course=course)
        pdf = generate_certificate_pdf(user, course, cert)
        cert.pdf.save(pdf.name, pdf)
        cert.save()
        # mark user as certified at that FDQ level optionally
        user.is_certified = True
        user.certified_at = cert.issued_at.date()
        # Optionally set fdq_level here if appropriate
        user.save(update_fields=["is_certified", "certified_at"])
        return cert
    return None

def cert_verify(request, cert_id):
    """Public endpoint to verify certificate by UUID (JSON)."""
    cert = get_object_or_404(Certificate, cert_id=cert_id)
    data = {
        "cert_id": str(cert.cert_id),
        "user": {"first_name": cert.user.first_name, "last_name": cert.user.last_name, "email": cert.user.email},
        "course": {"title": cert.course.title, "slug": cert.course.slug},
        "issued_at": cert.issued_at.isoformat(),
        "pdf_url": cert.pdf.url if cert.pdf else None,
    }
    return JsonResponse(data)
