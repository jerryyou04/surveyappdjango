# formsapp/models.py
from django.db import models
from django.core.serializers.json import DjangoJSONEncoder
from decimal import Decimal
import json 

class Survey(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    structure = models.JSONField(help_text="Define the structure of the survey as JSON.")  # Using models.JSONField (Django 3.1+)
    created_at = models.DateTimeField(auto_now_add=True)

    cell = models.CharField(max_length=100, help_text="Cell associated with this survey")
    def __str__(self):
        return self.name

class Answer(models.Model):
    STATUS_CHOICES = [
        ('open', 'Open'),
        ('closed', 'Closed'),
    ]
    survey = models.ForeignKey(Survey, on_delete=models.CASCADE)
    response_data = models.JSONField(encoder=DjangoJSONEncoder, help_text="Store the response data as JSON.")  # Use DjangoJSONEncoder to handle Decimal
    submitted_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.id}"

    def save(self, *args, **kwargs):
        # Convert all Decimal objects to strings
        def convert_decimal(obj):
            if isinstance(obj, Decimal):
                return str(obj)
            elif isinstance(obj, dict):
                return {k: convert_decimal(v) for k, v in obj.items()}
            elif isinstance(obj, list):
                return [convert_decimal(i) for i in obj]
            return obj

        self.response_data = convert_decimal(self.response_data)
        super(Answer, self).save(*args, **kwargs)

class QuestionAnswer(models.Model):
    STATUS_CHOICES = [
        ('open', 'Open'),
        ('closed', 'Closed'),
    ]

    survey = models.ForeignKey(Survey, on_delete=models.CASCADE)
    answer = models.ForeignKey(Answer, on_delete=models.CASCADE, related_name="question_answers")
    question_id = models.IntegerField(help_text="ID of the question from the survey JSON")
    question_text = models.TextField(help_text="Text of the question")
    response = models.TextField(help_text="The answer to the question")
    issue = models.TextField(blank=True, null=True, help_text="Description of the issue if the answer is 'No'")
    action_taken = models.TextField(blank=True, null=True, help_text="Action taken if the answer is 'No'")
    submitted_at = models.DateTimeField(auto_now_add=True)

    status_by_admin = models.CharField(max_length=20, choices=STATUS_CHOICES, default='open', help_text="Status set by admin")
    comment_by_admin = models.TextField(blank=True, null=True, help_text="Comment by admin")
    

    def __str__(self):
        return f"Answer to {self.question_text} (Survey: {self.survey.name})"