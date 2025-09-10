from django.shortcuts import render


# Create your views here.
def course_list(request):
    pass
# return render(request, 'courses/course_list.html')

def course_detail(request, course_id):
    pass

def course_lesson(request, course_id, lesson_id):
    pass
# return render(request, 'courses/course_detail.html', {'course_id': course_id})