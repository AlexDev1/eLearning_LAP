from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator
from django.urls import reverse

from courses.models import Chapter
from users.models import UserProfile
# Create your models here.
class Assignment(models.Model):
    name = models.CharField(max_length=100)
    chapter = models.ForeignKey(Chapter,
                                    on_delete=models.CASCADE,
                                    related_name='exam_of_chapter')
    # author of assignment : teacher
    owner = models.ForeignKey(UserProfile,
                            on_delete=models.CASCADE,
                            related_name='assignments_of')
    # student take an assignment
    students = models.ManyToManyField(UserProfile, through="TakenAssignment")
    question = models.TextField()
    answer = models.TextField()
    correct_answer = models.TextField(default='')
    
    def __str__(self):
        return self.name
    
    def get_absolute_url(self):
        return reverse('assignment', kwargs={
            'assignment_id': self.id
        })


class TakenAssignment(models.Model):
    student = models.ForeignKey(UserProfile,
                            on_delete=models.CASCADE,
                            related_name='taken_assignments')
    assignment = models.ForeignKey(Assignment,
                                on_delete=models.CASCADE,
                                related_name='taken_assignment')
    score = models.FloatField( blank=True,
                                validators=[
                                MinValueValidator(0),
                                MaxValueValidator(10)
                                ],
                                null=True
                            )
    take_date = models.DateTimeField(auto_now_add=True)
