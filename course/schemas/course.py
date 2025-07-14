from ninja import Schema, ModelSchema
from course.models import Course, Category, SubCategory
from typing import Optional


class ErrorSchema(Schema):
    message: str


class CourseSchema(ModelSchema):
    class Meta:
        model = Course
        fields = ['id', 'user', 'title', 'description', 'price', 'image', 'slug']
        read_only_fields = ['id']


class CreateCourseSchema(Schema):
    title: str
    description: str
    price: float
    image: str = None


class UpdateCourseSchema(Schema):
    title: str = Optional[str]
    description: str = Optional[str]
    price: float = Optional[float]
    image: str = Optional[str]


class RestoreCourseSchema(Schema):
    title: str
    description: str
    price: float
    image: str


class CategorySchema(ModelSchema):
    class Meta:
        model = Category
        fields = ['id', 'name', 'slug', 'image']


class SubCategorySchema(ModelSchema):
    class Meta:
        model = SubCategory
        fields = ['id', 'name', 'slug', 'image']