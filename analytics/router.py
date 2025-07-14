
from django.db.models import Count
from .schemas import AnalyticsSchema, ErrorSchema
from course.models import Course
from ninja_jwt.authentication import JWTAuth
from ninja_jwt.controller import NinjaJWTDefaultController
from ninja_extra import NinjaExtraAPI

analytics_api = NinjaExtraAPI(urls_namespace="analytics", auth=JWTAuth())

analytics_api.register_controllers(NinjaJWTDefaultController)

@analytics_api.get("analytics/", response={200: AnalyticsSchema, 404:ErrorSchema, 403:ErrorSchema})
def get_analytics(request):
    user = request.user
    if user.user_type not in ['admin', 'teacher']:
        return 403, {"message": "Permission denied"}
    

    courses = Course.objects.all()

    most_rated = Course.objects.annotate(
        rating_count=Count('rating')
    ).order_by('-rating_count')[:5]

    # most_viewed = Course.objects.order_by('-views')[:5]

    most_enrolled = Course.objects.annotate(
        student_count=Count('enrollments')
    ).order_by('-student_count')[:5]

    return {
        "courses": courses,
        "most_rated_courses": most_rated,
        "most_enrolled_courses": most_enrolled
    }
