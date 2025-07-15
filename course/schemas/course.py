from ninja import Schema, ModelSchema
from course.models import Course, Category, SubCategory
from typing import Optional


class ErrorSchema(Schema):
    message: str


class CourseSchema(ModelSchema):
    class Config:
        model = Course
        model_fields = ['id', 'user', 'title', 'description', 'price', 'image', 'slug']
        from_attributes = True


class CreateCourseSchema(Schema):
    title: str
    description: str
    price: float
    image: str = None
    subcategory_slug: str


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
    class Config:
        model = Category
        model_fields = ['id', 'name', 'slug', 'image']
        from_attributes = True

class SubCategorySchema(ModelSchema):
    class Config:
        model = SubCategory
        model_fields = ['id', 'name', 'slug', 'image']
        from_attributes = True