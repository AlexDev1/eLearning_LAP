from django.shortcuts import render, redirect, reverse
from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import user_passes_test, login_required

from courses.models import Chapter
from users.models import UserProfile
from assignment.models import *


from assignment.forms import *
# Create your views here.

@user_passes_test(lambda user: user.is_teacher)
def create_assignment(request, chapter_slug=None):
    chapter = Chapter.objects.get(slug=chapter_slug)
    owner = request.user
    add_assignment_form = CreateAssignmentForm(request.POST or None)

    queryset_assignment = Assignment.objects.filter(chapter=chapter)
    path = request.path.split("/")[1]
    redirect_path = path
    path = path.title()
    context = {
        'title': 'Create Assignment',
        'chapter': chapter,
        'add_assignment_form': add_assignment_form,
        'queryset_assignment': queryset_assignment,
        'path': path,
        'redirect_path': redirect_path
    }

    if add_assignment_form.is_valid():
        instance = add_assignment_form.save(commit=False)
        instance.owner = owner
        instance.chapter = chapter
        instance.save()
        return redirect(reverse('create_assignment', kwargs={
            'chapter_slug': chapter_slug
        })) 
    return render(request,
                'assignment/create.html',
                context)

@user_passes_test(lambda  user: user.is_teacher)
def update_assignment(request, assignment_id=None):
    assignment = Assignment.objects.get(id=assignment_id)
    edit_assignment_form = CreateAssignmentForm(request.POST or None, instance=assignment)
    path = request.path.split("/")[1]
    redirect_path = path
    path = path.title()

    context = {
        'title': 'Edit',
        'form': edit_assignment_form,
        'path': path,
        'assignment': assignment,
        'redirect_path': redirect_path
    }
    if edit_assignment_form.is_valid():
        edit_assignment_form.save()
        return redirect(reverse('create_assignment', kwargs={
            'chapter_slug': assignment.chapter.slug
        }))

    return render(request,
                'courses/edit.html',
                context)

@user_passes_test(lambda user: user.is_teacher)
def assignment(request, assignment_id=None):
    assignment = Assignment.objects.get(id=assignment_id)
    students = assignment.students.all()

    taken_assignments = TakenAssignment.objects.filter(assignment=assignment)
    path = request.path.split("/")[1]
    redirect_path = path
    path = path.title()
    context = {
        'tite':assignment.name,
        'assignment': assignment,
        'taken_assignments': taken_assignments,
        'path': path,
        'redirect_path': redirect_path,
    }


    return render(request,
                'assignment/assignment.html',
                context)

@login_required
def take_assignment(request, assignment_id=None):
    assignment = Assignment.objects.get(id=assignment_id)
    student = request.user
    answer_form = TakeAssignmentForm()
    path = request.path.split("/")[1]
    redirect_path = path
    path = path.title()
    context = {
        'title': 'Take ' + assignment.name,
        'assignment': assignment,
        'answer_form': answer_form,
        'path': path,
        'redirect_path': redirect_path
    }
    if request.method == 'POST':
        answer_form = TakeAssignmentForm(data=request.POST)
        if answer_form.is_valid():
            answer = answer_form.cleaned_data['answer']
            assignment.answer = answer
            assignment.save()

            exist_instance =  TakenAssignment.objects.filter(student=student, assignment=assignment)
            if exist_instance.count() > 0:
                exist_instance.delete()
            take_assignment_object = TakenAssignment(student=student, assignment=assignment)
            take_assignment_object.save()
            return redirect(reverse('student_course', kwargs={
                'course_name': assignment.chapter.course.name,
                'slug': assignment.chapter.slug
            }))
    return render(request,
                'assignment/take_assignment.html',
                context)

@user_passes_test(lambda user: user.is_teacher)
def give_score_to_assignment(request, take_assignment_id=None):
    taken_assignment_instance = TakenAssignment.objects.get(id=take_assignment_id)
    assignment = taken_assignment_instance.assignment
    give_score_form = GiveScoreForm(request.POST or None)
    path = request.path.split("/")[1]
    redirect_path = path
    path = path.title()
    context = {
        'title': 'Give a result',
        'taken_assignment_instance': taken_assignment_instance,
        'give_score_form' :give_score_form,
        'path': path,
        'redirect_path': redirect_path
    }
    
    if give_score_form.is_valid():
        score = give_score_form.cleaned_data['score']
        taken_assignment_instance.score = score
        taken_assignment_instance.save()
        return redirect(reverse('assignment', kwargs={
            'assignment_id': taken_assignment_instance.assignment.id
        }))

    return render(request,
                'assignment/give_result.html',
                context)

@login_required
def check_result(request, assignment_id=None):
    assignment = Assignment.objects.get(id=assignment_id)
    your_taken_assignment = TakenAssignment.objects.get(student=request.user, assignment=assignment)
    taken_list = TakenAssignment.objects.filter(assignment=assignment)
    path = request.path.split("/")[1]
    redirect_path = path
    path = path.title()

    print(assignment.question)
    context = {
        'title': 'Result',
        'assignment': assignment,
        'your_taken_assignment': your_taken_assignment,
        'taken_list': taken_list,
        'path': path,
        'redirect_path': redirect_path
    }
    return render(request,
                'assignment/result.html',
                context)

@user_passes_test(lambda user: user.is_teacher)
def delete_assignment(request, assignment_id):
    assignment = Assignment.objects.get(id=assignment_id)
    assignment.delete()
    return HttpResponseRedirect(reverse('create_assignment', kwargs={
        'chapter_slug': assignment.chapter.slug
    }))