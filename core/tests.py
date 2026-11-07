import io
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
from .models import InternalVisitor, SiteEvent, WaitlistSignup
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

    def test_tags_on_another_landing_page_carry_to_the_form(self):
        self.client.get(reverse('home') + '?utm_source=facebook&utm_campaign=fdq-page')
        response = self.client.get(reverse('waitlist'), HTTP_REFERER='http://testserver/')
        self.assertContains(response, 'name="utm_source" value="facebook"')
        self.assertContains(response, 'name="utm_campaign" value="fdq-page"')

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
        self.assertContains(self.client.get(reverse('waitlist_thanks')), 'We sent the link to <span data-clarity-mask="true">hand@example.com</span>')

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
        self.assertEqual(self.client.post(reverse('beacon'), 'x' * 9000, content_type='application/json').status_code, 413)

    def test_funnel_is_staff_only(self):
        self.assertEqual(self.client.get(reverse('staff_funnel')).status_code, 302)
        staff = get_user_model().objects.create_user(email='staff@example.com', password='pw-for-tests-only',
                                                     first_name='S', last_name='T', is_staff=True)
        self.client.force_login(staff)
        # A visitor on their own browser; the staff browser's visits are left out.
        visitor = Client()
        visitor.get(reverse('waitlist') + '?utm_campaign=cm03&utm_source=facebook')
        visitor.post(reverse('waitlist'), {'email': 'hand@example.com', 'website': ''})
        response = self.client.get(reverse('staff_funnel') + '?days=7')
        self.assertContains(response, 'Visitor funnel')
        # It sits inside the admin, with its header and breadcrumbs.
        self.assertContains(response, 'id="site-name"')
        self.assertContains(response, 'class="breadcrumbs"')
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


class SearchTagsTests(TestCase):
    """What search engines read: one canonical address, the social tags, and JSON-LD."""

    def ld_json(self, response):
        import json
        blocks = re.findall(r'<script type="application/ld\+json">(.*?)</script>', response.content.decode(), re.S)
        self.assertEqual(len(blocks), 1)
        return {item['@type']: item for item in json.loads(blocks[0])['@graph']}

    def test_canonical_drops_the_query_string(self):
        response = self.client.get(reverse('waitlist') + '?utm_source=facebook&utm_campaign=x')
        self.assertContains(response, '<link rel="canonical" href="http://testserver/tier-1/" />')
        self.assertContains(response, '<meta property="og:url" content="http://testserver/tier-1/" />')

    @override_settings(CANONICAL_ORIGIN='https://www.fielddrivenquality.com')
    def test_production_host_everywhere(self):
        response = self.client.get(reverse('home'))
        self.assertContains(response, '<link rel="canonical" href="https://www.fielddrivenquality.com/" />')
        self.assertContains(response, 'content="https://www.fielddrivenquality.com/tier-1/lesson-1.jpg"')
        self.assertContains(self.client.get(reverse('sitemap')), '<loc>https://www.fielddrivenquality.com/tier-1/</loc>')
        self.assertContains(self.client.get(reverse('robots')), 'Sitemap: https://www.fielddrivenquality.com/sitemap.xml')

    def test_one_og_image_and_a_description_on_public_pages(self):
        for name in ('home', 'waitlist', 'about', 'contact', 'lms:tier_list', 'blog_list'):
            html = self.client.get(reverse(name)).content.decode()
            self.assertEqual(html.count('property="og:image"'), 1, name)
            self.assertEqual(html.count('name="description"'), 1, name)

    @override_settings(GOOGLE_SITE_VERIFICATION='abc123')
    def test_search_console_token_only_when_set(self):
        self.assertContains(self.client.get(reverse('home')), '<meta name="google-site-verification" content="abc123" />')

    def test_no_search_console_token_by_default(self):
        self.assertNotContains(self.client.get(reverse('home')), 'google-site-verification')

    @override_settings(INDEXNOW_KEY='0123abcd')
    def test_indexnow_key_file(self):
        response = self.client.get('/0123abcd.txt')
        self.assertEqual(response.content, b'0123abcd')
        self.assertEqual(self.client.get('/other.txt').status_code, 404)
        self.assertEqual(self.client.get('/robots.txt').status_code, 200)

    def test_home_names_the_organization(self):
        graph = self.ld_json(self.client.get(reverse('home')))
        self.assertEqual(graph['Organization']['alternateName'], 'FDQ')
        self.assertEqual(graph['WebSite']['url'], 'http://testserver/')

    def test_tier_1_is_a_course(self):
        course = self.ld_json(self.client.get(reverse('waitlist')))['Course']
        self.assertEqual(course['url'], 'http://testserver/tier-1/')
        self.assertEqual(course['offers']['price'], '495')

    def test_blog_post_is_an_article(self):
        from blog.models import BlogPost
        post = BlogPost.objects.create(title='Weld maps </script>', summary='<p>Why they exist.</p>', content='<p>Body</p>')
        response = self.client.get(reverse('blog_detail', args=[post.slug]))
        self.assertContains(response, '<meta property="og:type" content="article" />')
        self.assertContains(response, '<meta name="description" content="Why they exist." />')
        self.assertEqual(self.ld_json(response)['BlogPosting']['headline'], 'Weld maps </script>')
        self.assertContains(self.client.get(reverse('sitemap')), f'<lastmod>{post.created_at.date():%Y-%m-%d}</lastmod>')


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


