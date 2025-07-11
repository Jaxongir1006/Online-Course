from ..schemas.lesson import LessonSchema, CreateLessonSchema,ErrorSchema, UpdateLessonSchema
from course.models import Lesson
from ninja_extra import NinjaExtraAPI
from course.models import Course
from typing import List
from ninja_jwt.controller import NinjaJWTDefaultController
from ninja_jwt.authentication import JWTAuth

lesson_api = NinjaExtraAPI(urls_namespace="lesson", auth=JWTAuth())

lesson_api.register_controllers(NinjaJWTDefaultController)

@lesson_api.get("lessons/",response={200: List[LessonSchema], 401: ErrorSchema, 404: ErrorSchema, 403: ErrorSchema})
def get_lesson(request, course_slug: str):
    if not request.user.is_authenticated:
        return 401, {"message": "Authentication required"}
    try:
        course = Course.objects.get(slug=course_slug)
        lessons = Lesson.objects.filter(course=course)
    except Course.DoesNotExist:
        return 404, {"message": "Course not found"}

    return 200, lessons


@lesson_api.post("lessons/", response={201: LessonSchema, 401: ErrorSchema, 404: ErrorSchema})
def create_lesson(request, data: CreateLessonSchema):
    user = request.user
    if not user.is_authenticated:
        return 401, {"message": "Authentication required"}
    if user.user_type not in ['teacher', 'admin']:
        return 403, {"message": "Permission denied"}
    data = data.model_dump()
    try:
        course = Course.objects.get(slug=data['course'])
        data.pop('course')
        lesson = Lesson(**data, course=course)
    except Course.DoesNotExist:
        return 404, {"message": "Course not found"}
    lesson.save()
    return 201, lesson

@lesson_api.delete("lessons/{lesson_id}", response={204: None,200: None, 401: ErrorSchema, 404: ErrorSchema, 403: ErrorSchema})
def delete_lesson(request, lesson_id: int):
    user = request.user
    if not user.is_authenticated:
        return 401, {"message": "Authentication required"}
    if user.user_type not in ['teacher', 'admin']:
        return 403, {"message": "Permission denied"}
    try:
        lesson = Lesson.objects.get(id=lesson_id)
    except Lesson.DoesNotExist:
        return 404, {"message": "Lesson not found"}
    lesson.delete()
    return 204, "Lesson deleted successfully"


@lesson_api.put("lessons/{lesson_id}", response={200: LessonSchema, 401: ErrorSchema, 404: ErrorSchema, 403: ErrorSchema})
def update_lesson(request, lesson_id: int, data: CreateLessonSchema):
    user = request.user
    if not user.is_authenticated:
        return 401, {"message": "Authentication required"}
    if user.user_type not in ['teacher', 'admin']:
        return 403, {"message": "Permission denied"}
    
    try:
        lesson = Lesson.objects.get(id=lesson_id)
    except Lesson.DoesNotExist:
        return 404, {"message": "Lesson not found"}

    data = data.model_dump()

    try:
        course = Course.objects.get(slug=data['course'])
        data.pop('course')
    except Course.DoesNotExist:
        return 404, {"message": "Course not found"}

    # Maydonlarni yangilash
    for field, value in data.items():
        setattr(lesson, field, value)
    lesson.course = course
    lesson.save()

    return 200, lesson


@lesson_api.patch("lessons/{lesson_id}", response={200: LessonSchema, 401: ErrorSchema, 404: ErrorSchema, 403: ErrorSchema})
def partial_update_lesson(request, lesson_id: int, data: UpdateLessonSchema):
    user = request.user
    if not user.is_authenticated:
        return 401, {"message": "Authentication required"}
    if user.user_type not in ['teacher', 'admin']:
        return 403, {"message": "Permission denied"}
    
    try:
        lesson = Lesson.objects.get(id=lesson_id)
    except Lesson.DoesNotExist:
        return 404, {"message": "Lesson not found"}

    data = data.model_dump(exclude_unset=True)  # faqat yuborilgan maydonlar olinadi

    for field, value in data.items():
        setattr(lesson, field, value)
    lesson.save()

    return 200, lesson
