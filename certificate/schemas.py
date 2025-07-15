from ninja import Schema, ModelSchema
from .models import Certificate

class ErrorSchema(Schema):
    message: str


class CertificateSchema(ModelSchema):
    class Config:
        model = Certificate
        model_fields = ['user', 'course', 'issued_at', 'certificate_file']
        from_attributes = True


class CreateCertificateSchema(Schema):
    student: str
    course: str
    certificate_file: str