class VisitorsPageTests(TestCase):
    def setUp(self):
        super().setUp()
        self.staff = get_user_model().objects.create_superuser(email='boss@example.com', password='pw-for-tests-only',
                                                               first_name='B', last_name='B')

    def test_staff_only(self):
        self.assertEqual(self.client.get(reverse('staff_visitors')).status_code, 302)

    def test_counts_visitors_by_source_and_hour(self):
        Client().get(reverse('waitlist') + '?utm_source=facebook&utm_campaign=reel-12', HTTP_USER_AGENT=FACEBOOK_PHONE)
        Client().get(reverse('home'), HTTP_REFERER='https://provenhand.com/feed/')
        Client().get(reverse('home'), HTTP_USER_AGENT='Render/1.0')
        Client().get(reverse('home'), HTTP_SEC_PURPOSE='prefetch')
        self.client.force_login(self.staff)
        response = self.client.get(reverse('staff_visitors') + '?days=7')
        self.assertContains(response, 'Visitors today')
        self.assertEqual(response.context['today_visitors'], 2)
        sources = {name: n for name, n, *_ in response.context['by_source']}
        self.assertEqual(sources, {'Facebook': 1, 'ProvenHand': 1})
        self.assertIn(('reel-12', 1, 0, 0), response.context['by_campaign'])
        self.assertEqual(sum(h['visitors'] for h in response.context['hourly']), 2)

    def test_admin_home_links_the_visitors_page(self):
        self.client.force_login(self.staff)
        self.assertContains(self.client.get(reverse('admin:index')), reverse('staff_visitors'))


class OwnVisitsTests(TestCase):
    """Our own browsers drop out of the visitor reports, past visits included."""

    def setUp(self):
        super().setUp()
        self.staff = get_user_model().objects.create_superuser(email='boss@example.com', password='pw-for-tests-only',
                                                               first_name='B', last_name='B')
        self.boss = Client()
        self.boss.force_login(self.staff)

    def visitors_today(self):
        return self.boss.get(reverse('staff_visitors') + '?days=7').context['today_visitors']

    def test_not_me_leaves_out_past_and_future_visits_until_undone(self):
        phone = Client()
        phone.get(reverse('home'))
        Client().get(reverse('home'))
        self.assertEqual(self.visitors_today(), 2)

        self.assertContains(phone.get(reverse('not_me')), "Don't count this browser")
        response = phone.post(reverse('not_me'))
        self.assertContains(response, "This browser isn't counted.")
        phone.get(reverse('about'))
        self.assertEqual(self.visitors_today(), 1)
        # The page itself isn't a visit.
        self.assertFalse(SiteEvent.objects.filter(path='/not-me/').exists())

        phone.post(reverse('not_me'), {'count_again': '1'})
        self.assertFalse(InternalVisitor.objects.filter(visitor_id=phone.cookies[VISITOR_COOKIE].value).exists())
        self.assertEqual(self.visitors_today(), 2)

    def test_a_browser_signed_in_as_staff_is_left_out(self):
        self.boss.get(reverse('home'))
        Client().get(reverse('home'))
        self.assertTrue(InternalVisitor.objects.filter(visitor_id=self.boss.cookies[VISITOR_COOKIE].value).exists())
        self.assertEqual(self.visitors_today(), 1)
        funnel = self.boss.get(reverse('staff_funnel') + '?days=7')
        self.assertEqual(funnel.context['steps'][0][1], 1)
        self.assertContains(funnel, '1 of your own browsers is left out')

    def test_admin_home_panel_leaves_them_out_too(self):
        self.boss.get(reverse('home'))
        Client().get(reverse('home'))
        home = self.boss.get(reverse('admin:index'))
        self.assertContains(home, '<b>1</b><span>Visitors today</span>', html=False)
        self.assertContains(home, '<b>1</b><span>Visitors in 7 days</span>', html=False)

    def test_robots_keeps_it_out_of_search(self):
        self.assertContains(self.client.get(reverse('robots')), 'Disallow: /not-me/')


