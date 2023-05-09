from django.urls import path
from django.contrib import admin
from django.http import Http404
from ninja import NinjaAPI, errors

from users.views import user
from auth.views import auth
from friendship.views import friends

api = NinjaAPI()

api.title = "Friendship Service API"
api.description = "Сервис, в котором можно добавлять в друзья."

api.add_router('/users', user)
api.add_router('/auth', auth)
api.add_router('/friends', friends)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/v1/', api.urls)
]


@api.exception_handler(Http404)
def not_found_errors(request, exc):
    return api.create_response(request, {"detail": str(exc)}, status=404)


@api.exception_handler(errors.ValidationError)
def validation_errors(request, exc):
    return api.create_response(request, {"detail": str(exc.errors)}, status=422)
