from ninja import Schema, ModelSchema
from course.models import Course


class ErrorSchema(Schema):
    message: str


class CourseSchema(ModelSchema):
    class Meta:
        model = Course
        fields = ['id', 'user', 'title', 'description', 'price', 'image']


class CreateCourseSchema(Schema):
    title: str
    description: str
    price: float
    image: str = None