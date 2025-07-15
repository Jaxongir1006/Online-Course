from ninja import Schema, ModelSchema
from ..models import Comment
from typing import Optional


class ErrorSchema(Schema):
    message: str

class CommentSchema(ModelSchema):
    class Config:
        model = Comment
        model_fields = ['id', 'user', 'course', 'text', 'parent', 'created_at', 'updated_at']
        from_attributes = True

class CreateCommentSchema(Schema):
    text: str
    parent: Optional[int] = None
    course: str