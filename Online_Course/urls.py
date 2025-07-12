"""
URL configuration for Online_Course project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.contrib import admin
from django.urls import path
from user.api import user_api
from course.routers.course import course_api
from course.routers.lesson import lesson_api
from enrollment.router.enrollment import enrollment_api

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/", user_api.urls),
    path("api/", course_api.urls),
    path("api/", lesson_api.urls),
    path("api/", enrollment_api.urls),

]
