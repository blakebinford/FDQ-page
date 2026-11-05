import re
from unittest import mock
from urllib.parse import urlparse

from django.contrib.auth import get_user_model
from django.core import mail
from django.core.cache import cache
from django.test import Client, TestCase, override_settings
from django.urls import reverse
from django.utils import timezone

from lms.models import Certificate, Tier

from .analytics import VISITOR_COOKIE
from .models import SiteEvent, WaitlistSignup
from .views import LESSON_1_VIDEO


class TestCase(TestCase):
    """Every test starts with an empty cache, so the forms' rate limit doesn't carry over."""

    def setUp(self):
        super().setUp()
        cache.clear()


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
        self.assertRedirects(response, reverse('waitlist_thanks') + '#lesson')
        signup = WaitlistSignup.objects.get()
        self.assertEqual(signup.email, 'hand@example.com')
        self.assertEqual(signup.trade, 'welder')
        self.assertEqual(signup.utm_campaign, 'comment-123')
        self.assertEqual(signup.referrer_host, 'l.facebook.com')

    def test_repeat_signup_keeps_first_source(self):
        self.post(utm_campaign='first')
        response = self.post(email='HAND@example.com', utm_campaign='second')
        self.assertRedirects(response, reverse('waitlist_thanks') + '#lesson')
        self.assertEqual(WaitlistSignup.objects.get().utm_campaign, 'first')

    def test_bad_email_shows_the_form_again(self):
        response = self.post(email='not-an-email')
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Enter an email address that can get mail.')
        self.assertFalse(WaitlistSignup.objects.exists())

    def test_honeypot_saves_nothing(self):
        response = self.post(website='http://spam.example')
        self.assertRedirects(response, reverse('waitlist_thanks') + '#lesson', fetch_redirect_response=False)
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


class WaitlistFormTests(TestCase):
    def test_bad_email_comes_back_at_the_form_with_the_error_tied_to_the_field(self):
        response = self.client.post(reverse('waitlist'), {'email': 'bob@', 'website': ''})
        self.assertContains(response, f'action="{reverse("waitlist")}#sign-up"')
        self.assertContains(response, 'aria-invalid="true" aria-describedby="wl-email-error" autofocus')
        self.assertNotContains(response, 'id="wl-email-error" role="alert" hidden')

    def test_fresh_form_has_no_error_showing(self):
        response = self.client.get(reverse('waitlist'))
        self.assertContains(response, 'id="wl-email-error" role="alert" hidden')
        self.assertNotContains(response, 'aria-invalid="true"')

    def test_page_promises_the_email_only_when_email_is_set_up(self):
        self.assertNotContains(self.client.get(reverse('waitlist')), 'we email you the link')
        with override_settings(**EMAIL_ON):
            self.assertContains(self.client.get(reverse('waitlist')), 'we email you the link')

    @override_settings(TIER1_OPENS='Wed Nov 18')
    def test_launch_date_shows_once_it_is_set(self):
        self.assertContains(self.client.get(reverse('waitlist')), 'Opens Wed Nov 18')
        self.assertContains(self.client.get(reverse('home')), 'Opens Wed Nov 18')

    def test_launch_date_is_left_out_until_set(self):
        self.assertContains(self.client.get(reverse('waitlist')), 'Opening soon')


EMAIL_ON = {
    'WAITLIST_EMAILS_ENABLED': True,
    'WAITLIST_FROM_EMAIL': 'FDQ <lessons@fielddrivenquality.com>',
    'BUSINESS_POSTAL_ADDRESS': 'PO Box 100, Odessa, TX 79760',
    'EMAIL_BACKEND': 'django.core.mail.backends.locmem.EmailBackend',
}


