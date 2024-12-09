from django.contrib import admin
from django import forms
from .models import Survey, Answer, QuestionAnswer
import json


class PrettyJSONWidget(forms.Textarea):
    """Widget to pretty-print JSON data in the admin."""
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.attrs['style'] = 'width: 90%; height: 400px; font-family: monospace;'

    def format_value(self, value):
        """Pretty-print JSON for display."""
        if isinstance(value, str):
            try:
                value = json.loads(value)  # Convert string to JSON object
            except json.JSONDecodeError:
                pass
        if isinstance(value, (dict, list)):
            return json.dumps(value, indent=4, sort_keys=True)
        return value


class SurveyForm(forms.ModelForm):
    """Custom form to pretty-print the JSONField."""
    structure = forms.JSONField(
        widget=PrettyJSONWidget,
        help_text="Define the structure of the survey as JSON."
    )

    class Meta:
        model = Survey
        fields = '__all__'


class SurveyAdmin(admin.ModelAdmin):
    form = SurveyForm
    list_display = ('id', 'name', 'description', 'created_at')
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
