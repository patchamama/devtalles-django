from django.shortcuts import render

# Create your views here.


def course_list(request):
    courses = [
        {
            'id': 1,
            'level': 'Principiante',
            'rating': 4.8,
            'course_title': 'Python: fundamentos hasta los detalles',
            'instructor': 'Elizabeth Olsen',
            'course_image': 'images/curso_1.jpg',
            'instructor_image': 'https://randomuser.me/api/portraits/women/68.jpg'
        },
        {
            'id': 2,
            'level': 'Intermedio',
            'rating': 4.9,
            'course_title': 'Django: Aplicaciones robustas',
            'instructor': 'Alonso Murray',
            'course_image': 'images/curso_2.jpg',
            'instructor_image': 'https://randomuser.me/api/portraits/women/20.jpg'
        },
        {
            'id': 3,
            'level': 'Principiante',
            'rating': 5.0,
            'course_title': 'Fast API',
            'instructor': 'Gregory Harris',
            'course_image': 'images/curso_3.jpg',
            'instructor_image': 'https://randomuser.me/api/portraits/women/32.jpg'
        },
        {
            'id': 4,
            'level': 'Avanzado',
            'rating': 5.0,
            'course_title': 'Django Rest',
            'instructor': 'Alison Walsh',
            'course_image': 'images/curso_4.jpg',
            'instructor_image': 'https://randomuser.me/api/portraits/women/45.jpg'
        }
    ]
    return render(request, "courses/courses.html", {
        'courses': courses
    })


def course_detail(request):
    course = {
        'course_title': 'Django Aplicaciones',
        'course_link': 'course_lessons',
        'course_image': 'images/curso_2.jpg',
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
                    {
                        'name': '¿Qué aprenderás en el curso?',
                        'type': 'video'
                    },
                    {
                        'name': '¿Cómo usar la plataforma?',
                        'type': 'article'
                    }
                ]
            }
        ]
    }
    return render(request, 'courses/course_detail.html', {
        'course': course
    })


def course_lessons(request):
    lesson = {
        'course_title': 'Django Aplicaciones',
        'course_progress': 30,
        'course_content': [
            {
                'id': 1,
                'name': 'Introducción al curso',
                'total_lessons': 6,
                'complete_lessons': 3,
                'lessons': [
                    {
                        'name': '¿Qué aprenderás en el curso?',
                        'type': 'video'
                    },
                    {
                        'name': '¿Cómo usar la plataforma?',
                        'type': 'article'
                    }
                ]
            },
            {
                'id': 2,
                'name': 'Django principios',
                'total_lessons': 12,
                'complete_lessons': 2,
                'lessons': [
                    {
                        'name': '¿Qué aprenderás en el curso?',
                        'type': 'video'
                    },
                    {
                        'name': '¿Cómo usar la plataforma?',
                        'type': 'article'
                    }
                ]
            }
        ]
    }
    return render(request, 'courses/course_lessons.html',
                  {
                      'lesson': lesson
                  })