@override_settings(**EMAIL_ON)
class LessonEmailTests(TestCase):
    def sign_up(self, client=None, email='hand@example.com'):
        return (client or self.client).post(reverse('waitlist'), {'email': email, 'website': ''})

    def test_signup_emails_the_lesson_link_with_an_unsubscribe(self):
        self.sign_up()
        self.assertEqual(len(mail.outbox), 1)
        message = mail.outbox[0]
        self.assertEqual(message.to, ['hand@example.com'])
        self.assertEqual(message.from_email, 'FDQ <lessons@fielddrivenquality.com>')
        self.assertIn('PO Box 100, Odessa, TX 79760', message.body)
        self.assertIn('/tier-1/lesson/', message.body)
        self.assertIn('/tier-1/leave/', message.extra_headers['List-Unsubscribe'])
        self.assertEqual(message.extra_headers['List-Unsubscribe-Post'], 'List-Unsubscribe=One-Click')
        self.assertIsNotNone(WaitlistSignup.objects.get().lesson_email_sent_at)
        self.assertContains(self.client.get(reverse('waitlist_thanks')), 'We sent the link to hand@example.com')

    def test_signing_up_again_soon_after_does_not_send_again(self):
        self.sign_up()
        self.sign_up()
        self.assertEqual(len(mail.outbox), 1)

    def test_lesson_link_opens_the_lesson_in_another_browser_and_confirms(self):
        self.sign_up()
        link = re.search(r'https?://\S+/tier-1/lesson/\S+/', mail.outbox[0].body).group(0)
        other_browser = Client()
        response = other_browser.get(urlparse(link).path, follow=True)
        self.assertContains(response, reverse('lesson_1_video'))
        self.assertIsNotNone(WaitlistSignup.objects.get().confirmed_at)

    def test_altered_lesson_link_is_not_found(self):
        self.assertEqual(self.client.get(reverse('lesson_link', args=['nope'])).status_code, 404)

    def test_unsubscribe_asks_then_takes_them_off(self):
        self.sign_up()
        path = urlparse(mail.outbox[0].extra_headers['List-Unsubscribe'].strip('<>')).path
        strict = Client(enforce_csrf_checks=True)
        self.assertContains(strict.get(path), 'Take me off the list')
        self.assertIsNone(WaitlistSignup.objects.get().unsubscribed_at)
        # Mail apps' one-click unsubscribe posts with no CSRF token.
        response = strict.post(path, 'List-Unsubscribe=One-Click', content_type='application/x-www-form-urlencoded')
        self.assertContains(response, "You're off the list.")
        self.assertIsNotNone(WaitlistSignup.objects.get().unsubscribed_at)

    def test_unsubscribed_address_gets_no_email_until_it_signs_up_again(self):
        signup = WaitlistSignup.objects.create(email='hand@example.com', unsubscribed_at=timezone.now())
        self.sign_up()
        signup.refresh_from_db()
        self.assertIsNone(signup.unsubscribed_at)
        self.assertEqual(len(mail.outbox), 1)

    def test_resend_answers_the_same_for_any_address(self):
        WaitlistSignup.objects.create(email='hand@example.com')
        for email in ('nobody@example.com', 'hand@example.com'):
            response = self.client.post(reverse('waitlist_resend'), {'email': email})
            self.assertContains(response, 'If that email is on the list')
        self.assertEqual([m.to for m in mail.outbox], [['hand@example.com']])


class NoEmailYetTests(TestCase):
    def test_nothing_is_sent_and_the_fallback_is_explained(self):
        self.client.post(reverse('waitlist'), {'email': 'hand@example.com', 'website': ''})
        self.assertEqual(len(mail.outbox), 0)
        response = self.client.get(reverse('waitlist_thanks'))
        self.assertNotContains(response, 'We sent the link')
        self.assertContains(response, 'Sign up again with the same email')

    def test_resend_page_waits_for_email(self):
        self.assertRedirects(self.client.get(reverse('waitlist_resend')), reverse('waitlist') + '#sign-up',
                             fetch_redirect_response=False)


