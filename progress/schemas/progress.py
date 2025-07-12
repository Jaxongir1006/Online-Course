from ..models import Progress
from ninja import Schema, ModelSchema 


class ErrorSchema(Schema):
    message: str


class ProgressSchema(ModelSchema):
    class Meta:
        model = Progress
        fields = ['user','lesson','watched_at','watched']