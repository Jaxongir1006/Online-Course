from ninja_extra import NinjaExtraAPI
from ..schemas.enrollment import EnrollmentSchema,ErrorSchema,RegisterEnrollmentSchema
from enrollment.models import Enrollment
from course.models import Course
from ninja_jwt.authentication import JWTAuth
from ninja_jwt.controller import NinjaJWTDefaultController

enrollment_api = NinjaExtraAPI(urls_namespace="enrollment", auth=JWTAuth())

enrollment_api.register_controllers(NinjaJWTDefaultController)


@enrollment_api.get("enrollments/{course_slug}/", response={200: list[EnrollmentSchema], 401: ErrorSchema})
def get_enrollments_for_admins(request, course_slug: str):
    if not request.user.is_authenticated:
        return 401, {"message": "Authentication required"}
    if request.user.user_type != 'admin':
        return 403, {"message": "Permission denied"}
    try:
        course = Course.objects.get(slug=course_slug)
        enrollments = Enrollment.objects.filter(course=course)
    except Course.DoesNotExist:
        return 404, {"message": "Course not found"}
    return 200, enrollments


@enrollment_api.post("enrollments/", response={201: EnrollmentSchema, 400: ErrorSchema, 401: ErrorSchema, 404: ErrorSchema})
def register_enrollment(request, data: RegisterEnrollmentSchema):
    user = request.user
    if not user.is_authenticated:
        return 401, {"message": "Authentication required"}
    data = data.model_dump()
    try:
        course = Course.objects.get(slug=data['course'])
        data.pop('course')
        enrollment = Enrollment(**data, course=course, user=user)
    except Course.DoesNotExist:
        return 404, {"message": "Course not found"}
    enrollment.save()
    return 201, enrollment

@enrollment_api.get("my-courses/", response={200: list[EnrollmentSchema], 401: ErrorSchema, 404: ErrorSchema})
def get_my_courses(request):
    if not request.user.is_authenticated:
        return 401, {"message": "Authentication required"}
    try:
        enrollments = Enrollment.objects.filter(user=request.user)
    except Enrollment.DoesNotExist:
        return 401, {"message": "We are sorry but you didn't enroll to any course yet\nIf you want to enroll to a course you can do it from the main page"}
    return 200, list(enrollments)
    

