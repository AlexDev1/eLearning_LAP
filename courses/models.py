from __future__ import unicode_literals

import os

from django.db import models
from django.urls import reverse
from django.db.models.signals import pre_save
from django.utils.text import slugify
from django.dispatch import receiver

from users.models import UserProfile
# Create your models here.

def get_first_user():
    return UserProfile.objects.first()

class Category(models.Model):
    name = models.CharField(max_length=100)
    created_date = models.DateTimeField(auto_now_add=True)
    slug = models.SlugField(unique=True)

    def __unicode__(self):
        return self.name
    
    def slug_default(self):
        slug = create_slug(new_slug=self.name)
        return slug
    
    def __str__(self):
        return self.name



class Course(models.Model):
    name = models.CharField(unique=True, max_length=200)
    created_date = models.DateTimeField(auto_now_add=True)

    #author's course aka teacher
    user = models.ForeignKey(UserProfile, 
                            default=get_first_user().id,
                            on_delete=models.CASCADE)
    # student in course
    students = models.ManyToManyField(UserProfile, 
                                        related_name='students_to_course') 
    # category
    category = models.ForeignKey(Category,
                                on_delete=models.CASCADE,
                                related_name='course_in_category')
    for_everybody = models.BooleanField(default=True)

    def __unicode__(self):
        return self.name
    
    def __str__(self):
        return self.name

class Chapter(models.Model):
    name = models.CharField(max_length=100)
    created_date = models.DateTimeField(auto_now_add=True)
    course = models.ForeignKey(
        Course,
        on_delete=models.CASCADE,
        default=1
    )
    slug = models.SlugField(unique=True)

    def __unicode__(self):
        return self.name
    
    def get_absolute_url(self):
        return reverse('chapter', kwargs={
            'course_name': self.course,
            'slug': self.slug
        })
    
    def slug_default(self):
        slug = create_slug(new_slug=self.name)
        return slug
    
    def __str__(self):
        return self.name

def create_slug(instance=None, new_slug=None):
    slug = slugify(instance.name)
    if new_slug is not None:
        slug = new_slug
    
    qs = Chapter.objects.filter(slug=slug).order_by('-id')
    exists = qs.exists()

    if exists:
        new_slug = "%s-%s" % (slug, qs.first().id)
        return create_slug(instance, new_slug=new_slug)
    return slug

def pre_save_receiver(sender, instance, *args, **kwargs):
    if not instance.slug:
        instance.slug = create_slug(instance)
pre_save.connect(pre_save_receiver, sender=Chapter)
pre_save.connect(pre_save_receiver, sender=Category)

class TextBlock(models.Model):
    lesson = models.TextField()
    text_block_fk =  models.ForeignKey(Chapter,
                                        on_delete=models.CASCADE,
                                        default=1)
    created_date = models.DateTimeField(auto_now_add=True)

class YTLink(models.Model):
    link = models.URLField(max_length=200)
    yt_link_fk = models.ForeignKey(Chapter, 
                                    on_delete=models.CASCADE,
                                    default=1)
    created_date = models.DateTimeField(auto_now_add=True)

class FileUpload(models.Model):
    file = models.FileField(null=False, blank=False, default='')
    file_fk = models.ForeignKey(Chapter,
                                on_delete=models.CASCADE,
                                default=1)
    created_date = models.DateTimeField(auto_now_add=True)

@receiver(models.signals.post_delete, sender=FileUpload)
def auto_delete_file_on_delete(sender, instance, **kwargs):
    if instance.file:
        if os.path.isfile(instance.file.path):
            os.remove(instance.file.path)