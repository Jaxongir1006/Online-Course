from ninja_extra import NinjaExtraAPI
from ninja_jwt.authentication import JWTAuth
from ninja_jwt.controller import NinjaJWTDefaultController
from .schemas import ErrorSchema, CreateExamQuestionSchema,ExamQuestionSchema, CreateExamSchema, ExamResultSchema, SubmitExamSchema
from course.models import Course
from .models import ExamQuestion,QuestionOption,Exam,ExamResult
from django.db import transaction
from certificate.models import Certificate


exams_api = NinjaExtraAPI(urls_namespace="exams", auth=JWTAuth())

exams_api.register_controllers(NinjaJWTDefaultController)


@exams_api.post("create-question/{course_slug}/", response={201: ExamQuestionSchema, 400: ErrorSchema, 401: ErrorSchema, 403: ErrorSchema, 404: ErrorSchema})
@transaction.atomic
def create_question(request, course_slug, data: CreateExamQuestionSchema):
    if not request.user.is_authenticated:
        return 401, {"message": "Authentication required"}
    if request.user.user_type not in ["teacher", "admin"]:
        return 403, {"message": "Permission denied"}

    try:
        course = Course.objects.get(slug=course_slug)
        exam = Exam.objects.get(course=course)
    except Course.DoesNotExist:
        return 404, {"message": "Course not found"}
    except Exam.DoesNotExist:
        return 404, {"message": "Exam not found"}

    data = data.model_dump()
    options = data.pop("options")
    question = ExamQuestion.objects.create(exam=exam, **data)

    for option in options:
        QuestionOption.objects.create(question=question, **option)

    return 201, question

@exams_api.get("questions/{course_slug}/", response={200: list[ExamQuestionSchema], 401: ErrorSchema, 404: ErrorSchema, 403: ErrorSchema})
def get_questions(request, course_slug: str):
    if not request.user.is_authenticated:
        return 401, {"message": "Authentication required"}
    if request.user.user_type not in ["teacher", "admin"]:
        return 403, {"message": "Permission denied"}
    try:
        course = Course.objects.get(slug=course_slug)
        exam = Exam.objects.get(course=course)
        questions = list(ExamQuestion.objects.filter(exam=exam))
    except Course.DoesNotExist:
        return 404, {"message": "Course not found"}
    except Exam.DoesNotExist:
        return 404, {"message": "Exam not found"}
    return 200, questions


@exams_api.post('create-exam/{course_slug}/', response={201: dict, 400: ErrorSchema, 401: ErrorSchema, 403: ErrorSchema, 404: ErrorSchema})
def create_exam(request, course_slug, data: CreateExamSchema):
    if not request.user.is_authenticated:
        return 401, {"message": "Authentication required"}
    if request.user.user_type not in ["teacher", "admin"]:
        return 403, {"message": "Permission denied"}

    try:
        course = Course.objects.get(slug=course_slug)
    except Course.DoesNotExist:
        return 404, {"message": "Course not found"}

    data = data.model_dump()
    title = data.pop("title")
    exam = Exam.objects.create(course=course, title=title)
    return 201, {"exam_id": exam.id, "title": title, "course": course.title, "course_id": course.id}


@exams_api.get('exam/{exam_id}/', response={200: dict, 400: ErrorSchema, 401: ErrorSchema, 403: ErrorSchema, 404: ErrorSchema})
def get_exam(request, exam_id: int):
    if not request.user.is_authenticated:
        return 401, {"message": "Authentication required"}
    if request.user.user_type not in ["teacher", "admin"]:
        return 403, {"message": "Permission denied"}

    try:
        exam = Exam.objects.get(id=exam_id)
    except Exam.DoesNotExist:
        return 404, {"message": "Exam not found"}

    return 200, {"exam_id": exam.id, "title": exam.title, "course": exam.course.title, "course_id": exam.course.id}


@exams_api.get('exam-results/{exam_id}/', response={200: list[ExamResultSchema], 400: ErrorSchema, 401: ErrorSchema, 403: ErrorSchema, 404: ErrorSchema})
def get_exam_results(request, exam_id: int):
    if not request.user.is_authenticated:
        return 401, {"message": "Authentication required"}
    
    try:
        exam = Exam.objects.get(id=exam_id)
    except Exam.DoesNotExist:
        return 404, {"message": "Exam not found"}

    return 200, list(ExamResult.objects.filter(exam=exam))

@exams_api.post("submit-exam/{exam_id}/", response={200: dict, 400: ErrorSchema, 401: ErrorSchema, 403: ErrorSchema, 404: ErrorSchema})
def submit_exam(request, exam_id: int, data: SubmitExamSchema):
    user = request.user
    if not user.is_authenticated:
        return 401, {"message": "Authentication required"}

    try:
        exam = Exam.objects.get(id=exam_id)
    except Exam.DoesNotExist:
        return 404, {"message": "Exam not found"}

    if ExamResult.objects.filter(user=user, exam=exam).exists():
        return 400, {"message": "You already submitted this exam"}

    answers = data.model_dump()["answers"]
    correct = 0
    total = 0

    for answer in answers:
        total += 1
        try:
            question = ExamQuestion.objects.get(id=answer["question_id"], exam=exam)
        except ExamQuestion.DoesNotExist:
            continue  # skip noto‘g‘ri question_id

        if question.correct_option == answer["selected_option"]:
            correct += 1
        print(question.correct_option)
    score = (correct / total) * 100 if total > 0 else 0
    score = round(score, 2)

    ExamResult.objects.create(
        user=user,
        exam=exam,
        score=score,
        total_questions=total,
        correct_answers=correct
    )

    if score > 70:
        Certificate.objects.create(user=user, course=exam.course, certificate_file="certificate.pdf")
        return 200, {
            "score": score,
            "correct": correct,
            "total": total, 
            'message': 'Congratulations! You passed the exam\nYour certificate has been sent to your email address.'
        }
    return 200, {
        "score": score,
        "correct": correct,
        "total": total
    }
