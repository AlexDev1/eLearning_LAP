from __future__ import unicode_literals

from django.db import models

# Create your models here.

class Topic(models.Model):
    subjects = models.CharField(max_length=200)
    topic_message =  models.TextField(max_length=1000)
    author = models.CharField(max_length=30)
    comment_count = models.IntegerField(default=1)
    stamp_created = models.DateTimeField(auto_now_add=True)
    stamp_updated = models.DateTimeField(auto_now_add=True)
    slug = models.SlugField(unique=True)

    class Meta:
        get_latest_by = 'id'

class Comment(models.Model):
    message = models.TextField()
    author = models.CharField(max_length=30)
    date_created = models.DateTimeField(auto_now_add=True)
    comment_fk = models.ForeignKey(Topic,
                                    on_delete=models.CASCADE)