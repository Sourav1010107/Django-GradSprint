from django.contrib import admin

from .models import (
    Test, Section, Question, Choice, Blank, BlankChoice,
    NumericValue, StudentAnswer, TestResult,
)


@admin.register(Test)
class TestAdmin(admin.ModelAdmin):
    list_display = ("id", "name")
    search_fields = ("name",)


@admin.register(Section)
class SectionAdmin(admin.ModelAdmin):
    list_display = ("id", "test", "name", "order", "time")
    list_filter = ("test",)
    search_fields = ("name", "test__name")
    ordering = ("test", "order")


@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    list_display = (
        "id", "section", "order", "question_type", "topic",
        "subtopic", "difficulty", "expected_time_seconds",
    )
    list_filter = (
        "section__test", "question_type", "topic",
        "subtopic", "difficulty",
    )
    search_fields = (
        "question", "topic", "subtopic",
        "section__name", "section__test__name",
    )
    ordering = ("section", "order")


@admin.register(Choice)
class ChoiceAdmin(admin.ModelAdmin):
    list_display = ("id", "question", "order", "text", "is_correct")
    list_filter = ("is_correct",)
    search_fields = ("text", "question__question")


@admin.register(Blank)
class BlankAdmin(admin.ModelAdmin):
    list_display = ("id", "question", "order")


@admin.register(BlankChoice)
class BlankChoiceAdmin(admin.ModelAdmin):
    list_display = ("id", "blank", "order", "text", "is_correct")
    list_filter = ("is_correct",)
    search_fields = ("text",)


@admin.register(NumericValue)
class NumericValueAdmin(admin.ModelAdmin):
    list_display = ("id", "question", "correct_value")
    search_fields = ("question__question",)


@admin.register(StudentAnswer)
class StudentAnswerAdmin(admin.ModelAdmin):
    list_display = (
        "user", "question", "topic", "subtopic", "difficulty",
        "is_correct", "time_taken", "expected_time", "answered_at",
    )
    list_filter = (
        "is_correct", "question__topic", "question__subtopic",
        "question__difficulty", "question__question_type",
    )
    search_fields = (
        "user__username", "question__question",
        "question__topic", "question__subtopic",
    )
    ordering = ("-answered_at",)
    list_select_related = ("user", "question")

    @admin.display(ordering="question__topic", description="Topic")
    def topic(self, obj):
        return obj.question.topic

    @admin.display(ordering="question__subtopic", description="Subtopic")
    def subtopic(self, obj):
        return obj.question.subtopic

    @admin.display(ordering="question__difficulty", description="Difficulty")
    def difficulty(self, obj):
        return obj.question.difficulty

    @admin.display(
        ordering="question__expected_time_seconds",
        description="Expected Time"
    )
    def expected_time(self, obj):
        return obj.question.expected_time_seconds


@admin.register(TestResult)
class TestResultAdmin(admin.ModelAdmin):
    list_display = (
        "user", "test", "verbal_score", "quant_score", "total_score",
        "correct_answers", "total_attempted_question", "accuracy",
        "completed_at",
    )
    list_filter = ("test",)
    search_fields = ("user__username", "test__name")
    ordering = ("-completed_at",)
    list_select_related = ("user", "test")

