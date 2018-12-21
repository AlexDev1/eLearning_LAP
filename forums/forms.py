from django import forms
from .models import *

import re

class AddTopicForm(forms.ModelForm):
    class Meta:
        model = Topic
        fields = ['subjects', 'topic_message']

    def clean_subjects(self):
        topic_name = self.cleaned_data['subjects']
        regexp = re.compile(r'[a-zA-Z!.? ]')
        if not regexp.match(topic_name):
            raise forms.ValidationError(
                "Please make sure topic name contains ( a-z, A-Z, !.?' ') characters"
            )
        return topic_name
    
class AddNewComment(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['message']