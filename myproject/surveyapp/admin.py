# from django.contrib import admin
# from django import forms
# from django.db import models
# from django.forms import Textarea
# from .models import Survey, Answer, QuestionAnswer
# import json


# class PrettyJSONWidget(forms.Textarea):
#     """Widget to pretty-print JSON data in the admin."""
#     def __init__(self, *args, **kwargs):
#         super().__init__(*args, **kwargs)
#         self.attrs['style'] = 'width: 90%; height: 400px; font-family: monospace;'

#     def format_value(self, value):
#         """Pretty-print JSON for display."""
#         if isinstance(value, str):
#             try:
#                 value = json.loads(value)  # Convert string to JSON object
#             except json.JSONDecodeError:
#                 pass
#         if isinstance(value, (dict, list)):
#             return json.dumps(value, indent=4, sort_keys=True)
#         return value


# class SurveyForm(forms.ModelForm):
#     """Custom form to pretty-print the JSONField."""
#     structure = forms.JSONField(
#         widget=PrettyJSONWidget(attrs={
#             'placeholder': (
#                 '[\n'
#                 '    {\n'
#                 '        "choices": [\n'
#                 '            "Yes",\n'
#                 '            "No"\n'
#                 '        ],\n'
#                 '        "id": 1,\n'
#                 '        "label": "Is Safety Guarding in place, secure and unobstructed?",\n'
#                 '        "name": "safety_guarding",\n'
#                 '        "required": true,\n'
#                 '        "type": "choice"\n'
#                 '    },\n'
#                 '    {\n'
#                 '        "choices": [\n'
#                 '            "Yes",\n'
#                 '            "No"\n'
#                 '        ],\n'
#                 '        "id": 2,\n'
#                 '        "label": "Are electrical cabinets closed?",\n'
#                 '        "name": "electrical_cabinets",\n'
#                 '        "required": true,\n'
#                 '        "type": "choice"\n'
#                 '    }\n'
#                 ']'
#             )
#         }),
#         help_text="Define the structure of the survey as JSON."
#     )

#     class Meta:
#         model = Survey
#         fields = '__all__'


# class SurveyAdmin(admin.ModelAdmin):
#     form = SurveyForm
#     list_display = ('id', 'name', 'description', 'cell', 'created_at')
#     search_fields = ('name', 'description')
#     list_filter = ('name',)
#     ordering = ('id',)


# class AnswerAdmin(admin.ModelAdmin):
#     list_display = ('id', 'survey', 'response_data', 'submitted_at', 'status_by_admin', 'comment_by_admin')
#     search_fields = ('survey__name', 'response_data')
#     list_filter = ('survey', 'status_by_admin', 'submitted_at')
#     ordering = ('-submitted_at',)
#     list_editable = ('status_by_admin', 'comment_by_admin')

#     formfield_overrides = {
#         models.TextField: {'widget': Textarea(attrs={'rows': 2, 'cols': 45})},
#     }
#     actions = ['set_status_open', 'set_status_closed']

#     def set_status_open(self, request, queryset):
#         queryset.update(status_by_admin='open')
#     set_status_open.short_description = "Mark selected items as Open"

#     def set_status_closed(self, request, queryset):
#         queryset.update(status_by_admin='closed')
#     set_status_closed.short_description = "Mark selected items as Closed"

# class QuestionAnswerAdmin(admin.ModelAdmin):
#     list_display = ('id', 'survey', 'answer', 'question_id', 'question_text', 'response', 'issue', 'action_taken', 'status_by_admin', 'comment_by_admin', 'submitted_at')
#     search_fields = ('survey__name', 'question_text', 'answer')
#     list_filter = ('survey', 'status_by_admin', 'submitted_at')
#     ordering = ('-submitted_at',)
#     list_editable = ('status_by_admin', 'comment_by_admin')

#     formfield_overrides = {
#         models.TextField: {'widget': Textarea(attrs={'rows': 2, 'cols': 45})},
#     }

#     actions = ['set_status_open', 'set_status_closed']

#     def set_status_open(self, request, queryset):
#         queryset.update(status_by_admin='open')
#     set_status_open.short_description = "Mark selected items as Open"

#     def set_status_closed(self, request, queryset):
#         queryset.update(status_by_admin='closed')
#     set_status_closed.short_description = "Mark selected items as Closed"


# admin.site.register(Survey, SurveyAdmin)
# admin.site.register(Answer, AnswerAdmin)
# admin.site.register(QuestionAnswer, QuestionAnswerAdmin)
from django.contrib import admin
from django import forms
from django.db import models
from django_svelte_jsoneditor.widgets import SvelteJSONEditorWidget

from django.forms import Textarea
from .models import Survey, Answer, QuestionAnswer


class SurveyForm(forms.ModelForm):
    structure = forms.JSONField(
        widget=SvelteJSONEditorWidget(attrs={'style': 'width: 100%; height: 400px;'}),
        help_text="Define the structure of the survey as JSON."
    )

    class Meta:
        model = Survey
        fields = '__all__'


class SurveyAdmin(admin.ModelAdmin):
    form = SurveyForm
    list_display = ('id', 'name', 'description', 'cell', 'created_at')
    search_fields = ('name', 'cell')
    list_filter = ('name',)
    ordering = ('id',)


class AnswerAdmin(admin.ModelAdmin):
    list_display = ('id', 'survey', 'response_data', 'submitted_at')
    search_fields = ('survey__name', 'response_data')
    list_filter = ('survey', 'submitted_at')
    ordering = ('-submitted_at',)

    formfield_overrides = {
        models.TextField: {'widget': Textarea(attrs={'rows': 2, 'cols': 45})},
    }
    actions = ['set_status_open', 'set_status_closed']

    def set_status_open(self, request, queryset):
        queryset.update(status_by_admin='open')
    set_status_open.short_description = "Mark selected items as Open"

    def set_status_closed(self, request, queryset):
        queryset.update(status_by_admin='closed')
    set_status_closed.short_description = "Mark selected items as Closed"


class QuestionAnswerAdmin(admin.ModelAdmin):
    list_display = ('id', 'survey', 'answer', 'question_id', 'question_text', 'response', 'issue', 'action_taken', 'status_by_admin', 'comment_by_admin', 'submitted_at')
    search_fields = ('survey__name', 'question_text', 'answer')
    list_filter = ('survey', 'status_by_admin', 'submitted_at')
    ordering = ('-submitted_at',)
    list_editable = ('status_by_admin', 'comment_by_admin')

    formfield_overrides = {
        models.TextField: {'widget': Textarea(attrs={'rows': 2, 'cols': 45})},
    }

    actions = ['set_status_open', 'set_status_closed']

    def set_status_open(self, request, queryset):
        queryset.update(status_by_admin='open')
    set_status_open.short_description = "Mark selected items as Open"

    def set_status_closed(self, request, queryset):
        queryset.update(status_by_admin='closed')
    set_status_closed.short_description = "Mark selected items as Closed"


admin.site.register(Survey, SurveyAdmin)
admin.site.register(Answer, AnswerAdmin)
admin.site.register(QuestionAnswer, QuestionAnswerAdmin)
