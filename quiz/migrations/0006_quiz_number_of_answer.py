# Generated by Django 2.1.2 on 2018-11-27 04:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('quiz', '0005_auto_20181127_1040'),
    ]

    operations = [
        migrations.AddField(
            model_name='quiz',
            name='number_of_answer',
            field=models.SmallIntegerField(default=0, max_length=5),
            preserve_default=False,
        ),
    ]
