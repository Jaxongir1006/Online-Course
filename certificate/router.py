from ninja_extra import NinjaExtraAPI
from .schemas import CertificateSchema,CreateCertificateSchema,ErrorSchema
from .models import Certificate
from ninja_jwt.authentication import JWTAuth
from ninja_jwt.controller import NinjaJWTDefaultController
from user.models import User
from course.models import Course
from utils.certificate import generate_certificate

certificate_api = NinjaExtraAPI(urls_namespace="certificate", auth=JWTAuth())

certificate_api.register_controllers(NinjaJWTDefaultController)


@certificate_api.get("certificates/", response={200: list[CertificateSchema], 401: ErrorSchema})
def list_certificates(request):
    if not request.user.is_authenticated:
        return 401, {"message": "Authentication required"}
    certificates = list(Certificate.objects.filter(user=request.user))
    return 200, certificates

@certificate_api.post("certificates/", response={201: CertificateSchema, 400: ErrorSchema, 401: ErrorSchema, 403: ErrorSchema, 404: ErrorSchema})
def giving_certificate(request, data: CreateCertificateSchema):
    if not request.user.is_authenticated:
        return 401, {"message": "Authentication required"}
    if request.user.user_type not in ["teacher", "admin"] :
        return 403, {"message": "Permission denied"}
    
    data = data.model_dump()
    student = data.pop("student")

    try:
        course = Course.objects.get(slug=data.pop("course"))
        user = User.objects.get(username=student)
    except Course.DoesNotExist:
        return 404, {"message": "Course not found"}
    except User.DoesNotExist:
        return 404, {"message": "User not found"}

    certificate = generate_certificate(user, course, data.pop("score"))

    return 201, certificate