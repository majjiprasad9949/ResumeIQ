"""
URL configuration for ResumeIQ project.
"""

from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    # Admin
    path('admin/', admin.site.urls),
    
    # API endpoints
    path('api/users/', include('apps.users.urls')),
    path('api/resumes/', include('apps.resumes.urls')),
    path('api/jobs/', include('apps.jobs.urls')),
    path('api/analysis/', include('apps.analysis.urls')),
]

# Serve media files in development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

from django.conf import settings
from django.conf.urls.static import static

urlpatterns += static(

    settings.MEDIA_URL,

    document_root=settings.MEDIA_ROOT

)
