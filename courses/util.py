from courses.models import *

def get_detail_list(get_teacher=True):
    detail_list = {} 
    index = 0
    if get_teacher:
        # display list course 
        teachers = UserProfile.objects.filter(is_teacher=True)
        for teacher in teachers:
            number_course = Course.objects.filter(user=teacher).count()
            detail_list[index] = {
                'num': number_course,
                'name': teacher.username
            }
            index += 1
    else:
        categories = Category.objects.all()
        for category in categories:
            number = Course.objects.filter(category=category, for_everybody=True).count()
            detail_list[index] = {
                'num': number,
                'slug': category.slug,
                'name': category.name
            }
            index += 1

    return detail_list

def get_five_new_course():
    new_courses = Course.objects.order_by('-created_date')[:5]
    return new_courses

def get_context(courses, filter=None):
    context = {
        'title': 'Courses',
        'courses': courses,
        'detail_teachers': get_detail_list(get_teacher=True),
        'detail_categories': get_detail_list(get_teacher=False),
        'related_courses': get_five_new_course(),
        'filter': filter
    }
    return context