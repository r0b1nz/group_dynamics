from django.conf.urls import url, include
from rest_framework import routers
from views import Register

router = routers.DefaultRouter()
router.register(r'register', Register, base_name='mobile_signup')

urlpatterns = [
    url(r'^', include(router.urls)),
    # url(r'^signup/', Register, name='register')
]


# Wire up our API using automatic URL routing.
# Additionally, we include login URLs for the browsable API.
# urlpatterns = [
#     url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework'))
#
