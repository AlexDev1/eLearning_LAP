import random

from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import user_passes_test, login_required
from django.contrib import messages
from django.db import transaction

from quiz.models import *
from courses.models import *
from users.models import *

from quiz.forms import *

# Create your views here.

@login_required
@user_passes_test(lambda user: user.is_teacher)
def create_quiz(request, chapter_slug=None):
    chapter = Chapter.objects.get(slug=chapter_slug)
    add_quiz_form = CreateQuizForm(request.POST or None)

    queryset_quiz = Quiz.objects.filter(chapter__slug=chapter_slug)
    path = request.path.split("/")[1]
    redirect_path = path
    path = path.title()
    context = {
        'title': 'Create Quiz',
        'course_name': chapter.course.name,
        'chapter_name': chapter.name,
        'chapter_slug': chapter_slug,
        'slug': chapter.slug,
        'add_quiz_form': add_quiz_form,
        'queryset_quiz': queryset_quiz,
        'path': path,
        'redirect_path': redirect_path
    }
    if add_quiz_form.is_valid():
        instance = add_quiz_form.save(commit=False)
        instance.chapter = chapter
        instance.owner = request.user
        instance.save()
        return redirect(reverse('create_quiz', kwargs={
            'chapter_slug': chapter_slug
        }))
    
    return render(request,
                    'quiz/create.html',
                    context)

@login_required
@user_passes_test(lambda user: user.is_teacher)
def quiz(request, chapter_slug=None, quiz_slug=None):
    quiz = Quiz.objects.get(chapter__slug=chapter_slug, slug=quiz_slug)
    add_question_form = CreateQuestionForm(request.POST or None)

    queryset_question = Question.objects.filter(quiz=quiz)
    path = request.path.split("/")[1]
    redirect_path = path
    path = path.title()
    context = {
        'title': quiz.name,
        'quiz_slug': quiz_slug,
        'chapter_slug': quiz.chapter.slug,
        'add_question_form': add_question_form,
        'queryset_question': queryset_question,
        'path': path,
        'redirect_path': redirect_path
    }

    if add_question_form.is_valid():
        instance = add_question_form.save(commit=False)
        instance.quiz = quiz
        instance.save()
        return redirect(reverse('quiz', kwargs={
            'chapter_slug': chapter_slug,
            'quiz_slug': quiz_slug
        }))
    return render(request,
                'quiz/quiz.html',
                context)

@login_required
@user_passes_test(lambda user: user.is_teacher)
def question(request, question_id=None):
    quest = Question.objects.get(pk=question_id)
    add_answer_form = CreateAnswerForm(request.POST or None)

    queryset_answer = Answer.objects.filter(question__pk=question_id)
    path = request.path.split("/")[1]
    redirect_path = path
    path = path.title()
    context = {
        'title': quest.text,
        'chapter_slug': quest.quiz.chapter.slug,
        'quiz_slug': quest.quiz.slug,
        'id': quest.id,
        'add_answer_form': add_answer_form,
        'queryset_answer': queryset_answer,
        'quest': quest,
        'path': path,
        'redirect_path': redirect_path
    }
    if queryset_answer.count() < quest.number_of_answer:
        if add_answer_form.is_valid():
            instance = add_answer_form.save(commit=False)
            instance.question = quest
            instance.save()
            return redirect(reverse('question', kwargs={
                'question_id': question_id
            }))

    return render(request,
                'quiz/question.html',
                context)


@login_required
def take_quiz(request, chapter_slug=None, quiz_slug=None):
    quiz = Quiz.objects.get(chapter__slug=chapter_slug, slug=quiz_slug)
    student = request.user
    total_questions = quiz.questions.count()

    unanswer_questions = get_unanswer_question(student, quiz)
    total_unanswer_questions = unanswer_questions.count()
    if total_unanswer_questions == 0:
        return redirect(reverse('quiz_result', kwargs={
                    'chapter_slug': chapter_slug,
                    'quiz_slug': quiz_slug
        }))

    path = request.path.split("/")[1]
    redirect_path = path
    path = path.title()

    progress = 100 - round(((total_unanswer_questions - 1) / total_questions) * 100 )
    question = unanswer_questions.first()
    
    form_question = QuestionAnswerForm(question=question)

    context = {
        'title': quiz.name,
        'form_question': form_question,
        'total_questions': total_questions,
        'path': path,
        'redirect_path': redirect_path,
        'quiz': quiz,
        'question': question,
        'progress': progress,
        'total_unanswer_questions': total_unanswer_questions,
        'chapter_slug': chapter_slug,
        'quiz_slug': quiz_slug,
        'course_name': quiz.chapter.course.name,
        'chapter_name': quiz.chapter.name
    }


    if request.method == 'POST':
        form_question = QuestionAnswerForm(question=question,data=request.POST)
        if form_question.is_valid():
            student_answer = form_question.save(commit=False)
            student_answer.student = student
            student_answer.save()

            if get_unanswer_question(student, quiz).exists():
                return redirect(reverse('take_quiz', kwargs={
                        'chapter_slug': chapter_slug,
                        'quiz_slug': quiz_slug
                    }))
            else:
                correct_answers = student.quiz_answers.filter(answer__question__quiz=quiz,
                                                                answer__is_correct=True).count()
                score = round((correct_answers / total_questions) * 100.0, 2)      
                exist_instance = TakenQuiz.objects.filter(quiz=quiz, student=student)
                if exist_instance.count() > 0:
                    exist_instance.delete()
                taken_quiz_instance = TakenQuiz(quiz=quiz, student=student, score=score)  
                taken_quiz_instance.save()
                return redirect(reverse('quiz_result', kwargs={
                    'chapter_slug': chapter_slug,
                    'quiz_slug': quiz_slug
                }))                                 
    return render(request,
                'quiz/taken_quiz.html',
                context)