class ThanksPageTests(TestCase):
    def setUp(self):
        self.client.post(reverse('waitlist'), {'email': 'hand@example.com', 'website': ''})

    def test_one_tap_trade_question_saves_the_answer(self):
        self.assertContains(self.client.get(reverse('waitlist_thanks')), 'One question: what do you do now?')
        response = self.client.post(reverse('waitlist_trade'), {'trade': 'helper'})
        self.assertRedirects(response, reverse('waitlist_thanks') + '#trade')
        self.assertEqual(WaitlistSignup.objects.get().trade, 'helper')
        self.assertContains(self.client.get(reverse('waitlist_thanks')), "Noted: Welder&#x27;s helper.")

    def test_unknown_trade_is_ignored(self):
        self.client.post(reverse('waitlist_trade'), {'trade': 'astronaut'})
        self.assertEqual(WaitlistSignup.objects.get().trade, '')

    def test_share_link_is_tagged(self):
        self.assertContains(self.client.get(reverse('waitlist_thanks')), 'utm_source=share')


FACEBOOK_PHONE = ('Mozilla/5.0 (iPhone; CPU iPhone OS 17_0 like Mac OS X) AppleWebKit/605.1.15 '
                  '(KHTML, like Gecko) Mobile/15E148 [FBAN/FBIOS;FBAV/440.0]')


class AnalyticsTests(TestCase):
    def test_page_view_is_recorded_with_source_device_and_in_app_browser(self):
        response = self.client.get(reverse('waitlist') + '?utm_source=facebook&utm_campaign=cm03&fbclid=abc',
                                   HTTP_USER_AGENT=FACEBOOK_PHONE)
        event = SiteEvent.objects.get(name='page_view')
        self.assertEqual((event.path, event.utm_campaign, event.device, event.in_app, event.fbclid_present),
                         ('/tier-1/', 'cm03', 'phone', 'facebook', True))
        self.assertEqual(event.visitor_id, response.cookies[VISITOR_COOKIE].value)
        self.assertTrue(response.cookies[VISITOR_COOKIE]['httponly'])

    def test_visitor_id_is_kept_across_pages(self):
        self.client.get(reverse('home'))
        self.client.get(reverse('about'))
        self.assertEqual(SiteEvent.objects.values('visitor_id').distinct().count(), 1)

    def test_bots_and_files_are_not_page_views(self):
        self.client.get(reverse('home'), HTTP_USER_AGENT='facebookexternalhit/1.1')
        self.client.get(reverse('field_sheet_preview'))
        self.assertFalse(SiteEvent.objects.filter(name='page_view').exists())

    def test_signup_and_form_errors_are_recorded(self):
        self.client.post(reverse('waitlist'), {'email': '', 'website': ''})
        self.client.post(reverse('waitlist'), {'email': 'hand@example.com', 'website': ''})
        self.client.post(reverse('waitlist'), {'email': 'hand@example.com', 'website': ''})
        self.assertEqual(SiteEvent.objects.get(name='form_error').props['code'], 'empty')
        self.assertEqual([e.props['is_new'] for e in SiteEvent.objects.filter(name='signup_success').order_by('pk')],
                         [True, False])

    def test_beacon_takes_known_events_only(self):
        ok = self.client.post(reverse('beacon'), {'name': 'cta_click', 'props': {'cta_id': 'home_hero', 'page': '/', 'path': 'x'}},
                              content_type='application/json')
        self.assertEqual(ok.status_code, 204)
        event = SiteEvent.objects.get(name='cta_click')
        self.assertEqual((event.path, event.props), ('/', {'cta_id': 'home_hero'}))
        bad = self.client.post(reverse('beacon'), {'name': 'drop_table'}, content_type='application/json')
        self.assertEqual(bad.status_code, 400)
        self.assertEqual(self.client.post(reverse('beacon'), 'x' * 3000, content_type='application/json').status_code, 413)

    def test_funnel_is_staff_only(self):
        self.assertEqual(self.client.get(reverse('staff_funnel')).status_code, 302)
        staff = get_user_model().objects.create_user(email='staff@example.com', password='pw-for-tests-only',
                                                     first_name='S', last_name='T', is_staff=True)
        self.client.force_login(staff)
        self.client.get(reverse('waitlist') + '?utm_campaign=cm03&utm_source=facebook')
        self.client.post(reverse('waitlist'), {'email': 'hand@example.com', 'website': ''})
        response = self.client.get(reverse('staff_funnel') + '?days=7')
        self.assertContains(response, 'Waitlist funnel')
        self.assertContains(response, 'cm03 (facebook)')
        self.assertContains(response, 'hand@example.com')


