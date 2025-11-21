# courses/utils.py
from io import BytesIO
from django.core.files.base import ContentFile
from reportlab.lib.pagesizes import landscape, A4
from reportlab.pdfgen import canvas
import qrcode
from django.conf import settings

def generate_certificate_pdf(user, course, certificate):
    """
    Generates a PDF for `certificate` (Certificate instance). Returns a ContentFile ready for saving.
    """
    buffer = BytesIO()
    width, height = landscape(A4)
    c = canvas.Canvas(buffer, pagesize=(width, height))

    # Header
    c.setFont("Helvetica-Bold", 36)
    c.drawCentredString(width/2, height - 120, "Field Driven Quality")
    c.setFont("Helvetica", 24)
    c.drawCentredString(width/2, height - 180, "Certificate of Completion")
    c.setFont("Helvetica", 18)
    c.drawCentredString(width/2, height - 240, "This certifies that")

    # Recipient
    c.setFont("Helvetica-Bold", 28)
    c.drawCentredString(width/2, height - 300, f"{user.first_name} {user.last_name}")

    # Course
    c.setFont("Helvetica", 16)
    c.drawCentredString(width/2, height - 340, f"has successfully completed {course.title}")

    # Issued
    c.setFont("Helvetica", 12)
    c.drawString(40, 40, f"Issued: {certificate.issued_at.strftime('%Y-%m-%d')}")
    c.drawString(40, 25, f"Certificate ID: {certificate.cert_id}")

    # QR: verification URL
    verification_url = f"{settings.SITE_URL.rstrip('/')}/cert/verify/{certificate.cert_id}/"
    qr = qrcode.make(verification_url)
    qr_buffer = BytesIO()
    qr.save(qr_buffer, format='PNG')
    qr_buffer.seek(0)
    c.drawInlineImage(qr_buffer, width - 220, 40, 180, 180)

    c.showPage()
    c.save()
    buffer.seek(0)
    return ContentFile(buffer.read(), name=f"certificate-{user.id}-{course.slug}.pdf")
