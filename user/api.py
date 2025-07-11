from .schemas import RegisterUserSchema, LoginUserSchema, UserSchema,ErrorSchema
from .models import User
from ninja_jwt.tokens import RefreshToken
from ninja_jwt.controller import NinjaJWTDefaultController
from ninja_extra import NinjaExtraAPI

user_api = NinjaExtraAPI(urls_namespace="user")

user_api.register_controllers(NinjaJWTDefaultController)


@user_api.post("register/", response={201: dict, 400: ErrorSchema})
def register(request, data: RegisterUserSchema):
    if data.password != data.confirm_password:
        return 400, {"message": "Passwords do not match"}
    if len(data.password) < 8:
        return 400, {"message": "Password must be at least 8 characters long"}
    if User.objects.filter(username=data.username).exists():
        return 400, {"message": "Username already exists"}
    if User.objects.filter(email=data.email).exists():
        return 400, {"message": "Email already exists"}
    data = data.model_dump()
    password = data.pop("password")
    data.pop("confirm_password")
    user = User(**data)
    token = RefreshToken.for_user(user)
    user.set_password(password)
    user.save()
    response_data = {
        "user": UserSchema.from_orm(user),
        "access_token": str(token.access_token),
        "refresh_token": str(token)
    }
    if not user:
        return 400, {"message": "User registration failed"}
    return 201, response_data

@user_api.post("login/", response={200: dict, 404: ErrorSchema, 400: ErrorSchema})
def login(request, data: LoginUserSchema):
    if data.email is None and data.username is None:
        return 400, {"message": "Username or email is required"}
    if data.password is None:
        return 400, {"message": "Password is required"}
    try:
        if data.email:
            user = User.objects.get(email=data.email)
        else:
            user = User.objects.get(username=data.username)
    except User.DoesNotExist:
        return 404, {"message": "User not found"}
    
    if not user.check_password(data.password):
        return 400, {"message": "Invalid password"}

    token = RefreshToken.for_user(user)
    response_data = {
        "user": UserSchema.from_orm(user),
        "access_token": str(token.access_token),
        "refresh_token": str(token)
    }
    return 200, response_data