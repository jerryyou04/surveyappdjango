# Generated by Django 4.2.16 on 2024-12-06 17:52

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('surveyapp', '0003_questionanswer_action_taken_questionanswer_issue'),
    ]

    operations = [
        migrations.AddField(
            model_name='survey',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
    ]
