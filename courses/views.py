from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import user_passes_test, login_required
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

from courses.models import Course
from users.models import UserProfile
from courses.forms import *
from courses.util import *
from quiz.models import Quiz
from quiz.forms import CreateQuizForm
# Create your views here.

# Manage course


@login_required
def courses(request):


    if request.user.is_teacher or request.user.is_site_admin:
        courses =  Course.objects.all()
    else:
        courses = Course.objects.filter(for_everybody=True)

    paginator = Paginator(courses, 8)
    page = request.GET.get('page')
    try:
        queryset = paginator.page(page)
    except PageNotAnInteger:
        queryset = paginator.page(1)
    except EmptyPage:
        queryset = paginator.page(paginator.num_pages)


    return render(request,
                'users/course.html',
                context=get_context(queryset))

@login_required
def courses_by_teacher(request, teacher_name=None):
    if not teacher_name:
        return redirect(reverse('courses'))
    courses = Course.objects.filter(user__username=teacher_name, for_everybody=True)
    return render(request,
                'users/course.html',
                context=get_context(courses, filter=teacher_name))

@login_required
def courses_by_category(request, category_slug=None):
    if not category_slug:
        return redirect(reverse('courses'))

    courses = Course.objects.filter(category__slug=category_slug, for_everybody=True)
    category_name = Category.objects.get(slug=category_slug).name
    return render(request,
                'users/course.html',
                context=get_context(courses, filter=category_name))

@user_passes_test(lambda user: user.is_teacher)
def course(request, course_name=None):
    # display course and create chapter when teacher navigate to teacher's course page
    add_chapter_form = AddChapterForm(request.POST or None, prefix='ch')
    queryset_chapter =  Chapter.objects.filter(course__name=course_name)

    course = Course.objects.get(name=course_name)
    context = {
        'title': course_name,
        'add_chapter_form': add_chapter_form,
        'queryset_chapter': queryset_chapter,

        'course_name': course_name,
        'path': 'Dashboard',
        'redirect_path': 'dashboard'
    }
    if request.POST:
        add_chapter_form = AddChapterForm(request.POST or None, prefix='ch')
        if add_chapter_form.is_valid():
            instance = add_chapter_form.save(commit=False)
            instance.course = course
            instance.save()
            return redirect(reverse('teacher_course', kwargs={
                'course_name': course_name
            }))
    
        add_quiz_form = CreateQuizForm(request.POST or None, prefix='q')
        if add_quiz_form.is_valid():
            quiz = add_quiz_form.save(commit=False)
            quiz.course = course
            quiz.save()
            return redirect(reverse('teacher_course', kwargs={
                'course_name': course_name
            }))

    return render(request,
                'courses/course.html',
                context)

@user_passes_test(lambda user: user.is_teacher)
def update_course(request, course_name=None):
    old_course = Course.objects.get(name=course_name)

    update_course_form = EditCourseForm(request.POST or None, instance=old_course)
    path = request.path.split('/')[1]
    redirect_path = path
    path = path.title()
    
    context = {
        'title': "Edit",
        'form': update_course_form,
        'path': path,
        'redirect_path': redirect_path
    }

    if update_course_form.is_valid():
        update_course_form.save()
        return redirect(reverse('dashboard'))
    return render(request,
                'courses/edit.html',
                context)

@user_passes_test(lambda user: user.is_teacher)
def delete_course(request, course_name=None):
    instance = Course.objects.get(name=course_name)
    instance.delete()
    return HttpResponseRedirect(reverse('dashboard'))

# Manage chapter 

@user_passes_test(lambda user: user.is_teacher)
def chapter(request, course_name=None, slug=None):
    chapter = Chapter.objects.get(course__name=course_name, slug=slug)

    add_link_form = AddLinkForm(request.POST or None)
    add_txt_form = AddTextForm(request.POST or None)
    file_upload_form = FileUploadForm(request.POST or None, request.FILES or None)

    queryset_txt_block = TextBlock.objects.filter(text_block_fk__id=chapter.id)
    queryset_yt_link = YTLink.objects.filter(yt_link_fk__id=chapter.id)
    queryset_files = FileUpload.objects.filter(file_fk__id=chapter.id)

    
    context = {
        'title': chapter.name,
        'course_name': course_name,
        'chapter_slug': chapter.slug,
        'slug': slug,
        'add_link_form': add_link_form,
        'add_txt_form': add_txt_form,
        'file_upload_form': file_upload_form,
        'queryset_txt_block': queryset_txt_block,
        'queryset_yt_link': queryset_yt_link,
        'queryset_files': queryset_files,
        'path': 'Dashboard',
        'redirect_path': 'dashboard'
    }

    if add_link_form.is_valid() and 'add_link' in request.POST:
        instance = add_link_form.save(commit=False)
        instance.yt_link_fk = Chapter.objects.get(id=chapter.id)

        key = add_link_form.cleaned_data['link']

        if 'embed' not in key and 'youtube' in key:
            key = key.split('=')[1]
            instance.link = 'https://www.youtube.com/embed/' + key

        instance.save()
        return redirect(reverse('chapter', kwargs={
            'course_name': course_name,
            'slug': slug
        }))
    
    if add_txt_form.is_valid() and 'add_text' in request.POST:
        instance = add_txt_form.save(commit=False)
        instance.text_block_fk = Chapter.objects.get(id=chapter.id)
        instance.save()
        return redirect(reverse('chapter', kwargs={
            'course_name': course_name,
            'slug': slug
        }))
    
    if file_upload_form.is_valid() and 'add_file' in request.POST:
        instance = file_upload_form.save(commit=False)
        instance.file_fk = Chapter.objects.get(id=chapter.id)
        instance.save()
        return redirect(reverse('chapter', kwargs={
            'course_name': course_name,
            'slug': slug
        }))
    
    return render(request,
                'courses/chapter.html',
                context)

