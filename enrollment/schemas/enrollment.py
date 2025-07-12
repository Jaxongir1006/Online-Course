from ninja import Schema, ModelSchema
from enrollment.models import Enrollment


class ErrorSchema(Schema):
    message: str


class EnrollmentSchema(ModelSchema):
    class Meta:
        model = Enrollment
        fields = ['id', 'user', 'course', 'enrolled_at']
        read_only_fields = ['id', 'enrolled_at', 'user']


class RegisterEnrollmentSchema(Schema):
    course: str