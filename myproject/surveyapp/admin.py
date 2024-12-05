from django.contrib import admin
from .models import Survey, Answer, QuestionAnswer

class SurveyAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'description', 'structure')
    search_fields = ('name', 'description')
    list_filter = ('name',)
    ordering = ('id',)

class AnswerAdmin(admin.ModelAdmin):
    list_display = ('id', 'survey', 'response_data', 'submitted_at')
    search_fields = ('survey__name', 'response_data')
    list_filter = ('survey', 'submitted_at')
    ordering = ('-submitted_at',)

class QuestionAnswerAdmin(admin.ModelAdmin):
    list_display = ('id', 'survey', 'question_id', 'question_text', 'answer', 'issue', 'action_taken', 'submitted_at')
    search_fields = ('survey__name', 'question_text', 'answer')
    list_filter = ('survey', 'submitted_at')
    ordering = ('-submitted_at',)


admin.site.register(Survey, SurveyAdmin)
admin.site.register(Answer, AnswerAdmin)
admin.site.register(QuestionAnswer, QuestionAnswerAdmin)