from django.contrib import admin
from django import forms
from django.db import models

from django_svelte_jsoneditor.widgets import SvelteJSONEditorWidget
from .widgets import CustomSvelteJSONEditorWidget
from django_json_widget.widgets import JSONEditorWidget

from django.forms import Textarea
from .models import Survey, Answer, QuestionAnswer, choice_tbl



class SurveyForm(forms.ModelForm):
    class Meta:
        model = Survey
        fields = '__all__'
        widgets = {
            'structure': JSONEditorWidget,
        }


class SurveyAdmin(admin.ModelAdmin):
    form = SurveyForm
    list_display = ('id', 'name', 'user', 'cell', 'description', 'active_status', 'sort_order', 'updated_at', 'created_at')
    list_display_links = ('name', 'user', 'updated_at', 'created_at')
    search_fields = ('name', 'cell', 'user__username')
    list_filter = ('active_status', 'created_at', 'updated_at', 'user')
    ordering = ('-created_at',)

    class Media:
        css = {
            'all': ('surveyapp/css/custom_admin.css',)
        }
        js = ('surveyapp/js/json_editor_maximize.js',)

    # Customize the form layout in the admin
    fieldsets = (
        (None, {
            'fields': (
                ('active_status', 'sort_order'),
                ('name', 'cell'),
                'description',
                'structure',
                'user',
            )
        }),
    )

    formfield_overrides = {
        models.TextField: {'widget': Textarea(attrs={'rows': 2, 'cols': 100})},
    }


class AnswerAdmin(admin.ModelAdmin):
    list_display = ('id', 'survey', 'user', 'response_data', 'active_status', 'sort_order', 'updated_at', 'created_at')
    list_display_links = ('survey', 'user', 'updated_at', 'created_at')
    search_fields = ('survey__name', 'response_data', 'user__username')
    list_filter = ('active_status', 'created_at', 'updated_at', 'user', 'survey')
    ordering = ('-created_at',)

    formfield_overrides = {
        models.TextField: {'widget': Textarea(attrs={'rows': 2, 'cols': 45})},
    }

    actions = ['set_status_open', 'set_status_closed']

    def set_status_open(self, request, queryset):
        queryset.update(active_status=1)
    set_status_open.short_description = "Mark selected items as Active"

    def set_status_closed(self, request, queryset):
        queryset.update(active_status=0)
    set_status_closed.short_description = "Mark selected items as Inactive"

class QuestionAnswerAdmin(admin.ModelAdmin):
    list_display = (
        'id', 'survey', 'answer', 'user', 'question_id', 'question_text', 'response',
        'issue', 'action_taken', 'status_by_admin', 'comment_by_admin', 'updated_at', 'created_at', 'active_status', 'sort_order'
    )
    list_display_links = ('id', 'survey', 'answer', 'user', 'updated_at', 'created_at')
    search_fields = ('survey__name', 'question_text', 'answer__response_data', 'user__username')
    list_filter = ('active_status', 'created_at', 'updated_at', 'status_by_admin', 'user', 'survey')
    ordering = ('-created_at',)
    list_editable = ('status_by_admin', 'comment_by_admin')

    formfield_overrides = {
        models.TextField: {'widget': Textarea(attrs={'rows': 2, 'cols': 20})},
    }

    actions = ['set_status_open', 'set_status_closed']

    def set_status_open(self, request, queryset):
        queryset.update(status_by_admin='open')
    set_status_open.short_description = "Mark selected items as Open"

    def set_status_closed(self, request, queryset):
        queryset.update(status_by_admin='closed')
    set_status_closed.short_description = "Mark selected items as Closed"

class ChoiceTblAdmin(admin.ModelAdmin):
    list_display = ('choice_tbl_grouping', 'choice_name')  # Display these fields in the admin list view
    search_fields = ('choice_tbl_grouping', 'choice_name')  # Add search functionality
    list_filter = ('choice_tbl_grouping',)  # Add a filter sidebar by grouping


# Register models with the admin site
admin.site.register(Survey, SurveyAdmin)
admin.site.register(Answer, AnswerAdmin)
admin.site.register(QuestionAnswer, QuestionAnswerAdmin)
admin.site.register(choice_tbl, ChoiceTblAdmin)
