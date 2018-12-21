from django.conf.urls import url
from django.urls import path

from . import views as course_views
from users import views as user_views
from quiz import views as quiz_views
from assignment import views as assignment_views

urlpatterns = [
    url(r'^$', course_views.courses, name='courses'),
    url(r'^(?P<teacher_name>[\w ]+)/$', course_views.courses_by_teacher, name='courses_by_teacher'),
    url(r'index/(?P<category_slug>[\w-]+)/$', course_views.courses_by_category, name='courses_by_category'),
    #student url
    url(r'^student/(?P<course_name>[\w ]+)/$', 
        user_views.course_homepage, name='course_homepage'),
    url(r'^student/(?P<course_name>[\w ]+)/(?P<slug>[\w-]+)/$', 
        user_views.student_course, name='student_course' ),
    url(r'^student/(?P<course_name>[\w ]+)/quiz/(?P<quiz_slug>[\w-]+)/$',
        quiz_views.take_quiz, name='take_quiz'),
    
    # teacher manage course url
    url(r'^teacher/(?P<course_name>[\w ]+)/$', 
        course_views.course, name='teacher_course'),
    url(r'^teacher/(?P<course_name>[\w ]+)/edit/$', 
        course_views.update_course, name='edit_course'),
    url(r'^teacher/(?P<course_name>[\w ]+)/delete/$', 
        course_views.delete_course, name='delete_course'),


    # teacher manage student url
    url(r'^teacher/(?P<course_name>[\w ]+)/students/$', 
        course_views.list_students_in_course, name='list_students'),
    url(r'^teacher/(?P<course_name>[\w ]+)/students/(?P<student_id>[\d ]+)/delete/$',
        course_views.delete_student, name='delete_student'),
    url(r'^teacher/(?P<course_name>[\w ]+)/students/(?P<student_id>[\d ]+)/add/$',
        course_views.add_student, name='add_student'),

    # teacher manage chapter url
    url(r'^teacher/(?P<course_name>[\w ]+)/(?P<slug>[\w-]+)/$', 
        course_views.chapter, name='chapter'),
    url(r'^teacher/(?P<course_name>[\w ]+)/(?P<slug>[\w-]+)/edit/$', 
        course_views.update_chapter, name='edit_chapter'),
    url(r'^teacher/(?P<course_name>[\w ]+)/(?P<slug>[\w-]+)/delete/$', 
        course_views.delete_chapter, name='delete_chapter'),

    #teacher manage quiz url
    url(r'^teacher/(?P<chapter_slug>[\w-]+)/quiz/create/$',
        quiz_views.create_quiz, name='create_quiz'),
    url(r'^teacher/(?P<chapter_slug>[\w-]+)/quiz/(?P<quiz_slug>[\w-]+)/$',
        quiz_views.quiz, name='quiz'),
    url(r'^teacher/(?P<chapter_slug>[\w-]+)/do-quiz/(?P<quiz_slug>[\w-]+)/$',
        quiz_views.take_quiz, name='take_quiz'),
    url(r'^teacher/(?P<chapter_slug>[\w-]+)/result/(?P<quiz_slug>[\w-]+)/$',
        quiz_views.get_result, name='quiz_result'),
    url(r'^teacher/(?P<chapter_slug>[\w-]+)/(?P<quiz_slug>[\w-]+)/quiz/edit/$',
        quiz_views.update_quiz, name='edit_quiz'),
    url(r'^teacher/(?P<chapter_slug>[\w-]+)/(?P<quiz_slug>[\w-]+)/quiz/delete/$',
        quiz_views.delete_quiz, name='delete_quiz'),

    #teacher manage question of quiz url
    url(r'teacher/quiz/questions/(?P<question_id>[\d ]+)/$',
        quiz_views.question, name='question'),
    url(r'teacher/quiz/questions/(?P<question_id>[\d ]+)/update/$',
        quiz_views.update_question, name='edit_question'),
    url(r'teacher/quiz/questions/(?P<question_id>[\d ]+)/delete/$',
        quiz_views.delete_question, name='delete_question'),

    #teacher manage answer
    url(r'teacher/quiz/answers/(?P<answer_id>[\d ]+)/edit/$',
        quiz_views.update_answer, name='edit_answer'),
    url(r'teacher/quiz/answers/(?P<answer_id>[\d ]+)/delete/$',
        quiz_views.delete_answer, name='delete_answer'),

    #teacher manage assigment
    url(r'^teacher/(?P<chapter_slug>[\w-]+)/assignment/create/$',
        assignment_views.create_assignment, name='create_assignment'),
    url(r'^teacher/assignments-detail/(?P<assignment_id>[\d ]+)/edit/$',
        assignment_views.update_assignment, name='edit_assignment'),  
    url(r'^teacher/assignments-detail/(?P<assignment_id>[\d ]+)/delete/$',
        assignment_views.delete_assignment, name='delete_assignment'),  
    url(r'^teacher/assignment-detail/(?P<assignment_id>[\d ]+)/$',
        assignment_views.assignment, name='assignment'),
    url(r'^teacher/take-assignment/(?P<assignment_id>[\d ]+)/$',
        assignment_views.take_assignment, name='take_assignment'),
    url(r'teacher/give-result/(?P<take_assignment_id>[\d ]+)/$',
        assignment_views.give_score_to_assignment, name='give_result'),
    url(r'^teacher/assignment-result/(?P<assignment_id>[\d ]+)/$',
        assignment_views.check_result, name='assignment_result'),

    #teacher manage text
    url(r'^teacher/(?P<course_name>[\w ]+)/(?P<slug>[\w-]+)/(?P<txt_id>[\d ]+)/txt/edit/$',
        course_views.update_text_block, name='edit_txt'),
    url(r'^teacher/(?P<course_name>[\w ]+)/(?P<slug>[\w-]+)/(?P<txt_id>[\d ]+)/txt/delete/$',
        course_views.delete_text_block, name='delete_txt'),

    #teacher manage youtube link
    url(r'^teacher/(?P<course_name>[\w ]+)/(?P<slug>[\w-]+)/(?P<yt_id>[\d ]+)/yt/edit/$',
        course_views.update_yt_link, name='edit_yt'),
    url(r'^teacher/(?P<course_name>[\w ]+)/(?P<slug>[\w-]+)/(?P<yt_id>[\d ]+)/yt/delete/$',
        course_views.delete_yt_link, name='delete_yt'),
    
    #teacher manage file 
    url(r'^teacher/(?P<course_name>[\w ]+)/(?P<slug>[\w-]+)/(?P<file_id>[\d ]+)/file/delete/$',
        course_views.delete_file, name='delete_file'),
]
