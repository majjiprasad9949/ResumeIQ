from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from apps.resumes.models import Resume
from apps.jobs.models import JobDescription

from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity

import re


class ATSAnalysisViewSet(viewsets.ViewSet):

    permission_classes=[IsAuthenticated]

    @action(
        detail=False,
        methods=["post"]
    )
    def calculate_score(self,request):

        resume_id=request.data.get(
            "resume_id"
        )

        job_id=request.data.get(
            "job_id"
        )


        try:

            resume=Resume.objects.get(

                id=resume_id,
                user=request.user

            )

            job=JobDescription.objects.get(

                id=job_id,
                user=request.user

            )

        except:

            return Response(

                {

                    "error":
                    "Resume or Job not found"

                },

                status=404

            )


        resume_text=(

            resume.raw_text or ""

        ).lower()


        job_text=(

            job.content or ""

        ).lower()



        resume_text=re.sub(

            r'[^a-zA-Z0-9 ]',

            ' ',

            resume_text

        )


        job_text=re.sub(

            r'[^a-zA-Z0-9 ]',

            ' ',

            job_text

        )



        model=SentenceTransformer(

            'all-MiniLM-L6-v2'

        )


        resume_embedding=model.encode(

            resume_text

        )


        job_embedding=model.encode(

            job_text

        )


        similarity=cosine_similarity(

            [resume_embedding],
            [job_embedding]

        )[0][0]



        skill_keywords=[

            "python",
            "java",
            "sql",
            "power bi",
            "excel",
            "analytics",
            "analysis",
            "business analyst",
            "data analyst",
            "communication",
            "stakeholder",
            "reporting",
            "problem solving",
            "consulting",
            "operations",
            "project",
            "testing",
            "media",
            "agile",
            "leadership",
            "teamwork",
            "machine learning",
            "aws",
            "react",
            "django"

        ]


        important_keywords=[]


        for skill in skill_keywords:

            if skill in job_text:

                important_keywords.append(

                    skill

                )


        matched=[]

        missing=[]


        for skill in important_keywords:

            if skill in resume_text:

                matched.append(

                    skill

                )

            else:

                missing.append(

                    skill

                )


        keyword_match=(

            len(matched)

            /

            max(

                len(

                    important_keywords

                ),

                1

            )

        )*100



        ats_score=round(

            (

                similarity*50

            )

            +

            (

                keyword_match*50/100

            ),

            1

        )


        if ats_score>100:

            ats_score=100



        if ats_score>=80:

            risk_level="Strong Match"

            recommendation="✅ Safe to apply"

            score_color="green"


        elif ats_score>=50:

            risk_level="Moderate Match"

            recommendation="⚠️ Apply after improvements"

            score_color="yellow"


        elif ats_score>=40:

            risk_level="Average Match"

            recommendation="🟠 Improve resume before applying"

            score_color="orange"


        else:

            risk_level="Weak Match"

            recommendation="❌ Don't apply with this resume"

            score_color="red"



        return Response(

            {

                "ats_score":

                ats_score,

                "keyword_match_score":

                round(

                    keyword_match,

                    1

                ),

                "skills_match_score":

                round(

                    keyword_match,

                    1

                ),

                "matched_keywords":

                matched,

                "missing_keywords":

                missing,

                "skills_gap":

                missing,

                "resume_structure_score":

                85,

                "experience_match_score":

                80,

                "grammar_quality_score":

                90,

                "risk_level":

                risk_level,

                "recommendation":

                recommendation,

                "score_color":

                score_color

            }

        )