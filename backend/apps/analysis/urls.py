from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views import ATSAnalysisViewSet

router = DefaultRouter()

router.register(
    "ats",
    ATSAnalysisViewSet,
    basename="ats"
)

urlpatterns = [

    path(
        "",
        include(
            router.urls
        )
    )

]