@user_passes_test(lambda user: user.is_teacher)
def update_chapter(request, course_name=None, slug=None):
    old_chapter = Chapter.objects.get(slug=slug)

    update_chapter_form = EditChapterForm(request.POST or None, instance=old_chapter)

    path = request.path.split('/')[1]
    redirect_path = path
    path = path.title()

    context = {
        'title': "Edit",
        'form': update_chapter_form,
        'path': path,
        'redirect_path': redirect_path
    }

    if update_chapter_form.is_valid():
        update_chapter_form.save()
        return redirect(reverse('teacher_course', kwargs={
            'course_name': course_name
        }))

    return render(request,
                'courses/edit.html',
                context)

@user_passes_test(lambda user: user.is_teacher)
def delete_chapter(request, course_name=None, slug=None):
    instance = Chapter.objects.get( slug=slug)
    instance.delete()
    return HttpResponseRedirect(reverse('teacher_course', kwargs={
        'course_name': course_name
    }))

# Manage videos, text and file 

@user_passes_test(lambda user: user.is_teacher)
def update_text_block(request, course_name=None, slug=None, txt_id=None):
    old_text = TextBlock.objects.get(id=txt_id)
    update_text_form = EditTextForm(request.POST or None, instance=old_text)

    context = {
        'title': 'Edit',
        'course_name': course_name,
        'txt_id': txt_id,
        'form': update_text_form,
        'path': 'Dashboard',
        'redirect_path': 'dashboard'
    }

    if update_text_form.is_valid():
        update_text_form.save()
        return redirect(reverse('chapter', kwargs={
            'course_name': course_name,
            'slug': slug
        }))
    
    return render(request,
                'courses/edit.html',
                context)

@user_passes_test(lambda user: user.is_teacher)
def delete_text_block(request, course_name=None, slug=None, txt_id=None):
    instance = TextBlock.objects.get(id=txt_id)
    instance.delete()
    return HttpResponseRedirect(reverse('chapter', kwargs={
        'course_name': course_name,
        'slug': slug
    }))

@user_passes_test(lambda user: user.is_teacher)
def update_yt_link(request, course_name=None, slug=None, yt_id=None):
    old_link = YTLink.objects.get(id=yt_id)
    update_yt_link = EditLinkForm(request.POST or None, instance=old_link)

    context = {
        'title': 'Edit',
        'course_name': course_name,
        'yt_id': yt_id,
        'form': update_yt_link,
        'path': 'Dashboard',
        'redirect_path': 'dashboard'
    }

    if update_yt_link.is_valid():
        update_yt_link.save()
        return redirect(reverse('chapter', kwargs={
            'course_name': course_name,
            'slug': slug
        }))
    
    return render(request,
                'courses/edit.html',
                context)

@user_passes_test(lambda user: user.is_teacher)
def delete_yt_link(request, course_name=None, slug=None, yt_id=None):
    instance = YTLink.objects.get(id=yt_id)
    instance.delete()
    return HttpResponseRedirect(reverse('chapter', kwargs={
        'course_name': course_name,
        'slug': slug
    }))

@user_passes_test(lambda user: user.is_teacher)
def delete_file(request, course_name=None, slug=None, file_id=None):
    instance = FileUpload.objects.get(id=file_id)
    instance.delete()
    return HttpResponseRedirect(reverse('chapter', kwargs={
        'course_name': course_name,
        'slug': slug
    }))

# Manage student in course
@user_passes_test(lambda user: user.is_teacher)
def list_students_in_course(request, course_name=None):
    course = Course.objects.get(name=course_name)
    students_in_course = UserProfile.objects.filter(students_to_course=course)
    exclude_students = UserProfile.objects.exclude(students_to_course=course).filter(
                        is_teacher=False).filter(is_site_admin=False)
    
    query_first = request.GET.get('q1')
    if query_first:
        exclude_students = exclude_students.filter(username__icontains=query_first)
    query_second = request.GET.get('q2')
    if query_second:
        students_in_course = students_in_course.filter(username__icontains=query_second)
    
    path = request.path.split('/')[1]
    redirect_path = path
    path = path.title()

    context = {
        'title': 'Edit students in course' + course_name,
        'exclude_students': exclude_students,
        'students_in_course': students_in_course,
        'course_name': course_name,
        'path': path,
        'redirect_path': redirect
    }
    return render(request,
                'courses/add_students.html',
                context)

@user_passes_test(lambda user: user.is_teacher)
def add_student(request,student_id, course_name=None, ):
    student = UserProfile.objects.get(id=student_id)
    course = Course.objects.get(name=course_name)
    course.students.add(student)
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

@user_passes_test(lambda user: user.is_teacher)
def delete_student(request, student_id, course_name=None):
    student = UserProfile.objects.get(id=student_id)
    course = Course.objects.get(name=course_name)
    course.students.remove(student)
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))