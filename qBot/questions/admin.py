from django.contrib import admin
from questions.models import Question, Answer


# makes the question admin show up in the admin panel
@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    list_display = ["title", "user", "created_at"]
    list_filter = ["created_at", "user"]
    search_fields = ["title", "content", "user"]

    class Meta:
        model = Question

@admin.register(Answer)
class AnswerAdmin(admin.ModelAdmin):
    list_display = ["body", "answer_to", "user", "created_at"]
    list_filter = ["created_at", "user", "body"]
    search_fields = ["answer_to", "content", "user"]

    class Meta:
        model = Answer

