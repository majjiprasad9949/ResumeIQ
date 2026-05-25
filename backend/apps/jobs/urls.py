"""
URL configuration for jobs app.
"""

from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import JobDescriptionViewSet

router = DefaultRouter()
router.register(r'', JobDescriptionViewSet, basename='job')

urlpatterns = [
    path('', include(router.urls)),
]
