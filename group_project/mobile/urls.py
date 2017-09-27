from django.conf.urls import url, include
from rest_framework import routers
from views import Register, UserLoginAPIView

router = routers.DefaultRouter()
router.register(r'register', Register, base_name='mobile_signup')

urlpatterns = [
    url(r'^', include(router.urls)),
    url(r'^login', UserLoginAPIView.as_view(), name='login')
]
