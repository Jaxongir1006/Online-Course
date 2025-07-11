from functools import wraps
from ninja.errors import HttpError

def user_types_required(*allowed_types):
    def decorator(func):
        @wraps(func)
        def wrapper(request, *args, **kwargs):
            if not request.user.is_authenticated:
                raise HttpError(401, "Authentication required")
            if request.user.type not in allowed_types:
                raise HttpError(403, "Permission denied")
            return func(request, *args, **kwargs)
        return wrapper
    return decorator