class SiteFilesTests(TestCase):
    def test_privacy_robots_sitemap_and_favicon(self):
        self.assertContains(self.client.get(reverse('privacy')), 'What we collect')
        robots = self.client.get(reverse('robots'))
        self.assertEqual(robots['Content-Type'], 'text/plain')
        self.assertContains(robots, 'Sitemap: http://testserver/sitemap.xml')
        sitemap = self.client.get(reverse('sitemap'))
        self.assertEqual(sitemap['Content-Type'], 'application/xml')
        self.assertContains(sitemap, '<loc>http://testserver/tier-1/</loc>')
        self.assertEqual(self.client.get('/favicon.ico')['Content-Type'], 'image/x-icon')

    def test_footer_links_privacy(self):
        self.assertContains(self.client.get(reverse('home')), f'href="{reverse("privacy")}"')


class AccountSignupTests(TestCase):
    def test_account_signup_waits_for_launch(self):
        self.assertRedirects(self.client.get(reverse('accounts:register')), reverse('waitlist') + '#sign-up',
                             fetch_redirect_response=False)
        login = self.client.get(reverse('accounts:login'))
        self.assertNotContains(login, 'Create an account')
        self.assertContains(login, "Tier 1 isn't open yet.")

    @override_settings(ACCOUNT_SIGNUP_OPEN=True)
    def test_register_form_labels_are_tied_to_their_fields(self):
        response = self.client.get(reverse('accounts:register'))
        self.assertContains(response, '<label for="reg-email">Email</label>')
        self.assertContains(response, 'id="reg-email"')


class CertificateLookupTests(TestCase):
    def setUp(self):
        user = get_user_model().objects.create_user(email='grad@example.com', password='pw-for-tests-only',
                                                    first_name='Pat', last_name='Rivera')
        tier = Tier.objects.create(name='Tier 1', slug='tier-1', description='x', price_cents=0, order=1)
        self.certificate = Certificate.objects.create(user=user, tier=tier)

    def test_id_and_last_name_find_the_certificate(self):
        response = self.client.get(reverse('lms:certificate_lookup'),
                                   {'id': str(self.certificate.certificate_id), 'last_name': ' rivera '})
        self.assertRedirects(response, reverse('lms:certificate_verify', args=[self.certificate.certificate_id]))

    def test_wrong_last_name_finds_nothing(self):
        response = self.client.get(reverse('lms:certificate_lookup'),
                                   {'id': str(self.certificate.certificate_id), 'last_name': 'Smith'})
        self.assertContains(response, 'No certificate matches that ID and last name.')

    def test_malformed_id_is_not_found_rather_than_an_error(self):
        self.assertContains(self.client.get(reverse('lms:certificate_verify', args=['abc'])), 'No certificate has this ID.')


