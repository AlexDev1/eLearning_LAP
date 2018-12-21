from django.shortcuts import render, redirect
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.utils.text import slugify
from django.utils import timezone

from .models import *
from .forms import *
# Create your views here.

@login_required
def forum(request): 
    topics = Topic.objects.all().order_by('-stamp_updated')
    add_new_topic = AddTopicForm(request.POST or None)

    path = request.path.split('/')[1]
    redirect_path = path
    path = path.title()

    search = request.GET.get('search')
    if search:
        topics = topics.filter(subjects__startswith=search)
    
    paginator = Paginator(topics, 10)
    
    if add_new_topic.is_valid():
        instance = add_new_topic.save(commit=False)
        instance.author = request.user
        slug = slugify(instance.subjects)
        exists = Topic.objects.filter(slug=slug).exists()
        last_topic = Topic.objects.order_by('id').last()
        if last_topic is None:
            max_id = 0
        else:
            max_id = last_topic.id 
        max_id += 1

        # if slug exists then append slug by id
        if exists:
            slug = "%s-%s" % (slug, max_id)
        instance.slug = slug
        instance.save()
    
    page = request.GET.get('page')
    try:
        queryset = paginator.page(page)
    except PageNotAnInteger:
        #if page is not an integer, deliver first page
        queryset = paginator.page(1)
    except EmptyPage:
        # if page is out of range (e.g: 9999), deliver last page of result
        queryset = paginator.page(paginator.num_pages)
    
    context = {
        'title': 'Forum',
        'add_new_topic': add_new_topic,
        'topics': queryset,
        'path': path,
        'redirect_path': redirect_path,
    }
    return render(request,
                'forum/forum.html',
                context)

@login_required
def topic(request, slug=None):
    add_new_comment = AddNewComment(request.POST or None)
    topic_id  = Topic.objects.get(slug=slug)
    comments =  Comment.objects.filter(comment_fk=topic_id)

    path = request.path.split('/')[1]
    redirect_path = path
    path = path.title()

    context = {
        'title': Topic.objects.get(slug=slug).subjects,
        'add_new_comment': add_new_comment,
        'path': path,
        'redirect_path': redirect_path,
        'comments': comments,
        "first_comment": Topic.objects.get(slug=slug).topic_message,
        "first_comment_timestamp": Topic.objects.get(slug=slug).stamp_created,
        "first_comment_author": Topic.objects.get(slug=slug).author,
    }
    
    if add_new_comment.is_valid():
        instance = add_new_comment.save(commit=False)
        instance.author = request.user
        instance.comment_fk = Topic.objects.get(slug=slug)
        topic_obj = Topic.objects.get(slug=slug)
        topic_obj.comment_count += 1
        topic_obj.stamp_updated = timezone.now()
        topic_obj.save()
        instance.save()
        return redirect(reverse(topic, kwargs={'slug': slug}))
    
    return render(request,
                'forum/topic.html',
                context)