from django.contrib import admin
from django.utils.html import format_html
from leaflet.admin import LeafletGeoAdmin
from .models import (
    Questionnaire,
    Question,
    SkipLogic,
    FilterLogic,
    Submission,
    Answer,
)


class SkipLogicInline(admin.TabularInline):
    model = SkipLogic
    fk_name = "question"
    extra = 0

class FilterLogicInline(admin.TabularInline):
    model = FilterLogic
    fk_name = "question"
    extra = 0


class QuestionInline(admin.TabularInline):
    model = Question
    extra = 0

# Register your models here.
@admin.register(Questionnaire)
class QuestionnaireAdmin(admin.ModelAdmin):
    list_display = (
        "creator",
        "title",
        "created_at",
        "updated_at",
        "qr_preview",
        "link",
    )
    search_fields = ("title","creator__first_name","creator__last_name", "description")
    readonly_fields = ("qr_preview", "created_at", "updated_at")
    inlines = [QuestionInline]
    ordering = ("-created_at",)

    def qr_preview(self, obj):
        if obj.qr_code:
            return format_html(
                '<img src="{}" width="120" height="120" />',
                obj.qr_code.url
            )
        return "No QR"

    qr_preview.short_description = "QR Code"
    
@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    list_display = (
        "question",
        "questionnaire",
        "question_type",
        "answer_type",
        "is_required",
        "created_at",
        "updated_at",
    )
    search_fields = ("question", "questionnaire__title")
    readonly_fields = ("created_at", "updated_at")
    inlines = [SkipLogicInline, FilterLogicInline]
    ordering = ("-created_at",)
    
@admin.register(SkipLogic)
class SkipLogicAdmin(admin.ModelAdmin):
    list_display = (
        "question",
        "answer_value",
        "display_question",
        "created_at",
        "updated_at",
    )
    search_fields = ("question__question", "display_question__question", "answer_value")
    readonly_fields = ("created_at", "updated_at")
    ordering = ("-created_at",)
    
@admin.register(FilterLogic)
class FilterLogicAdmin(admin.ModelAdmin):       
    list_display = (
        "question",
        "source_question",
        "mapping",
        "created_at",
        "updated_at",
    )
    search_fields = ("question__question", "source_question__question", "mapping")
    readonly_fields = ("created_at", "updated_at")
    ordering = ("-created_at",)
    
@admin.register(Submission)
class SubmissionAdmin(admin.ModelAdmin):    
    list_display = (
        "questionnaire",
        "enumerator",
        "fill_duration",
        "submitted_at",
    )
    search_fields = ("questionnaire__title", "enumerator__firt_name", "enumerator__last_name", "enumerator__email")
    readonly_fields = ("submitted_at",)
    ordering = ("-submitted_at",)
    
@admin.register(Answer)
class AnswerAdmin(LeafletGeoAdmin):
    list_display = (
        "question",
        "created_at",
        "updated_at",
    )
    search_fields = ("question__question",)
    readonly_fields = ("id",)
    ordering = ("-created_at",)