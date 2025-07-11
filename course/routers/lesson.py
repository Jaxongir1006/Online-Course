from ..schemas.lesson import LessonSchema, CreateLessonSchema,ErrorSchema
from course.models import Lesson
from ninja_extra import NinjaExtraAPI
from course.models import Course
from typing import List
from ninja_jwt.controller import NinjaJWTDefaultController
from ninja_jwt.authentication import JWTAuth

lesson_api = NinjaExtraAPI(urls_namespace="lesson", auth=JWTAuth())

lesson_api.register_controllers(NinjaJWTDefaultController)

@lesson_api.get("lessons/",response={200: List[LessonSchema], 401: ErrorSchema, 404: ErrorSchema})
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