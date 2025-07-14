from ninja_extra import NinjaExtraAPI
from ..schemas.course import (
    CourseSchema,
    ErrorSchema,
    CreateCourseSchema,
    UpdateCourseSchema,
    RestoreCourseSchema,
    CategorySchema,
    SubCategorySchema,
)
from course.models import Course,Category,SubCategory
from ninja_jwt.controller import NinjaJWTDefaultController
from ninja_jwt.authentication import JWTAuth



course_api = NinjaExtraAPI(urls_namespace="course", auth=JWTAuth())

course_api.register_controllers(NinjaJWTDefaultController)


@course_api.get("courses/{subcategory_slug}", response={200: list[CourseSchema], 401: ErrorSchema})
def list_courses(request, subcategory_slug: str):
    if not request.user.is_authenticated:
        return 401, {"message": "Authentication required"}
    try:
        subcategory = SubCategory.objects.get(slug=subcategory_slug)
        courses = list(Course.objects.filter(subcategory=subcategory))
    except SubCategory.DoesNotExist:
        return 404, {"message": "SubCategory not found"}
    return 200, courses


@course_api.post(
    "courses/",
    response={201: CourseSchema, 400: ErrorSchema, 401: ErrorSchema, 403: ErrorSchema},
)
def create_course(request, data: CreateCourseSchema):
    user = request.user

    if not user.is_authenticated:
        return 401, {"message": "Authentication required"}
    if user.user_type not in ["teacher", "admin"]:
        return 403, {"message": "Permission denied"}

    data = data.model_dump()
    course = Course(**data, user=request.user)
    course.save()
    return 201, course


@course_api.delete(
    "courses/{course_id}",
    response={204: None, 401: ErrorSchema, 404: ErrorSchema, 403: ErrorSchema},
)
def delete_course(request, course_id: int):
    user = request.user
    if not user.is_authenticated:
        return 401, {"message": "Authentication required"}
    if user.user_type not in ["teacher", "admin"]:
        return 403, {"message": "Permission denied"}
    try:
        course = Course.objects.get(id=course_id)
    except Course.DoesNotExist:
        return 404, {"message": "Course not found"}
    course.delete()
    return 204, "Course deleted successfully"


@course_api.put(
    "courses/{course_id}",
    response={200: CourseSchema, 401: ErrorSchema, 404: ErrorSchema, 403: ErrorSchema},
)
def update_course(request, course_id: int, data: CreateCourseSchema):
    user = request.user
    if not user.is_authenticated:
        return 401, {"message": "Authentication required"}
    if user.user_type not in ["teacher", "admin"]:
        return 403, {"message": "Permission denied"}
    try:
        course = Course.objects.get(user=user, id=course_id)
    except Course.DoesNotExist:
        return 404, {"message": "Course not found"}
    data = data.model_dump()
    for field, value in data.items():
        setattr(course, field, value)
    course.save()
    return 200, course


@course_api.patch(
    "courses/{course_id}",
    response={200: CourseSchema, 401: ErrorSchema, 404: ErrorSchema, 403: ErrorSchema},
)
def partial_update_course(request, course_id: int, data: UpdateCourseSchema):
    user = request.user
    if not user.is_authenticated:
        return 401, {"message": "Authentication required"}
    if user.user_type not in ["teacher", "admin"]:
        return 403, {"message": "Permission denied"}
    try:
        course = Course.objects.get(user=user, id=course_id)
    except Course.DoesNotExist:
        return 404, {"message": "Course not found"}
    data = data.model_dump(exclude_unset=True)
    for field, value in data.items():
        setattr(course, field, value)
    course.save()
    return 200, course


@course_api.post(
    "courses/restore/",
    response={200: CourseSchema, 401: ErrorSchema, 404: ErrorSchema, 403: ErrorSchema},
)
def restore_course(request, data: RestoreCourseSchema):
    user = request.user
    if not user.is_authenticated:
        return 401, {"message": "Authentication required"}
    if user.user_type not in ["teacher", "admin"]:
        return 403, {"message": "Permission denied"}
    data = data.model_dump()
    data.pop("image")
    data.pop("description")
    try:
        course = Course.objects.get(**data, is_deleted=True, user=user)
    except Course.DoesNotExist:
        return 404, {"message": "Course not found"}
    except Exception as e:
        return 404, {
            "message": "Sorry but we couldn't find your course\nGive us specific data\nTry again"
        }
    course.restore()
    return 200, course


@course_api.get("categories/", response={200: list[CategorySchema], 401: ErrorSchema})
def list_categories(request):
    if not request.user.is_authenticated:
        return 401, {"message": "Authentication required"}
    categories = list(Category.objects.all())
    return 200, categories

@course_api.get("subcategories/", response={200: list[SubCategorySchema], 401: ErrorSchema})
def list_subcategories(request):
    if not request.user.is_authenticated:
        return 401, {"message": "Authentication required"}
    subcategories = list(SubCategory.objects.all())
    return 200, subcategories

@course_api.get("subcategories/{category_slug}", response={200: list[SubCategorySchema], 401: ErrorSchema})
def list_subcategories_by_category(request, category_slug: str):
    if not request.user.is_authenticated:
        return 401, {"message": "Authentication required"}
    try:
        category = Category.objects.get(slug=category_slug)
        subcategories = list(SubCategory.objects.filter(category=category))
    except Category.DoesNotExist:
        return 404, {"message": "Category not found"}
    return 200, subcategories