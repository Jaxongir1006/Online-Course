from django.template.loader import render_to_string
from weasyprint import HTML
import tempfile
from django.core.files import File
from datetime import date
from certificate.models import Certificate

def generate_certificate(user, course, score):
    html_string = render_to_string("certificate.html", {
        "user": user,
        "course": course,
        "score": score,
        "date": date.today().strftime('%B %d, %Y')
    })

    with tempfile.NamedTemporaryFile(delete=True, suffix=".pdf") as output:
        HTML(string=html_string, base_url='.').write_pdf(output.name)

        # Optional: Django modelga saqlash
        cert_model = Certificate.objects.create(
            user=user,
            course=course
        )
        cert_model.certificate_file.save(f"{user.username}_certificate.pdf", File(open(output.name, "rb")))
        cert_model.save()

        return cert_model
