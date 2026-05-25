from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from .models import Resume
from .serializers import (
    ResumeUploadSerializer,
    ResumeListSerializer,
    ResumeDetailSerializer
)

import fitz
import docx


class ResumeViewSet(viewsets.ModelViewSet):

    permission_classes = [IsAuthenticated]


    def get_queryset(self):

        return Resume.objects.filter(
            user=self.request.user
        )


    def get_serializer_class(self):

        if self.action == "upload":
            return ResumeUploadSerializer

        if self.action == "retrieve":
            return ResumeDetailSerializer

        return ResumeListSerializer

    def get_serializer_context(self):
        return {

        "request": self.request

        }

       


    @action(
        detail=False,
        methods=["post"]
    )
    def upload(self, request):

        uploaded_file = request.FILES.get("file")

        title = request.data.get("title")

        if not uploaded_file:

            return Response(
                {"error": "No file selected"},
                status=400
            )


        extracted_text = ""

        try:

            file_name = uploaded_file.name.lower()

            # PDF
            if file_name.endswith(".pdf"):

                pdf_bytes = uploaded_file.read()

                pdf = fitz.open(
                    stream=pdf_bytes,
                    filetype="pdf"
                )

                for page in pdf:

                    page_text = page.get_text()

                    if page_text:

                        extracted_text += page_text + "\n"


            # DOCX
            elif file_name.endswith(".docx"):

                document = docx.Document(
                    uploaded_file
                )

                for p in document.paragraphs:

                    extracted_text += (
                        p.text + "\n"
                    )


            # TXT
            elif file_name.endswith(".txt"):

                extracted_text = uploaded_file.read().decode(
                    "utf-8"
                )


        except Exception as e:

            print(
                "PDF extraction error:",
                e
            )


        uploaded_file.seek(0)


        resume = Resume.objects.create(

            user=request.user,

            title=title,

            file=uploaded_file,

            raw_text=extracted_text,

            file_size=uploaded_file.size,

            file_format=file_name.split(".")[-1]

        )


        serializer = ResumeDetailSerializer(

            resume,
            context={"request": request}

        )

        return Response(

            serializer.data,

            status=status.HTTP_201_CREATED

        )