class WaitlistSmtpTests(TestCase):
    @override_settings(**EMAIL_ON, WAITLIST_EMAIL_HOST='smtp.resend.com', WAITLIST_EMAIL_HOST_USER='resend',
                       WAITLIST_EMAIL_HOST_PASSWORD='')
    def test_own_smtp_account_waits_for_its_password(self):
        self.client.post(reverse('waitlist'), {'email': 'hand@example.com', 'website': ''})
        self.assertEqual(len(mail.outbox), 0)

    @override_settings(**EMAIL_ON)
    def test_postal_address_is_in_the_email_but_not_on_the_site(self):
        self.client.post(reverse('waitlist'), {'email': 'hand@example.com', 'website': ''})
        self.assertIn('PO Box 100', mail.outbox[0].body)
        for name in ('home', 'privacy', 'waitlist'):
            self.assertNotContains(self.client.get(reverse(name)), 'PO Box 100')


TURNSTILE_ON = {'TURNSTILE_SITE_KEY': '1x00000000000000000000AA', 'TURNSTILE_SECRET_KEY': 'test-secret'}


def cloudflare_says(**result):
    """A stand-in for urlopen that answers like Turnstile's siteverify."""
    import io
    import json as _json

    def fake_urlopen(url, data=None, timeout=None):
        fake_urlopen.sent = data
        return io.BytesIO(_json.dumps(result).encode())
    return fake_urlopen


@override_settings(**TURNSTILE_ON)
class TurnstileTests(TestCase):
    def post(self, **extra):
        return self.client.post(reverse('waitlist'), {'email': 'hand@example.com', 'website': '', **extra},
                                HTTP_X_FORWARDED_FOR='203.0.113.9, 10.0.0.1')

    def test_widget_and_script_show_when_keys_are_set(self):
        response = self.client.get(reverse('waitlist'))
        self.assertContains(response, 'challenges.cloudflare.com/turnstile/v0/api.js')
        self.assertContains(response, 'data-sitekey="1x00000000000000000000AA"')

    def test_missing_token_is_refused_with_a_message(self):
        response = self.post()
        self.assertContains(response, "We couldn&#x27;t confirm you&#x27;re a person.")
        self.assertFalse(WaitlistSignup.objects.exists())
        self.assertEqual(SiteEvent.objects.get(name='spam_blocked').props['reason'], 'turnstile')

    def test_confirmed_token_signs_up_and_sends_the_visitor_ip(self):
        fake = cloudflare_says(success=True)
        with mock.patch('core.spam.urllib.request.urlopen', fake):
            response = self.post(**{'cf-turnstile-response': 'token-from-widget'})
        self.assertRedirects(response, reverse('waitlist_thanks') + '#lesson', fetch_redirect_response=False)
        self.assertTrue(WaitlistSignup.objects.exists())
        self.assertIn(b'remoteip=203.0.113.9', fake.sent)

    def test_rejected_token_is_refused(self):
        with mock.patch('core.spam.urllib.request.urlopen', cloudflare_says(success=False, **{'error-codes': ['invalid-input-response']})):
            self.post(**{'cf-turnstile-response': 'forged'})
        self.assertFalse(WaitlistSignup.objects.exists())

    def test_our_own_bad_keys_or_an_outage_never_lock_people_out(self):
        with mock.patch('core.spam.urllib.request.urlopen', cloudflare_says(success=False, **{'error-codes': ['invalid-input-secret']})):
            self.post(**{'cf-turnstile-response': 't'}, email='one@example.com')
        with mock.patch('core.spam.urllib.request.urlopen', side_effect=OSError('down')):
            self.post(**{'cf-turnstile-response': 't'}, email='two@example.com')
        self.assertEqual(WaitlistSignup.objects.count(), 2)

    def test_contact_and_resend_forms_carry_the_widget(self):
        self.assertContains(self.client.get(reverse('contact')), 'data-action="contact"')
        with override_settings(**EMAIL_ON):
            self.assertContains(self.client.get(reverse('waitlist_resend')), 'data-action="resend"')


