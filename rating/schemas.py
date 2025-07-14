from ninja import Schema, ModelSchema
from .models import Rating

class ErrorSchema(Schema):
    message: str


class RatingSchema(ModelSchema):
    class Meta:
        model = Rating
        fields = ['user', 'course', 'stars']
        read_only_fields = ['user', 'course']

class CreateRatingSchema(Schema):
    stars: int

class DeleteRatingSchema(Schema):
    course_slug: str