@login_required
def get_result(request, chapter_slug=None, quiz_slug=None, ):
    quiz = Quiz.objects.get(chapter__slug=chapter_slug, slug=quiz_slug)
    queryset_taken_quizzes = quiz.taken_quizzes.all()
    questions = quiz.questions.all()
    correct_answers = []
    current_student = request.user
    taken_answer = current_student.quiz_answers.filter(answer__question__quiz=quiz)
    for question in questions:
        correct_answers.append({
            'question': question.text,
            'correct_answer': Answer.objects.get(question=question, is_correct=True).text
        })
    current_log = []
    for answer in taken_answer:
        current_log.append(answer)

    #clear answered 
    taken_answer.delete()
    context = {
        'title': "Result",
        'queryset_taken_quizzes': queryset_taken_quizzes,
        'chapter_name': quiz.chapter.name,
        'course_name': quiz.chapter.course.name,
        'chapter_slug': chapter_slug,
        'quiz': quiz,
        'correct_answers': correct_answers,
        'taken_answer': current_log,
        'student': current_student
    }
    return render(request,
                'quiz/result.html',
                context)

def clear_history(current_student, quiz):
    taken_answer = current_student.quiz_answers.filter(answer__question__quiz=quiz)
    print(taken_answer)
    taken_answer.delete()

def get_unanswer_question(student, quiz):
    answered_questions = student.quiz_answers \
                        .filter(answer__question__quiz=quiz)\
                        .values_list('answer__question__pk', flat=True)
    questions = quiz.questions.exclude(pk__in=answered_questions).order_by('text')
    return questions

@user_passes_test(lambda user:user.is_teacher)
def update_quiz(request, chapter_slug=None, quiz_slug=None):
    quiz = Quiz.objects.get(slug=quiz_slug)
    update_quiz_form = CreateQuizForm(request.POST or None, instance=quiz)

    path = request.path.split("/")[1]
    redirect_path = path
    path = path.title()

    context = {
        'title':  quiz.name ,
        'form': update_quiz_form,
        'path': path,
        'redirect_path': redirect_path,
        'quiz_slug': quiz_slug,
        'chapter_slug': chapter_slug,
        'chapter_name': quiz.chapter.name
    }

    if update_quiz_form.is_valid():
        update_quiz_form.save()
        return redirect(reverse('create_quiz', kwargs={
            'chapter_slug': chapter_slug
        }))

    return render(request,
                'courses/edit.html',
                context)

@user_passes_test(lambda user: user.is_teacher)
def delete_quiz(request, chapter_slug=None, quiz_slug=None):
    quiz = Quiz.objects.get(slug=quiz_slug)
    quiz.delete()
    return HttpResponseRedirect(reverse('create_quiz', kwargs={
        'chapter_slug': chapter_slug
    }))

@user_passes_test(lambda user:user.is_teacher)
def update_question(request, question_id=None):
    question = Question.objects.get(pk=question_id)
    update_question_form = CreateQuestionForm(request.POST or None, instance=question)

    path = request.path.split("/")[1]
    redirect_path = path
    path = path.title()

    context = {
        'title':  question.text,
        'form': update_question_form,
        'path': path,
        'redirect_path': redirect_path,
        'quiz_slug': question.quiz.slug,
        'chapter_slug': question.quiz.chapter.slug,
        'quiz_name': question.quiz.name,
        'question_id': question_id
    }

    if update_question_form.is_valid():
        update_question_form.save()
        return redirect(reverse('quiz', kwargs={
            'chapter_slug': question.quiz.chapter.slug,
            'quiz_slug': question.quiz.slug
        }))

    return render(request,
                'courses/edit.html',
                context)

@user_passes_test(lambda user: user.is_teacher)
def delete_question(request, question_id=None):
    question = Question.objects.get(id=question_id)
    question.delete()
    return HttpResponseRedirect(reverse('quiz', kwargs={
            'chapter_slug': question.quiz.chapter.slug,
            'quiz_slug': question.quiz.slug
        }))


@user_passes_test(lambda user:user.is_teacher)
def update_answer(request, answer_id=None):
    answer = Answer.objects.get(pk=answer_id)
    update_answer_form = CreateAnswerForm(request.POST or None, instance=answer)

    path = request.path.split("/")[1]
    redirect_path = path
    path = path.title()

    context = {
        'title':  answer.text,
        'form': update_answer_form,
        'path': path,
        'redirect_path': redirect_path,
        'question_id': answer.question.id,
        'question_text': answer.question.text,
        'answer_id': answer_id
    }

    if update_answer_form.is_valid():
        update_answer_form.save()
        return redirect(reverse('question', kwargs={
            'question_id': answer.question.id
        }))

    return render(request,
                'courses/edit.html',
                context)

@user_passes_test(lambda user: user.is_teacher)
def delete_answer(request, answer_id=None):
    answer = Answer.objects.get(id=answer_id)
    answer.delete()
    return HttpResponseRedirect(reverse('question', kwargs={
            'question_id': answer.question.id
        }))
