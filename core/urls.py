from django.urls import path
from .insights import beacon, funnel, test_alert, visitors
from .reports import forms as forms_report, pages as pages_report, visitor as visitor_timeline
from .views import (
    home, about, contact_view, contact_thanks, privacy, not_me,
    waitlist, waitlist_thanks, waitlist_trade, waitlist_resend, lesson_link, unsubscribe,
    field_sheet, field_sheet_preview,
    lesson_1_video, lesson_1_captions, lesson_1_poster, lesson_1_player_poster,
    favicon, robots_txt, sitemap_xml,
)

urlpatterns = [
    path('', home, name='home'),
    path('about/', about, name='about'),
    path('contact/', contact_view, name='contact'),
    path('contact/thanks/', contact_thanks, name='contact_thanks'),
    path('privacy/', privacy, name='privacy'),
    path('not-me/', not_me, name='not_me'),
    path('tier-1/', waitlist, name='waitlist'),
    path('tier-1/thanks/', waitlist_thanks, name='waitlist_thanks'),
    path('tier-1/thanks/trade/', waitlist_trade, name='waitlist_trade'),
    path('tier-1/resend/', waitlist_resend, name='waitlist_resend'),
    path('tier-1/lesson/<str:token>/', lesson_link, name='lesson_link'),
    path('tier-1/leave/<str:token>/', unsubscribe, name='unsubscribe'),
    path('tier-1/weld-field-sheet.pdf', field_sheet, name='field_sheet'),
    path('tier-1/weld-field-sheet.jpg', field_sheet_preview, name='field_sheet_preview'),
    path('tier-1/lesson-1.mp4', lesson_1_video, name='lesson_1_video'),
    path('tier-1/lesson-1.vtt', lesson_1_captions, name='lesson_1_captions'),
    path('tier-1/lesson-1.jpg', lesson_1_poster, name='lesson_1_poster'),
    path('tier-1/lesson-1-player.jpg', lesson_1_player_poster, name='lesson_1_player_poster'),
    path('e/', beacon, name='beacon'),
    path('staff/funnel/', funnel, name='staff_funnel'),
    path('staff/visitors/', visitors, name='staff_visitors'),
    path('staff/visitors/<str:visitor_id>/', visitor_timeline, name='staff_visitor'),
    path('staff/pages/', pages_report, name='staff_pages'),
    path('staff/forms/', forms_report, name='staff_forms'),
    path('staff/test-alert/', test_alert, name='staff_test_alert'),
    path('favicon.ico', favicon, name='favicon'),
    path('robots.txt', robots_txt, name='robots'),
    path('sitemap.xml', sitemap_xml, name='sitemap'),
]
