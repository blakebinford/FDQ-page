import json
import re

from django import template
from django.conf import settings
from django.templatetags.static import static
from django.urls import reverse
from django.utils.html import strip_tags
from django.utils.safestring import mark_safe

register = template.Library()

# FDQ's own pages elsewhere. Google uses these to tie the site to the same organization.
SAME_AS = [
    'https://www.facebook.com/profile.php?id=61596185915140',
    'https://www.linkedin.com/company/144087831/',
]

TIER1_DESCRIPTION = ('An online course and certification for pipeline and facilities construction hands '
                     'with no quality background. It teaches the work of a contractor QC tech or an owner-side '
                     'junior inspector, on the right-of-way and inside the fence.')


def site_origin(request):
    """https://www.fielddrivenquality.com in production, whatever host served the page elsewhere."""
    return (settings.CANONICAL_ORIGIN or request.build_absolute_uri('/')).rstrip('/')


def _absolute(origin, url):
    return url if url.startswith('http') else origin + url


def _org(origin):
    return {
        '@type': 'Organization',
        '@id': f'{origin}/#org',
        'name': 'Field Driven Quality',
        'alternateName': 'FDQ',
        'url': f'{origin}/',
        'logo': _absolute(origin, static('images/apple-touch-icon.png')),
        'sameAs': SAME_AS,
    }


def _tier1(origin):
    course = {
        '@type': 'Course',
        '@id': f'{origin}/tier-1/#course',
        'name': 'FDQ Tier 1: From the crew to the quality side',
        'description': TIER1_DESCRIPTION,
        'url': f'{origin}{reverse("waitlist")}',
        'inLanguage': 'en-US',
        'provider': {'@id': f'{origin}/#org'},
        'hasCourseInstance': {'@type': 'CourseInstance', 'courseMode': 'Online'},
    }
    price = re.sub(r'[^\d.]', '', settings.TIER1_PRICE or '')
    if price:
        course['offers'] = {'@type': 'Offer', 'category': 'Paid', 'price': price, 'priceCurrency': 'USD'}
    return course


def _post(origin, post):
    data = {
        '@type': 'BlogPosting',
        'headline': post.title,
        'description': strip_tags(post.summary).strip()[:300],
        'url': f'{origin}{reverse("blog_detail", args=[post.slug])}',
        'datePublished': post.created_at.isoformat(),
        'author': {'@id': f'{origin}/#org'},
        'publisher': {'@id': f'{origin}/#org'},
    }
    if post.banner_image:
        data['image'] = _absolute(origin, post.banner_image.url)
    return data


@register.simple_tag(takes_context=True)
def structured_data(context, kind):
    """A JSON-LD block that tells search engines what the page is: the organization on
    every public page, plus the course on Tier 1 and the article on a blog post."""
    origin = site_origin(context['request'])
    graph = [_org(origin)]
    if kind == 'home':
        graph.append({'@type': 'WebSite', '@id': f'{origin}/#website', 'url': f'{origin}/',
                      'name': 'Field Driven Quality', 'alternateName': 'FDQ',
                      'publisher': {'@id': f'{origin}/#org'}})
    elif kind == 'tier1':
        graph.append(_tier1(origin))
    elif kind == 'post':
        graph.append(_post(origin, context['post']))
    data = json.dumps({'@context': 'https://schema.org', '@graph': graph})
    # Keep the JSON from closing the script tag early.
    data = data.replace('<', '\\u003c').replace('>', '\\u003e').replace('&', '\\u0026')
    return mark_safe(f'<script type="application/ld+json">{data}</script>')


@register.simple_tag(takes_context=True)
def canonical_url(context):
    """The page's one address: production host, no query string (so utm tags don't split it)."""
    request = context['request']
    return site_origin(request) + request.path


@register.simple_tag(takes_context=True)
def absolute(context, path):
    """A full address on the production host, for tags that need one (og:image)."""
    return site_origin(context['request']) + path
