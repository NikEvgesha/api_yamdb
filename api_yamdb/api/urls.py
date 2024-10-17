from django.urls import path, include
from rest_framework.routers import DefaultRouter

from users.views import UserViewSet

router_v1 = DefaultRouter()
router_v1.register('users', UserViewSet, basename='user')


urlpatterns_v1 = [
    path('', include(router_v1.urls)),
    #  path('auth/token', ...),
    #  path('auth/signup', ...)
]

urlpatterns = [
    path('v1/', include(urlpatterns_v1))
]
