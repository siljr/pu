from django.contrib import admin
from questions.models import Question, Answer


# makes the question admin show up in the admin panel
@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    pass

@admin.register(Answer)
class AnswerAdmin(admin.ModelAdmin):
    pass