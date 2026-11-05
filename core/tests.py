from django.test import TestCase
from django.urls import reverse

from .models import WaitlistSignup
from .views import LESSON_1_VIDEO


class WaitlistTests(TestCase):
    def post(self, **fields):
        data = {'email': 'hand@example.com', 'trade': 'welder', 'website': ''}
        data.update(fields)
        return self.client.post(reverse('waitlist'), data)

    def test_page_carries_utm_tags_and_referrer_into_the_form(self):
        response = self.client.get(
            reverse('waitlist') + '?utm_source=facebook&utm_campaign=comment-123',
            HTTP_REFERER='https://l.facebook.com/l.php?u=x',
        )
        self.assertContains(response, 'name="utm_source" value="facebook"')
        self.assertContains(response, 'name="utm_campaign" value="comment-123"')
        self.assertContains(response, 'name="referrer_host" value="l.facebook.com"')

    def test_own_site_is_not_recorded_as_referrer(self):
        response = self.client.get(reverse('waitlist'), HTTP_REFERER='http://testserver/about/')
        self.assertContains(response, 'name="referrer_host" value=""')

    def test_signup_saves_email_trade_and_source(self):
        response = self.post(email=' Hand@Example.com ', utm_source='facebook', utm_campaign='comment-123',
                             referrer_host='l.facebook.com')
        self.assertRedirects(response, reverse('waitlist_thanks'))
        signup = WaitlistSignup.objects.get()
        self.assertEqual(signup.email, 'hand@example.com')
        self.assertEqual(signup.trade, 'welder')
        self.assertEqual(signup.utm_campaign, 'comment-123')
        self.assertEqual(signup.referrer_host, 'l.facebook.com')

    def test_repeat_signup_keeps_first_source(self):
        self.post(utm_campaign='first')
        response = self.post(email='HAND@example.com', utm_campaign='second')
        self.assertRedirects(response, reverse('waitlist_thanks'))
        self.assertEqual(WaitlistSignup.objects.get().utm_campaign, 'first')

    def test_bad_email_shows_the_form_again(self):
        response = self.post(email='not-an-email')
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Enter an email address that can get mail.')
        self.assertFalse(WaitlistSignup.objects.exists())

    def test_honeypot_saves_nothing(self):
        response = self.post(website='http://spam.example')
        self.assertRedirects(response, reverse('waitlist_thanks'), fetch_redirect_response=False)
        self.assertFalse(WaitlistSignup.objects.exists())
        self.assertRedirects(self.client.get(reverse('waitlist_thanks')), reverse('waitlist') + '#sign-up')

    def test_field_sheet_files_are_served(self):
        pdf = self.client.get(reverse('field_sheet'))
        self.assertEqual(pdf['Content-Type'], 'application/pdf')
        self.assertTrue(b''.join(pdf.streaming_content).startswith(b'%PDF'))
        jpg = self.client.get(reverse('field_sheet_preview'))
        self.assertEqual(jpg['Content-Type'], 'image/jpeg')

    def test_thanks_page_needs_a_signup(self):
        response = self.client.get(reverse('waitlist_thanks'))
        self.assertRedirects(response, reverse('waitlist') + '#sign-up')

    def test_thanks_page_plays_lesson_1_and_links_the_field_sheet(self):
        self.post()
        response = self.client.get(reverse('waitlist_thanks'))
        self.assertContains(response, reverse('lesson_1_video'))
        self.assertContains(response, reverse('lesson_1_captions'))
        self.assertContains(response, reverse('field_sheet'))

    def test_lesson_1_video_is_served_whole(self):
        response = self.client.get(reverse('lesson_1_video'))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response['Content-Type'], 'video/mp4')
        self.assertEqual(response['Accept-Ranges'], 'bytes')
        self.assertEqual(int(response['Content-Length']), LESSON_1_VIDEO.stat().st_size)

    def test_lesson_1_video_serves_byte_ranges(self):
        size = LESSON_1_VIDEO.stat().st_size
        response = self.client.get(reverse('lesson_1_video'), HTTP_RANGE='bytes=0-1')
        self.assertEqual(response.status_code, 206)
        self.assertEqual(response['Content-Range'], f'bytes 0-1/{size}')
        self.assertEqual(b''.join(response.streaming_content), LESSON_1_VIDEO.read_bytes()[:2])

        response = self.client.get(reverse('lesson_1_video'), HTTP_RANGE='bytes=-10')
        self.assertEqual(response['Content-Range'], f'bytes {size - 10}-{size - 1}/{size}')
        self.assertEqual(len(b''.join(response.streaming_content)), 10)

        response = self.client.get(reverse('lesson_1_video'), HTTP_RANGE=f'bytes={size}-')
        self.assertEqual(response.status_code, 416)

    def test_lesson_1_captions_and_poster_are_served(self):
        captions = self.client.get(reverse('lesson_1_captions'))
        self.assertTrue(captions['Content-Type'].startswith('text/vtt'))
        self.assertTrue(b''.join(captions.streaming_content).startswith(b'WEBVTT'))
        for name in ('lesson_1_poster', 'lesson_1_player_poster'):
            self.assertEqual(self.client.get(reverse(name))['Content-Type'], 'image/jpeg')
