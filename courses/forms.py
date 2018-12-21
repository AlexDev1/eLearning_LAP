from django import forms
from courses.models import *
import re

def get_category_choices():
    """ get all category"""
    categories = Category.objects.all()
    return categories

class AddCourseForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super(AddCourseForm, self).__init__(*args, **kwargs)
        self.fields['category'] = forms.ModelChoiceField(queryset=get_category_choices())

    class Meta:
        model = Course
        fields = ['category','name', 'for_everybody']
    
    def clean_name(self):
        name = self.cleaned_data.get('name')
        regexp = re.compile(r'[0-9a-zA-Z ]')
        if not regexp.match(name):
            raise forms.ValidationError('Please make sure the course name contain (a-z, A-Z, 0-9, space) letters')
        return name

class AddChapterForm(forms.ModelForm):
    class Meta:
        model = Chapter
        fields = ['name']
    
    def clean_name(self):
        name = self.cleaned_data['name']
        regexp = re.compile(r'[0-9a-zA-Z ]')

        if not regexp.match(name):
            raise forms.ValidationError("Please make sure chapter name contain (a-z, A-Z, 0-9 and blank")
        return name

class AddLinkForm(forms.ModelForm):
    class Meta:
        model = YTLink
        fields = ['link']

class AddTextForm(forms.ModelForm):

    class Meta:
        model = TextBlock
        fields = ["lesson"]

class EditCourseForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(EditCourseForm, self).__init__(*args, **kwargs)
        self.fields['category'] = forms.ModelChoiceField(queryset=get_category_choices())

    class Meta:
        model = Course
        fields = ['category','name', 'for_everybody']

class EditChapterForm(forms.ModelForm):
    class Meta:
        model = Chapter
        fields = ['name']

class EditLinkForm(forms.ModelForm):
    class Meta:
        model = YTLink
        fields = ['link']

class EditTextForm(forms.ModelForm):
    class Meta:
        model = TextBlock
        fields = ['lesson']

class FileUploadForm(forms.ModelForm):
    class Meta:
        model = FileUpload
        fields = ['file']