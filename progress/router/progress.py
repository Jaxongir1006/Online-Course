from ninja_extra import NinjaExtraAPI
from ..schemas.progress import ProgressSchema,ErrorSchema
from progress.models import Progress
from ninja_jwt.controller import NinjaJWTDefaultController
from ninja_jwt.authentication import JWTAuth
from user.models import User
from course.models import Lesson

progress_api = NinjaExtraAPI(urls_namespace="progress", auth=JWTAuth())

progress_api.register_controllers(NinjaJWTDefaultController)


@progress_api.get("/user/{user_id}/lesson/{lesson_id}", response={200: ProgressSchema, 401: ErrorSchema, 404: ErrorSchema})
def get_progress(request, user_id: int, lesson_id: int):
    user = request.user
    if not user.is_authenticated:
        return 401, {"message": "Authentication required"}
    try:
        user = User.objects.get(id=user_id)
        lesson = Lesson.objects.get(id=lesson_id)
        progress = Progress.objects.get(user=user, lesson=lesson)
    except Progress.DoesNotExist:
        return 404, {"message": "Progress not found"}
    return 200, progress

