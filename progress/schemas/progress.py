from ..models import Progress
from ninja import Schema, ModelSchema 


class ErrorSchema(Schema):
    message: str


class ProgressSchema(ModelSchema):
    class Config:
        model = Progress
        model_fields = ['user','lesson','watched_at','watched']
        from_attributes = True