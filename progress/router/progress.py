from ninja_extra import NinjaExtraAPI
from ..schemas.progress import ProgressSchema,ErrorSchema
from progress.models import Progress
from ninja_jwt.controller import NinjaJWTDefaultController
from ninja_jwt.authentication import JWTAuth
from django.utils import timezone
from course.models import Lesson
from enrollment.models import Enrollment
from user.models import User

progress_api = NinjaExtraAPI(urls_namespace="progress", auth=JWTAuth())

progress_api.register_controllers(NinjaJWTDefaultController)


@progress_api.get("progress/user/{user_id}/lesson/{lesson_id}/", response={200: ProgressSchema, 401: ErrorSchema, 404: ErrorSchema, 403: ErrorSchema})
def get_progress(request, user_id: int, lesson_id: int):
    current_user = request.user

    if not current_user.is_authenticated:
        return 401, {"message": "Authentication required"}
    
    if current_user.user_type not in ['teacher', 'admin']:
        return 403, {"message": "Permission denied"}
    
    try:
        user = User.objects.get(id=user_id)
        lesson = Lesson.objects.get(id=lesson_id)
        progress = Progress.objects.get(user=user, lesson=lesson)
    except Progress.DoesNotExist:
        return 404, {"message": "Progress not found"}
    except User.DoesNotExist:
        return 404, {"message": "User not found"}
    except Lesson.DoesNotExist:
        return 404, {"message": "Lesson not found"}

    return 200, progress


@progress_api.get("progress-user/", response={200: list[ProgressSchema], 401: ErrorSchema, 404: ErrorSchema})
def get_user_progress(request):
    user = request.user
    if not user.is_authenticated:
        return 401, {"message": "Authentication required"}
    try:
        progress = Progress.objects.filter(user=user)
    except Progress.DoesNotExist:
        return 404, {"message": "Progress not found"}
    return 200, progress    

@progress_api.post("progress-done/lesson/{lesson_id}/", response={200: ProgressSchema, 401: ErrorSchema, 404: ErrorSchema})
def mark_lesson_watched(request, lesson_id: int):
    user = request.user

    if not user.is_authenticated:
        return 401, {"message": "Authentication required"}
    try:
        lesson = Lesson.objects.get(id=lesson_id)
    except Lesson.DoesNotExist:
        return 404, {"message": "Lesson not found"}
    
    if not Enrollment.objects.filter(user=user, course=lesson.course).exists():
        return 403, {"message": "You are not enrolled in this course"}

    progress, created = Progress.objects.get_or_create(user=user, lesson=lesson)
    progress.watched = True
    progress.watched_at = timezone.now()
    progress.save()

    return 200, progress


@progress_api.get("unwatched-lessons/", response={200: list[ProgressSchema], 401: ErrorSchema, 404: ErrorSchema})
def unwatched_lessons(request):
    user = request.user
    if not user.is_authenticated:
        return 401, {"message": "Authentication required"}
    try:
        progress = Progress.objects.filter(user=user, watched=False)
    except Progress.DoesNotExist:
        return 404, {"message": "Progress not found"}
    return 200, progress