class BotLimitTests(TestCase):
    def test_one_connection_is_limited_to_eight_signups_an_hour(self):
        for n in range(9):
            response = self.client.post(reverse('waitlist'), {'email': f'hand{n}@example.com', 'website': ''})
        self.assertContains(response, 'Too many tries from this connection.')
        self.assertEqual(WaitlistSignup.objects.count(), 8)
        self.assertEqual(SiteEvent.objects.filter(name='spam_blocked', props__reason='rate_limit').count(), 1)

    def test_honeypot_is_counted(self):
        self.client.post(reverse('waitlist'), {'email': 'bot@example.com', 'website': 'http://spam.example'})
        self.assertEqual(SiteEvent.objects.get(name='spam_blocked').props, {'form': 'waitlist', 'reason': 'honeypot'})

    def test_contact_honeypot_sends_nothing(self):
        response = self.client.post(reverse('contact'), {'name': 'Bot', 'email': 'bot@example.com',
                                                         'message': 'buy now', 'website': 'x'})
        self.assertRedirects(response, reverse('contact_thanks'))
        self.assertEqual(len(mail.outbox), 0)

    def test_signup_remembers_the_browser_it_came_from(self):
        self.client.get(reverse('waitlist'), HTTP_USER_AGENT=FACEBOOK_PHONE)
        self.client.post(reverse('waitlist'), {'email': 'hand@example.com', 'website': ''}, HTTP_USER_AGENT=FACEBOOK_PHONE)
        signup = WaitlistSignup.objects.get()
        self.assertEqual((signup.device, signup.in_app), ('phone', 'facebook'))
        self.assertEqual(signup.visitor_id, SiteEvent.objects.filter(name='page_view').first().visitor_id)


class AdminTests(TestCase):
    def setUp(self):
        super().setUp()
        self.staff = get_user_model().objects.create_superuser(email='boss@example.com', password='pw-for-tests-only',
                                                               first_name='B', last_name='B')
        self.client.get(reverse('waitlist') + '?utm_source=facebook&utm_campaign=cm03')
        self.client.post(reverse('waitlist'), {'email': 'hand@example.com', 'website': ''})
        self.client.post(reverse('waitlist'), {'email': 'bot@example.com', 'website': 'x'})
        self.client.force_login(self.staff)

    def test_home_shows_the_waitlist_panel_in_fdq_colors(self):
        response = self.client.get(reverse('admin:index'))
        self.assertContains(response, 'Tier 1 waitlist')
        self.assertContains(response, '--header-bg: #17191b;')
        self.assertNotContains(response, 'dark_mode.css')

    def test_signup_list_has_the_summary(self):
        response = self.client.get(reverse('admin:core_waitlistsignup_changelist'))
        self.assertContains(response, 'On the list now')
        self.assertContains(response, 'Hidden field filled')
        self.assertContains(response, 'hand@example.com')

    def test_signup_page_shows_its_visits(self):
        signup = WaitlistSignup.objects.get(email='hand@example.com')
        response = self.client.get(reverse('admin:core_waitlistsignup_change', args=[signup.pk]))
        self.assertContains(response, 'class="fdq-trail"')
        self.assertContains(response, 'cm03')

    def test_events_are_read_only(self):
        response = self.client.get(reverse('admin:core_siteevent_changelist'))
        self.assertContains(response, 'page_view')
        self.assertEqual(self.client.get(reverse('admin:core_siteevent_add')).status_code, 403)

    def test_csv_export_carries_the_new_columns(self):
        response = self.client.post(reverse('admin:core_waitlistsignup_changelist'), {
            'action': 'export_csv', '_selected_action': list(WaitlistSignup.objects.values_list('pk', flat=True)),
        })
        self.assertIn(b'device,in_app,created_at,lesson_email_sent_at,confirmed_at,unsubscribed_at', response.content)


class PageTitleTests(TestCase):
    def test_titles_are_plain_text(self):
        for name in ('home', 'waitlist', 'about', 'contact', 'privacy'):
            title = re.search(r'<title>(.*?)</title>', self.client.get(reverse(name)).content.decode(), re.S).group(1)
            self.assertNotIn('{', title, name)
