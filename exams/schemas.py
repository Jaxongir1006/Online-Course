from ninja import Schema, ModelSchema
from .models import ExamQuestion,Exam,ExamResult
from typing import Optional, Literal

class ErrorSchema(Schema):
    message: str


class ExamQuestionSchema(ModelSchema):
    class Config:
        model = ExamQuestion
        model_fields = '__all__'
        from_attributes = True


class QuestionOptionSchema(Schema):
    label: str  # 'A', 'B', 'C', 'D'
    text: str

class CreateExamQuestionSchema(Schema):
    text: str
    image: Optional[str] = None
    correct_option: str
    options: list[QuestionOptionSchema]


class CreateExamSchema(Schema):
    title: str


class ExamResultSchema(ModelSchema):
    class Config:
        model = ExamResult
        model_fields = '__all__'
        from_attributes = True


class AnswerSchema(Schema):
    question_id: int
    selected_option: Literal["A", "B", "C", "D"]

class SubmitExamSchema(Schema):
    answers: list[AnswerSchema]