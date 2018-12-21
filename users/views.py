import random

from django.shortcuts import render, redirect
from django.contrib.auth.hashers import make_password
from django.contrib.auth.decorators import user_passes_test, login_required
from django.urls import reverse
from django.core.mail import send_mail
from django.conf import settings
from django.http import Http404
from django.contrib import messages
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

from itertools import chain

from users.forms import *
from courses.forms import AddCourseForm
from courses.models import *
from quiz.models import *
from assignment.models import *
# Create your views here.

def home(request):
    context = {
        'title': 'eLearning',
    }
    return render(request, 'home.html', context)

@login_required
def dashboard(request):
    if request.user.is_site_admin:
        return redirect(reverse('admin'))
    elif request.user.is_teacher:
        return redirect(reverse('teacher'))
    return redirect(reverse('student'))

@user_passes_test(lambda user: user.is_site_admin)
def admin(request):
    add_user_form = AddUser(request.POST or None)
    queryset = UserProfile.objects.all()

    search = request.GET.get('search')
    if search:
        queryset = queryset.filter(username__icontains=search)

    context = {
        'title': 'Admin',
        'add_user_form': add_user_form,
        'queryset': queryset,
    }
    
    if add_user_form.is_valid():
        instance = add_user_form.save(commit=False)
        passwd = add_user_form.cleaned_data.get('password')
        #hash password before save to dabatase
        instance.password = make_password(password=passwd,
                                            salt='salt',)
        instance.save()
        return redirect(reverse('dashboard') ) 

    return render(request,
                'users/sysadmin_dashboard.html',
                context)

@user_passes_test(lambda user: user.is_teacher)
def teacher(request):
    add_course_form = AddCourseForm(request.POST or None)
    queryset_course =  Course.objects.filter(user__username=request.user)

    path = request.path.split('/')[1]
    redirect_path = path
    path = path.title()

    context = {
        'title': 'Teacher',
        'add_course_form': add_course_form,
        'queryset_course': queryset_course,
        'path': path,
        'redirect_path': redirect_path
    }

    if add_course_form.is_valid():
        instance = add_course_form.save(commit=False)
        course_name = add_course_form.cleaned_data['name']
        course_category = add_course_form.cleaned_data['category']
        instance.user = request.user
        instance.save()
        return redirect(reverse('teacher'))
    
    return render(request,
                'users/teacher_dashboard.html',
                context)

@login_required
def student(request):
    queryset = Course.objects.filter(students=request.user)
    context = {
        'queryset': queryset,
        'title': request.user,
    }
    return render(request,
                'users/student_dashboard.html',
                context)

@login_required
def course_homepage(request, course_name):
    chapter_list = Chapter.objects.filter(course__name=course_name)

    if chapter_list:
        return redirect(reverse(student_course, kwargs={
            'course_name': course_name,
            'slug': chapter_list[0].slug
        }))
    else:
        warning_message = 'Currently there are no chapters this course'
        messages.warning(request, warning_message)
        return redirect(reverse('courses', kwargs=None))

def get_current_score(student, chapter):
    student_take_quizzes = TakenQuiz.objects.filter(student=student, quiz__chapter=chapter)
    number_quiz = student_take_quizzes.count()
    score = 0.0
    for q in student_take_quizzes:
        score += q.score
    try:
        average_score = round(score / number_quiz, 2)
    except ZeroDivisionError:
        average_score = 0 
    return average_score

def check_average_quiz_score(average_score):
    if average_score >= 5.0:
        return True
    return False

@login_required
def student_course(request, course_name, slug=None):
    course = Course.objects.get(name=course_name)
    # shuffle all course then get first 5 course
    all_course = list(Course.objects.all().exclude(name=course_name, category__name=course.category.name))
    random.shuffle(all_course)
    chapter_list = Chapter.objects.filter(course=course)
    chapter = Chapter.objects.get(course__name=course_name, slug=slug)
    text = TextBlock.objects.filter(text_block_fk=chapter)
    videos = YTLink.objects.filter(yt_link_fk=chapter)
    files = FileUpload.objects.filter(file_fk=chapter)
    user = request.user
    quizzes = Quiz.objects.filter(chapter__slug=slug)
    
    average_score = get_current_score(request.user, chapter)
    check_is_valid_score = check_average_quiz_score(average_score=average_score)
    try:
        assignment = Assignment.objects.get(chapter__slug=slug)
    except Assignment.DoesNotExist:
        warning_message = "Your average quiz's score have to reach more than 50.0 to access the Assigments"
        assignment = None
    
    #check whether user has taken assignment or not?
    isTaken = False
    isAssignemntExist = TakenAssignment.objects.filter(student=request.user, assignment=assignment).exists()
    if assignment and check_is_valid_score:
        if isAssignemntExist:
            isTaken = True
    print(isTaken)

    if user in course.students.all() or user.is_teacher or user.is_site_admin or course.for_everybody:
        context = {
            'course_name': course_name,
            'chapter_list': chapter_list,
            'chapter_name': chapter.name,
            'slug': chapter.slug,
            'text': text,
            'files': files,
            'videos': videos,
            'title': course_name + ' : ' + chapter.name,
            'random_course': all_course[:6],
            'quizzes': quizzes,
            'assignment': assignment,
            'isTaken': isTaken,
            'current_quiz_score': average_score
        }
        return render(request,
                    'users/student_courses.html',
                    context)
    else:
        raise Http404


def update_user(request, username):
    user = UserProfile.objects.get(username=username)
    user_info = {
        'username': user.username,
        'email': user.email
    }
    if user.is_site_admin:
        update_user_form = EditUserByAdmin(initial=user_info, instance=user)
    else:
        update_user_form = EditUserByUser(initial=user_info, instance=user)

    path = request.path.split('/')[1]
    redirect_path = path
    path = path.title()

    context = {
        'title': 'Edit',
        'update_user_form': update_user_form,
        'path': path,
        'redirect_path': redirect_path,
        'current_user': user
    }

    if request.POST:
        user_form = EditUserByAdmin(request.POST, instance=user)

        if user_form.is_valid():
            instance = user_form.save(commit=False)
            passwd = user_form.cleaned_data['password']

            if passwd:
                instance.password = make_password(password=passwd,
                                                salt='salt')
            instance.save()
            return redirect(reverse('dashboard'))

    return render(request,
                'users/edit_user.html',
                context)

@user_passes_test(lambda user: user.is_site_admin)
def delete_user(request, username):
    instance = UserProfile.objects.get(username=username)
    instance.delete()
    return redirect(reverse('dashboard'))
