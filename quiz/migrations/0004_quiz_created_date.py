# Generated by Django 2.1.2 on 2018-11-27 03:21

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('quiz', '0003_remove_quiz_created_date'),
    ]

    operations = [
        migrations.AddField(
            model_name='quiz',
            name='created_date',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
    ]
