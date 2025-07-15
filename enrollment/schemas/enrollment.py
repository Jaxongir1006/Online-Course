from ninja import Schema, ModelSchema
from enrollment.models import Enrollment

class ErrorSchema(Schema):
    message: str


class EnrollmentSchema(ModelSchema):
    class Config:
        model = Enrollment
        model_fields = '__all__'
        from_attributes = True

class RegisterEnrollmentSchema(Schema):
    course: str