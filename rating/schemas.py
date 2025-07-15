from ninja import Schema, ModelSchema
from .models import Rating

class ErrorSchema(Schema):
    message: str


class RatingSchema(ModelSchema):
    class Config:
        model = Rating
        model_fields = ['user', 'course', 'stars']
        from_attributes = True

class CreateRatingSchema(Schema):
    stars: int

class DeleteRatingSchema(Schema):
    course_slug: str