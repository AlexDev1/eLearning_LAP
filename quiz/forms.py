
from django import forms

from .models import *

class CreateQuizForm(forms.ModelForm):
    class Meta:
        model = Quiz
        fields = ['name',]

class CreateQuestionForm(forms.ModelForm):
    class Meta:
        model = Question
        fields = ['text', 'number_of_answer']

class CreateAnswerForm(forms.ModelForm):
    class Meta:
        model = Answer
        fields = ['text', 'is_correct']

class QuestionAnswerForm(forms.ModelForm):
    answer = forms.ModelChoiceField(
        queryset=Answer.objects.none(),
        widget=forms.RadioSelect(),
        empty_label=None)

    class Meta:
        model = StudentAnswer
        fields = ['answer',]

    def __init__(self, *args, **kwargs):
        question = kwargs.pop('question')
        super().__init__(*args, **kwargs)
        self.fields['answer'].queryset = question.answers.order_by('-question_id')
