from django.db import models
from django.utils.text import slugify
from django.db.models.signals import pre_save
from django.urls import reverse
from django.core.validators import MaxValueValidator, MinValueValidator
from django.utils.timezone import now

from users.models import UserProfile
from courses.models import Chapter
# Create your models here.
class Quiz(models.Model):
    owner =  models.ForeignKey(UserProfile,
                            on_delete=models.CASCADE,
                            related_name='quizzes')
    name = models.CharField(max_length=64)
    chapter = models.ForeignKey(Chapter,
                                on_delete=models.CASCADE,
                                related_name='chapter_quizzes')
    students = models.ManyToManyField(UserProfile, through='TakenQuiz')
    slug = models.SlugField(unique=True)
    created_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name
    
    def get_absolute_url(self):
        return reverse("quiz", kwargs={
            "chapter_slug":self.chapter.slug,
            "quiz_slug": self.slug
        })
    
    def slug_default(self):
        slug = create_slug(new_slug=self.name)
        return slug
    


class Question(models.Model):
    text = models.CharField(max_length=250)
    quiz = models.ForeignKey(Quiz,
                            on_delete=models.CASCADE,
                            related_name='questions')
    number_of_answer = models.IntegerField( default=4,
                                            validators=[
                                                MaxValueValidator(5),
                                                MinValueValidator(4)
                                            ])


    def __str__(self):
        return self.text


class Answer(models.Model):
    text = models.CharField(max_length=100  )
    is_correct = models.BooleanField(default=False)
    question = models.ForeignKey(Question,
                                on_delete=models.CASCADE,
                                related_name='answers')
    def __str__(self):
        return self.text


class StudentAnswer(models.Model):
    student = models.ForeignKey(UserProfile, 
                            on_delete=models.CASCADE, 
                            related_name='quiz_answers')
    answer = models.ForeignKey(Answer, 
                            on_delete=models.CASCADE, 
                            related_name='+')


class TakenQuiz(models.Model):
    quiz = models.ForeignKey(Quiz,
                            on_delete=models.CASCADE,
                            related_name='taken_quizzes')
    student = models.ForeignKey(UserProfile,
                                on_delete=models.CASCADE,
                                related_name='taken_quizzes')
    score = models.FloatField()
    created_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return "%s-%s" %(self.quiz.slug, self.student.username )


def create_slug(instance=None, new_slug=None):
    slug = slugify(instance.name)
    if new_slug is not None:
        slug = new_slug
    
    qs = Quiz.objects.filter(slug=slug).order_by('-id')
    exists = qs.exists()

    if exists:
        new_slug = "%s-%s" % (slug, qs.first().id)
        return create_slug(instance, new_slug=new_slug)
    return slug

def pre_save_receiver(sender, instance, *args, **kwargs):
    if not instance.slug:
        instance.slug = create_slug(instance)
pre_save.connect(pre_save_receiver, sender=Quiz)