from django.shortcuts import render


# Create your views here.
def course_list(request):
    courses = [
        {'id': 1, 
         'course_title': 'Python: fundamentos hasta los detalles', 
         'level': 'Beginner', 
         'rating': 4.5, 
         'instructor': 'Alison Walsh',
         'course_image': 'images/curso_1.jpg',
         'instructor_image': 'https://randomuser.me/api/portraits/women/68.jpg'
         },
        {
            'id': 2,
            'course_title': 'Django: Aplicaciones robustas',
            'level': 'Beginner',
            'rating': 4.7,
            'instructor': 'Patty Kutch',
            'course_image': 'images/curso_2.jpg',
            'instructor_image': 'https://randomuser.me/api/portraits/women/20.jpg'
        },
        {
            'id': 3,
            'course_title': 'Django Avanzado: Construye y despliega aplicaciones web profesionales',
            'level': 'Advanced',
            'rating': 4.3,
            'instructor': 'Alonzo Murray',
            'course_image': 'images/curso_3.jpg',
            'instructor_image': 'https://randomuser.me/api/portraits/women/32.jpg'
        },
        {
            'id': 4,
            'course_title': 'FastAPI Avanzado: Construye APIs rápidas y escalables',
            'level': 'Advanced',
            'rating': 4.8,
            'instructor': 'Gregory Harris',
            'course_image': 'images/curso_4.jpg',
            'instructor_image': 'https://randomuser.me/api/portraits/women/45.jpg'
        }
    ]  # Aquí iría la lógica para obtener los cursos desde la base de datos
    return render(request, 'courses/courses.html', {'courses': courses})

def course_detail(request):
    course = {
        'course_title': 'Python: fundamentos hasta los detalles',
        'course_link': 'https://www.udemy.com/course/python-fundamentos-hasta-los-detalles/',
        'info_course': {
            'lessons': 79,
            'duration': 8,
            'instructor': 'Ricardo Cuéllar'
            },
        'course_content': [ 
            {
                'id': 1,
                'name': 'Introducción al curso',
                'lessons': [
                    {'name': 'Bienvenida', 'type': 'video', 'duration': '5:00'},
                    {'name': '¿Qué es Python?', 'type': 'article', 'duration': '10:00'},
                    {'name': 'Instalación de Python', 'type': 'video', 'duration': '8:30'},
                ]
            }
        ]
    }  # Aquí iría la lógica para obtener los detalles del curso desde la base de datos
    return render(request, 'courses/course_detail.html', {'course': course})

def course_lesson(request, course_id, lesson_id):
    pass
# return render(request, 'courses/course_detail.html', {'course_id': course_id})