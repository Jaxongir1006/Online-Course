from ninja_extra import NinjaExtraAPI
from ..schemas.course import CourseSchema, ErrorSchema, CreateCourseSchema
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

@course_api.post("courses/", response={201: CourseSchema, 400: ErrorSchema})
def create_course(request, data: CreateCourseSchema):
    user = request.user
    
    if not user.is_authenticated:
        return 401, {"message": "Authentication required"}
    if user.user_type not in ['teacher', 'admin']:
        return 403, {"message": "Permission denied"}
    
    data = data.model_dump()
    course = Course(**data)
    course.save()
    return 201, course
