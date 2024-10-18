from django.urls import path, include
from rest_framework.routers import DefaultRouter

from users.views import UserViewSet, UserSignup, GetToken

router_v1 = DefaultRouter()
#  router_v1.register('users/me', UserMeViewSet, basename='me')
router_v1.register('users', UserViewSet, basename='user')

urlpatterns_v1 = [
    path('', include(router_v1.urls)),
]

authentication_patterns = [
    path('auth/token/', GetToken.as_view(), name='token'),
    path('auth/signup/', UserSignup.as_view(), name='signup')
]


urlpatterns = [
    path('v1/', include(urlpatterns_v1)),
    path('v1/', include(authentication_patterns)),
]