class PageDetailTests(TestCase):
    """The page script's batched events and the Pages, Forms and visitor reports built on them."""

    def setUp(self):
        super().setUp()
        staff = get_user_model().objects.create_superuser(email='boss@example.com', password='pw-for-tests-only',
                                                          first_name='B', last_name='B')
        self.boss = Client()
        self.boss.force_login(staff)

    def send(self, client, *events):
        return client.post(reverse('beacon'), {'events': [{'name': n, 'props': p} for n, p in events]},
                           content_type='application/json')

    def visitor(self, path='/', **headers):
        client = Client()
        client.get(path, **headers)
        return client

    def test_beacon_takes_a_batch_and_drops_unknown_events(self):
        hand = self.visitor()
        response = self.send(hand, ('tap', {'kind': 'link', 'label': 'Get lesson 1 free', 'to': '/tier-1/#sign-up', 'page': '/'}),
                             ('section_view', {'section': 'hero', 'order': 1, 'page': '/'}), ('drop_table', {}))
        self.assertEqual(response.status_code, 204)
        self.assertEqual(sorted(SiteEvent.objects.exclude(name='page_view').values_list('name', flat=True)), ['section_view', 'tap'])
        tap = SiteEvent.objects.get(name='tap')
        self.assertEqual((tap.path, tap.props['label'], tap.visitor_id), ('/', 'Get lesson 1 free', hand.cookies[VISITOR_COOKIE].value))
        too_many = self.send(hand, *[('tap', {'kind': 'link'})] * 21)
        self.assertEqual(too_many.status_code, 400)
        self.assertEqual(self.send(hand, ('drop_table', {})).status_code, 400)

    def test_pages_report_reading_and_taps(self):
        for seconds, scroll in ((45, 80), (5, 10)):
            hand = self.visitor()
            self.send(hand, ('section_view', {'section': 'hero', 'order': 1, 'page': '/'}),
                      ('page_leave', {'view': 'a1', 'seconds': seconds // 2, 'scroll': scroll // 2, 'page': '/'}),
                      ('page_leave', {'view': 'a1', 'seconds': seconds, 'scroll': scroll, 'page': '/'}),
                      ('tap', {'kind': 'link', 'label': 'See all 12 modules', 'to': '/tier-1/#modules', 'section': 'tier-1', 'page': '/'}))
            if seconds == 45:
                self.send(hand, ('section_view', {'section': 'tier-1', 'order': 3, 'page': '/'}),
                          ('tap', {'kind': 'dead', 'label': 'img: weld log', 'section': 'weld-log', 'page': '/'}))
        response = self.boss.get(reverse('staff_pages') + '?days=7&page=/')
        self.assertEqual(response.status_code, 200)
        context = response.context
        self.assertEqual([(s['name'], s['visitors'], s['share']) for s in context['sections']], [('hero', 2, 100), ('tier-1', 1, 50)])
        self.assertEqual(context['measured'], 2)
        self.assertEqual({b['label']: b['count'] for b in context['times']}['30 seconds to a minute'], 1)
        self.assertEqual(context['taps'][0]['label'], 'See all 12 modules')
        self.assertEqual(context['taps'][0]['visitors'], 2)
        self.assertEqual(context['dead'][0]['label'], 'img: weld log')
        row = context['table'][0]
        self.assertEqual((row['path'], row['visitors'], row['median_seconds']), ('/', 2, 25.0))

    def test_forms_report_steps_stops_errors_and_speed(self):
        sender, quitter = self.visitor('/tier-1/'), self.visitor('/tier-1/')
        self.send(sender, ('field_focus', {'form': 'wl-form', 'field': 'email', 'page': '/tier-1/'}),
                  ('form_send', {'form': 'wl-form', 'seconds': 12, 'fields': 1, 'page': '/tier-1/'}),
                  ('page_speed', {'view': 'b', 'first_byte': 300, 'ready': 900, 'biggest_paint': 1800, 'page': '/tier-1/'}))
        self.send(quitter, ('field_focus', {'form': 'wl-form', 'field': 'email', 'page': '/tier-1/'}),
                  ('field_focus', {'form': 'wl-form', 'field': 'trade', 'page': '/tier-1/'}),
                  ('form_abandon', {'form': 'wl-form', 'last_field': 'trade', 'fields': 2, 'filled': 1, 'page': '/tier-1/'}),
                  ('js_error', {'message': 'x is not defined', 'file': '/tier-1/', 'line': 12, 'page': '/tier-1/'}),
                  ('turnstile_shown', {'page': '/tier-1/'}))
        context = self.boss.get(reverse('staff_forms') + '?days=7').context
        form = context['forms'][0]
        self.assertEqual((form['form'], form['started'], form['sent'], form['left'], form['median_seconds']), ('Tier 1 sign-up', 2, 1, 1, 12))
        self.assertEqual(form['last_fields'], [('trade', 1)])
        self.assertEqual(form['left_with_something_filled'], 1)
        self.assertEqual(context['errors'][0]['message'], 'x is not defined')
        self.assertEqual(context['shown'], [('/tier-1/', 1)])
        self.assertEqual(context['speed'][0]['values'][:3], [0.3, 0.9, 1.8])

    def test_visitor_timeline(self):
        hand = self.visitor('/?utm_source=facebook&utm_campaign=fdq-fb1', HTTP_USER_AGENT=FACEBOOK_PHONE)
        self.send(hand, ('tap', {'kind': 'link', 'label': 'Tier 1', 'to': '/tier-1/', 'section': 'nav', 'page': '/'}),
                  ('page_leave', {'view': 'c', 'seconds': 31, 'scroll': 64, 'page': '/'}))
        visitor_id = hand.cookies[VISITOR_COOKIE].value
        response = self.boss.get(reverse('staff_visitor', args=[visitor_id]))
        self.assertContains(response, 'from Facebook (fdq-fb1)')
        self.assertContains(response, 'Tier 1 → /tier-1/')
        self.assertContains(response, '31 s on screen, scrolled 64%')
        self.assertEqual(self.boss.get(reverse('staff_visitor', args=['nope'])).status_code, 404)
        visitors = self.boss.get(reverse('staff_visitors') + '?days=7')
        self.assertContains(visitors, reverse('staff_visitor', args=[visitor_id]))
        self.assertEqual(Client().get(reverse('staff_visitor', args=[visitor_id])).status_code, 302)


@override_settings(CLARITY_PROJECT_ID='abc123xyz')
class ClarityTests(TestCase):
    def test_loads_for_visitors_with_their_id(self):
        response = self.client.get(reverse('home'))
        self.assertContains(response, 'https://www.clarity.ms/tag/')
        self.assertContains(response, '"abc123xyz"')
        self.assertContains(response, f'"fdq_vid", "{response.cookies[VISITOR_COOKIE].value}"')
        self.assertContains(self.client.get(reverse('privacy')), 'Microsoft Clarity')

    def test_not_on_private_pages_for_staff_or_our_own_browsers(self):
        self.assertNotContains(self.client.get(reverse('not_me')), 'clarity.ms')
        self.client.post(reverse('not_me'))
        self.assertNotContains(self.client.get(reverse('home')), 'clarity.ms')
        staff = get_user_model().objects.create_superuser(email='boss@example.com', password='pw-for-tests-only',
                                                          first_name='B', last_name='B')
        boss = Client()
        boss.force_login(staff)
        self.assertNotContains(boss.get(reverse('home')), 'clarity.ms')

    def test_key_steps_go_to_clarity_as_events(self):
        self.assertContains(self.client.get(reverse('home')), "window.clarity('event', name)")

    def test_forms_and_emails_are_masked(self):
        self.assertContains(self.client.get(reverse('waitlist')), 'id="wl-form" data-clarity-mask="true"')

    @override_settings(CLARITY_PROJECT_ID='')
    def test_off_without_a_project_id(self):
        self.assertNotContains(self.client.get(reverse('home')), 'clarity.ms')
        privacy = self.client.get(reverse('privacy'))
        self.assertNotContains(privacy, 'uses Microsoft Clarity')
        self.assertContains(privacy, 'There are no third-party analytics.')


class SourceLabelTests(TestCase):
    def test_labels(self):
        from .analytics import source_label
        self.assertEqual(source_label('fb', '', ''), 'Facebook')
        self.assertEqual(source_label('', 'l.facebook.com', ''), 'Facebook')
        self.assertEqual(source_label('', '', 'facebook'), 'Facebook')
        self.assertEqual(source_label('', 'l.instagram.com', ''), 'Instagram')
        self.assertEqual(source_label('', 'www.provenhand.com', ''), 'ProvenHand')
        self.assertEqual(source_label('', 'www.google.com', ''), 'Search')
        self.assertEqual(source_label('', '', ''), 'Direct or unknown')


class SitePolishTests(TestCase):
    def test_no_public_log_in_link(self):
        for name in ('home', 'waitlist', 'about'):
            self.assertNotContains(self.client.get(reverse(name)), 'href="/accounts/login/"')

    def test_modules_open_by_default_and_fold_on_phones(self):
        response = self.client.get(reverse('waitlist'))
        self.assertContains(response, '<details class="mod" id="module-6" open>', html=False)
        self.assertContains(response, "matchMedia('(max-width: 800px)')")

    def test_weld_field_sheet_name_and_description(self):
        self.assertContains(self.client.get(reverse('waitlist')),
                            'Take your weld notes in the field to transfer to a weld map or weld log')
        self.assertNotContains(self.client.get(reverse('home')), 'weld field sheet')


class RunNow:
    """Stands in for threading.Thread so the alert is sent inside the test."""

    def __init__(self, target, args=(), daemon=None):
        self.target, self.args = target, args

    def start(self):
        self.target(*self.args)


@override_settings(SIGNUP_ALERT_NTFY_TOPIC='fdq-test-topic', NTFY_SERVER='https://ntfy.example')
class SignupAlertTests(TestCase):
    def test_new_signup_sends_one_phone_alert_without_the_email(self):
        sent = []
        with mock.patch('core.alerts.threading.Thread', RunNow), \
             mock.patch('core.alerts.urllib.request.urlopen', lambda request, timeout: sent.append(request) or io.BytesIO()):
            self.client.get(reverse('waitlist') + '?utm_source=facebook&utm_campaign=reel-12', HTTP_USER_AGENT=FACEBOOK_PHONE)
            form = {'email': 'hand@example.com', 'website': '', 'utm_source': 'facebook', 'utm_campaign': 'reel-12'}
            self.client.post(reverse('waitlist'), form, HTTP_USER_AGENT=FACEBOOK_PHONE)
            self.client.post(reverse('waitlist'), form, HTTP_USER_AGENT=FACEBOOK_PHONE)
        self.assertEqual(len(sent), 1)
        alert = sent[0]
        self.assertEqual(alert.full_url, 'https://ntfy.example/fdq-test-topic')
        self.assertEqual(alert.get_header('Title'), 'New Tier 1 signup')
        body = alert.data.decode()
        self.assertIn('Facebook · reel-12 · phone in the Facebook app', body)
        self.assertIn('1 on the list now.', body)
        self.assertNotIn('hand@example.com', body)
        self.assertIn('/admin/core/waitlistsignup/', alert.get_header('Click'))

    def test_admin_test_button(self):
        staff = get_user_model().objects.create_superuser(email='boss@example.com', password='pw-for-tests-only',
                                                          first_name='B', last_name='B')
        self.client.force_login(staff)
        self.assertContains(self.client.get(reverse('admin:index')), 'Send a test alert')
        sent = []
        with mock.patch('core.alerts.threading.Thread', RunNow), \
             mock.patch('core.alerts.urllib.request.urlopen', lambda request, timeout: sent.append(request) or io.BytesIO()):
            response = self.client.post(reverse('staff_test_alert'), follow=True)
        self.assertContains(response, 'Test alert sent.')
        self.assertEqual(sent[0].get_header('Title'), 'FDQ test alert')


class NoAlertsTests(TestCase):
    def test_off_without_a_topic(self):
        with mock.patch('core.alerts.threading.Thread') as thread:
            self.client.post(reverse('waitlist'), {'email': 'hand@example.com', 'website': ''})
        thread.assert_not_called()


class PriceTests(TestCase):
    def test_tier1_page_shows_the_price_and_the_founding_price(self):
        response = self.client.get(reverse('waitlist'))
        self.assertContains(response, 'Founding price: $395')
        self.assertContains(response, 'Nothing to pay now.')
        self.assertContains(response, '$495. People on the list pay the founding price, $395.')

    @override_settings(**EMAIL_ON)
    def test_thanks_page_and_email_tell_a_new_signup_their_price(self):
        self.client.post(reverse('waitlist'), {'email': 'hand@example.com', 'website': ''})
        self.assertContains(self.client.get(reverse('waitlist_thanks')), "You're in for the founding price: $395 instead of $495.")
        self.assertIn('founding price: $395 instead of $495', mail.outbox[0].body)

    @override_settings(TIER1_PRICE='', TIER1_FOUNDING_PRICE='')
    def test_no_price_set_says_it_is_coming(self):
        response = self.client.get(reverse('waitlist'))
        self.assertContains(response, 'The price goes on this page before Tier 1 opens.')
        self.assertNotContains(response, 'Founding price')
