from ninja import Schema

class ErrorSchema(Schema):
    message: str

class UserSchema(Schema):
    id: int
    username: str

    class Config:
        from_attributes = True

class CourseSchema(Schema):
    id: int
    title: str
    slug: str
    user: UserSchema

    class Config:
        from_attributes = True

class AnalyticsSchema(Schema):
    courses: list[CourseSchema]
    most_rated_courses: list[CourseSchema]
    # most_viewed_courses: list[CourseSchema]
    most_enrolled_courses: list[CourseSchema]

    class Config:
        from_attributes = True