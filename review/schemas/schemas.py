from ninja import Schema, ModelSchema
from ..models import Comment
from typing import Optional


class ErrorSchema(Schema):
    message: str

class CommentSchema(ModelSchema):
    class Meta:
        model = Comment
        fields = ['id', 'user', 'course', 'text', 'parent', 'created_at', 'updated_at']
        read_only_fields = ['id', 'created_at', 'updated_at','user', 'course']

class CreateCommentSchema(Schema):
    text: str
    parent: Optional[int] = None
    course: str