from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('core.urls')),
    path('blog/', include('blog.urls')),
    path('accounts/', include('accounts.urls', namespace='accounts')),
    path('apply/', include('applications.urls', namespace='applications')),
    path('certifications/', include('lms.urls', namespace='lms')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
