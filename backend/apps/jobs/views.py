from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from .models import JobDescription
from .serializers import (
    JobDescriptionListSerializer,
    JobDescriptionDetailSerializer,
    JobDescriptionUploadSerializer
)


class JobDescriptionViewSet(
    viewsets.ModelViewSet
):

    permission_classes = [
        IsAuthenticated
    ]


    def get_queryset(self):

        return JobDescription.objects.filter(

            user=self.request.user

        )


    def get_serializer_class(self):

        if self.action == "retrieve":

            return JobDescriptionDetailSerializer

        elif self.action == "upload":

            return JobDescriptionUploadSerializer

        return JobDescriptionListSerializer


    @action(
        detail=False,
        methods=["post"]
    )
    def upload(self, request):

        serializer = JobDescriptionUploadSerializer(

            data=request.data

        )

        serializer.is_valid(

            raise_exception=True

        )

        job = JobDescription.objects.create(

            user=request.user,

            title=serializer.validated_data[
                "title"
            ],

            company=serializer.validated_data.get(
                "company"
            ),

            content=serializer.validated_data[
                "content"
            ],

            source_url=serializer.validated_data.get(
                "source_url"
            )

        )

        return Response(

            JobDescriptionDetailSerializer(
                job
            ).data,

            status=status.HTTP_201_CREATED

        )