from django import forms
from django.core.validators import MaxValueValidator, MinValueValidator
from  assignment.models import *
class CreateAssignmentForm(forms.ModelForm):
    class Meta:
        model = Assignment
        fields = ['name', 'question', 'correct_answer']

class TakeAssignmentForm(forms.ModelForm):
    class Meta:
        model = Assignment
        fields = [ 'answer']

class GiveScoreForm(forms.Form):
    score = forms.FloatField(
        validators=[
            MinValueValidator(0),
            MaxValueValidator(10)
        ]
    )
