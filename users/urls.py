from django.conf.urls import url
from . import  views 


urlpatterns = [
    url(r'^$', views.dashboard, name='dashboard'),
    url(r'^student/', views.student, name='student'),
    url(r'^teacher/', views.teacher, name='teacher'),

    url(r'^admin/', views.admin, name='admin'),
    url(r'^edit/(?P<username>[\w ]+)/$', views.update_user, name='edit_user'),
    url(r'^delete/(?P<username>[\w ]+)/$', views.delete_user, name='delete_user'),

    url(r'^profile/(?P<username>[\w ]+)/$', views.update_user, name='user_profile')
]
