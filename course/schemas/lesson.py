from ninja import Schema, ModelSchema
from course.models import Lesson
from typing import Optional

class ErrorSchema(Schema):
    message: str

class LessonSchema(ModelSchema):
    class Meta:
        model = Lesson
        fields = ['id', 'course', 'title', 'duration_minutes', 'video_url']
        read_only_fields = ['id']


class CreateLessonSchema(Schema):
    title: str
    duration_minutes: int
    video_url: str
    course: str
    

class UpdateLessonSchema(Schema):
    title: str = Optional[str]
    duration_minutes: int = Optional[int]
    video_url: str = Optional[str]


class RestoreLessonSchema(Schema):
    title: str
    duration_minutes: int
    video_url: str
    course: str