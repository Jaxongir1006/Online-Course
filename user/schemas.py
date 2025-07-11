from ninja import Schema, ModelSchema
from .models import User


class ErrorSchema(Schema):
    message: str

class RegisterUserSchema(Schema):
    username: str
    email: str
    password: str
    confirm_password: str

class LoginUserSchema(Schema):
    username: str = None
    password: str
    email: str = None

class UserSchema(ModelSchema): 
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'date_joined', 'first_name', 'last_name', 'user_type',]

