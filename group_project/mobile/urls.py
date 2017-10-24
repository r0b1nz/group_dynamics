from django.conf.urls import url, include
from .views import UserCreateAPIView, UserLoginAPIView, assign_groups
# from rest_framework import routers

# router = routers.DefaultRouter()
# router.register(r'register', Register, base_name='mobile_signup')

urlpatterns = [
    # url(r'^', include(router.urls)),
    url(r'^$', UserLoginAPIView.as_view(), name='login'),
    url(r'^login', UserLoginAPIView.as_view(), name='login'),
    url(r'^register', UserCreateAPIView.as_view(), name='register'),
    url(r'^groups', assign_groups, name='groups')
]
