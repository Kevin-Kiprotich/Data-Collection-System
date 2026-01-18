import json
from django.db import transaction
from django.contrib.gis.geos import Point, LineString, Polygon, GEOSGeometry
from rest_framework.views import APIView
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status

from .models import (
    Questionnaire,
    Question,
    Submission,
    Answer,
)


class BulkSubmissionView(APIView):
    """
    Handles bulk multipart submission.
    Requires authentication.
    Creates one Submission + many Answers.
    """
    permission_classes = [IsAuthenticated]
    parser_classes = (MultiPartParser, FormParser)

    @transaction.atomic
    def post(self, request):
        user = request.user
        answers_raw = request.data.get("answers")
        questionnaire_id = request.data.get("questionnaire")

        if not answers_raw or not questionnaire_id:
            return Response(
                {"detail": "Questionnaire ID and answers are required"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        try:
            answers_data = json.loads(answers_raw)
        except json.JSONDecodeError:
            return Response(
                {"detail": "Invalid JSON in answers field"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        try:
            questionnaire = Questionnaire.objects.get(id=questionnaire_id)
        except Questionnaire.DoesNotExist:
            return Response(
                {"detail": "Questionnaire not found"},
                status=status.HTTP_404_NOT_FOUND,
            )

        # ---------- Create submission (monitoring entry) ----------
        submission = Submission.objects.create(
            questionnaire=questionnaire,
            enumerator=user,
        )

        files = request.FILES
        answer_objects = []

        # ---------- Prefetch questions to avoid N+1 ----------
        questions = {
            str(q.id): q
            for q in Question.objects.filter(
                questionnaire=questionnaire
            )
        }

        for item in answers_data:
            question_id = str(item.get("question"))
            question = questions.get(question_id)

            if not question:
                continue

            answer = Answer(
                question=question,
            )

            answer_type = question.answer_type

            # ---------- TEXT ----------
            if answer_type == "SHORT_TEXT":
                answer.short_text_answer = item.get("answer_text")

            elif answer_type == "LONG_TEXT":
                answer.long_text_answer = item.get("answer_text")

            elif answer_type == "PHONE_NUMBER":
                answer.phone_number_answer = item.get("answer_text")

            elif answer_type == "EMAIL":
                answer.email_answer = item.get("answer_text")

            elif answer_type == "LINK":
                answer.link_answer = item.get("answer_url")

            elif answer_type == "TIMESTAMP":
                answer.timestamp_answer = item.get("answer_timestamp")

            # ---------- NUMBERS ----------
            elif answer_type == "INTEGER":
                answer.integer_answer = item.get("answer_integer")

            elif answer_type == "DECIMAL":
                answer.decimal_answer = item.get("answer_decimal")

            # ---------- CHOICES ----------
            elif answer_type == "SINGLE_CHOICE":
                answer.single_choice_answer = item.get("answer_choice")

            elif answer_type == "MULTI_CHOICE":
                answer.multi_choice_answer = item.get("answer_choice")

            # ---------- GEOMETRY ----------
            elif answer_type == "POINT":
                lat, lng = map(float, item["answer_point"].split(","))
                answer.point_answer = Point(lng, lat, srid=4326)

            elif answer_type == "LINE":
                coords = item["answer_line"]["features"][0]["geometry"]["coordinates"]
                answer.line_answer = LineString(coords, srid=4326)

            elif answer_type == "POLYGON":
                coords = item["answer_polygon"]["features"][0]["geometry"]["coordinates"][0]
                answer.polygon_answer = Polygon(coords, srid=4326)

            # ---------- FILES ----------
            file = files.get(question_id)
            if file:
                if answer_type == "IMAGE":
                    answer.image_answer = file
                elif answer_type == "DOCUMENT":
                    answer.document_answer = file
                elif answer_type == "VIDEO":
                    answer.video_answer = file
                elif answer_type == "AUDIO":
                    answer.audio_answer = file

            answer_objects.append(answer)

        # ---------- Bulk insert ----------
        Answer.objects.bulk_create(answer_objects, batch_size=500)

        return Response(
            {
                "detail": "Submission successful",
                "submission_id": submission.id,
                "answers_saved": len(answer_objects),
            },
            status=status.HTTP_201_CREATED,
        )
