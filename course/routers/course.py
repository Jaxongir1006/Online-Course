from ninja_extra import NinjaExtraAPI
from ..schemas.course import CourseSchema, ErrorSchema, CreateCourseSchema, UpdateCourseSchema
from course.models import Course
from ninja_jwt.controller import NinjaJWTDefaultController
from ninja_jwt.authentication import JWTAuth

course_api = NinjaExtraAPI(urls_namespace="course", auth=JWTAuth()) 

course_api.register_controllers(NinjaJWTDefaultController)

@course_api.get("courses/", response={200: list[CourseSchema], 401: ErrorSchema})
def list_courses(request):
    if not request.user.is_authenticated:
        return 401, {"message": "Authentication required"}
    courses = list(Course.objects.all())
    return 200, courses

@course_api.post("courses/", response={201: CourseSchema, 400: ErrorSchema, 401: ErrorSchema, 403: ErrorSchema})
def create_course(request, data: CreateCourseSchema):
    user = request.user
    
    if not user.is_authenticated:
        return 401, {"message": "Authentication required"}
    if user.user_type not in ['teacher', 'admin']:
        return 403, {"message": "Permission denied"}
    
    data = data.model_dump()
    course = Course(**data, user=request.user)
    course.save()
    return 201, course


@course_api.delete("courses/{course_id}", response={204: None, 401: ErrorSchema, 404: ErrorSchema, 403: ErrorSchema})
def delete_course(request, course_id: int):
    user = request.user
    if not user.is_authenticated:
        return 401, {"message": "Authentication required"}
    if user.user_type not in ['teacher', 'admin']:
        return 403, {"message": "Permission denied"}
    try:
        course = Course.objects.get(id=course_id)
    except Course.DoesNotExist:
        return 404, {"message": "Course not found"}
    course.delete()
    return 204, "Course deleted successfully"

@course_api.put("courses/{course_id}", response={200: CourseSchema, 401: ErrorSchema, 404: ErrorSchema, 403: ErrorSchema})
def update_course(request, course_id: int, data: CreateCourseSchema):
    user = request.user
    if not user.is_authenticated:
        return 401, {"message": "Authentication required"}
    if user.user_type not in ['teacher', 'admin']:
        return 403, {"message": "Permission denied"}
    try:
        course = Course.objects.get(user=user, id=course_id)
    except Course.DoesNotExist:
        return 404, {"message": "Course not found"}
    data = data.model_dump()
    for field, value in data.items():
        setattr(course, field, value)
    course.save()
    return 200, course

@course_api.patch("courses/{course_id}", response={200: CourseSchema, 401: ErrorSchema, 404: ErrorSchema, 403: ErrorSchema})
def partial_update_course(request, course_id: int, data: UpdateCourseSchema):
    user = request.user
    if not user.is_authenticated:
        return 401, {"message": "Authentication required"}
    if user.user_type not in ['teacher', 'admin']:
        return 403, {"message": "Permission denied"}
    try:
        course = Course.objects.get(user=user, id=course_id)
    except Course.DoesNotExist:
        return 404, {"message": "Course not found"}
    data = data.model_dump(exclude_unset=True)
    for field, value in data.items():
        setattr(course, field, value)
    course.save()
    return 200, course
