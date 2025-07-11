from ninja_jwt.authentication import JWTBaseAuthentication
from ninja.security import HttpBearer
from ninja.errors import HttpError

class JWTAuth(HttpBearer):
    def authenticate(self, request, token):
        jwt_auth = JWTBaseAuthentication()
        try:
            validated_token = jwt_auth.get_validated_token(token)
            user = jwt_auth.get_user(validated_token)
            return user
        except Exception as e:
            # Token yaroqsiz yoki foydalanuvchi topilmadi
            raise HttpError(401, "Token notogri yoki muddati tugagan")
