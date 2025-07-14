from ninja_extra import NinjaExtraAPI
from ..schemas.schemas import CommentSchema,ErrorSchema, CreateCommentSchema
from review.models import Comment
from ninja_jwt.authentication import JWTAuth
from ninja_jwt.controller import NinjaJWTDefaultController
from course.models import Course

 
review_api = NinjaExtraAPI(urls_namespace="review", auth=JWTAuth())

review_api.register_controllers(NinjaJWTDefaultController)


@review_api.post("create-comment/", response={201: CommentSchema, 400: ErrorSchema, 401: ErrorSchema, 404: ErrorSchema})
def create_comment(request, data: CreateCommentSchema):
    user = request.user
    if not user.is_authenticated:
        return 401, {"message": "Authentication required"}
    data = data.model_dump()
    course_slug = data.pop('course')
    parent = data.pop('parent')
    try:
        course = Course.objects.get(slug=course_slug)
        data['course'] = course
        if parent is not None:
            data['parent'] = Comment.objects.get(id=parent)
    except Course.DoesNotExist:
        return 404, {"message": "Course not found"}
    except Comment.DoesNotExist:
        return 404, {"message": "Parent comment not found"} 
    comment = Comment(**data, user=user)
    comment.save()
    return 201, comment

@review_api.get("comments/{course_slug}/", response={200: list[CommentSchema], 401: ErrorSchema, 404: ErrorSchema})
def get_comments(request, course_slug: str):
    user = request.user
    if not user.is_authenticated:
        return 401, {"message": "Authentication required"}
    comments = Comment.objects.filter(course__slug=course_slug, parent=None).order_by('-created_at')
    if not comments.exists():
        return 404, {"message": "Comments are not found"}
    return 200, comments

@review_api.get("comments/replies/{comment_id}/", response={200: list[CommentSchema], 401: ErrorSchema, 404: ErrorSchema})
def get_comment_replies(request, comment_id: int):
    user = request.user
    if not user.is_authenticated:
        return 401, {"message": "Authentication required"}
    replies = Comment.objects.filter(parent__id=comment_id).order_by('-created_at')
    if not replies.exists():
        return 404, {"message": "Replies not found"}
    return 200, replies