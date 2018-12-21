
from courses.models import Course
from users.models import UserProfile

teachers = UserProfile.objects.filter(is_teacher=True)
detail_courses = []
for teacher in teachers:
    number_course = Course.objects.filter(user=teacher).count()
    detail_courses.append({
        "num": number_course,
        "name_teacher": teacher.username
    })

for instance in detail_courses:
    print (instance)