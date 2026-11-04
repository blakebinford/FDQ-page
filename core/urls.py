from django.urls import path
from .views import (
    home, about, contact_view, contact_thanks,
    waitlist, waitlist_thanks, field_card, field_card_preview,
    lesson_1_video, lesson_1_captions, lesson_1_poster, lesson_1_player_poster,
)

urlpatterns = [
    path('', home, name='home'),
    path('about/', about, name='about'),
    path('contact/', contact_view, name='contact'),
    path('contact/thanks/', contact_thanks, name='contact_thanks'),
    path('tier-1/', waitlist, name='waitlist'),
    path('tier-1/thanks/', waitlist_thanks, name='waitlist_thanks'),
    path('tier-1/weld-map-field-card.pdf', field_card, name='field_card'),
    path('tier-1/weld-map-field-card.png', field_card_preview, name='field_card_preview'),
    path('tier-1/lesson-1.mp4', lesson_1_video, name='lesson_1_video'),
    path('tier-1/lesson-1.vtt', lesson_1_captions, name='lesson_1_captions'),
    path('tier-1/lesson-1.jpg', lesson_1_poster, name='lesson_1_poster'),
    path('tier-1/lesson-1-player.jpg', lesson_1_player_poster, name='lesson_1_player_poster'),
]

