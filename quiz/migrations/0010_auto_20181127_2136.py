# Generated by Django 2.1.2 on 2018-11-27 14:36

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('quiz', '0009_auto_20181127_2015'),
    ]

    operations = [
        migrations.CreateModel(
            name='TakenQuiz',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_date', models.DateTimeField(auto_now_add=True)),
                ('score', models.FloatField()),
            ],
        ),
        migrations.RemoveField(
            model_name='score',
            name='quiz',
        ),
        migrations.RemoveField(
            model_name='score',
            name='student',
        ),

        migrations.DeleteModel(
            name='Score',
        ),
        migrations.AddField(
            model_name='takenquiz',
            name='quiz',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='scores_in_quiz', to='quiz.Quiz'),
        ),
        migrations.AddField(
            model_name='takenquiz',
            name='student',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='student_has_score', to=settings.AUTH_USER_MODEL),
        ),
    ]
