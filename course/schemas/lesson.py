from ninja import Schema, ModelSchema
from course.models import Lesson


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
    