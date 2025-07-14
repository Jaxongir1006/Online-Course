from ninja import Schema, ModelSchema
from enrollment.models import Enrollment

class ErrorSchema(Schema):
    message: str


class EnrollmentSchema(ModelSchema):
    class Meta:
        model = Enrollment
        fields = '__all__'

class RegisterEnrollmentSchema(Schema):
    course: str