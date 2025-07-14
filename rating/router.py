from ninja_extra import NinjaExtraAPI
from .schemas import RatingSchema,ErrorSchema,CreateRatingSchema,DeleteRatingSchema
from .models import Rating
from ninja_jwt.authentication import JWTAuth
from ninja_jwt.controller import NinjaJWTDefaultController
from course.models import Course


rating_api = NinjaExtraAPI(urls_namespace="rating", auth=JWTAuth())

rating_api.register_controllers(NinjaJWTDefaultController)

@rating_api.post("ratings/{course_slug}/", response={201: RatingSchema, 400: ErrorSchema, 401: ErrorSchema, 404: ErrorSchema})
def create_rating(request, course_slug: str, data: CreateRatingSchema):
    user = request.user
    if not user.is_authenticated:
        return 401, {"message": "Authentication required"}
    data = data.model_dump()
    try:
        course = Course.objects.get(slug=course_slug)
        data['course'] = course
        data['user'] = user
    except Course.DoesNotExist:
        return 404, {"message": "Course not found"}
    rating = Rating(**data)
    rating.save()
    return 201, rating


@rating_api.get("ratings/{course_slug}/", response={200: float, 400: ErrorSchema, 401: ErrorSchema, 404: ErrorSchema})
def get_rating(request, course_slug: str):
    user = request.user
    if not user.is_authenticated:
        return 401, {"message": "Authentication required"}
    try:
        course = Course.objects.get(slug=course_slug)
        rating = Rating.objects.get(course=course, user=user)
    except Course.DoesNotExist:
        return 404, {"message": "Course not found"}
    except Rating.DoesNotExist:
        return 404, {"message": "Rating not found"}
    return 200, rating.calculate_rating()


@rating_api.post("rating/delete/", response={204: dict, 401: ErrorSchema, 404: ErrorSchema, 403: ErrorSchema})
def delete_rating(request, data: DeleteRatingSchema):
    user = request.user
    if not user.is_authenticated:
        return 401, {"message": "Authentication required"}
    data = data.model_dump()
    try:
        course = Course.objects.get(slug=data['course_slug'])
        rating = Rating.objects.get(course=course, user=user)
    except Course.DoesNotExist:
        return 404, {"message": "Course not found"}
    except Rating.DoesNotExist:
        return 404, {"message": "Rating not found"}
    rating.delete()
    return 204, {"message":"Rating deleted successfully"}