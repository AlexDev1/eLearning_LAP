# Generated by Django 2.1.2 on 2018-11-27 04:31

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('quiz', '0007_auto_20181127_1129'),
    ]

    operations = [
        migrations.AlterField(
            model_name='question',
            name='number_of_answer',
            field=models.IntegerField(default=0, validators=[django.core.validators.MaxValueValidator(5), django.core.validators.MinValueValidator(3)]),
        ),
    ]
