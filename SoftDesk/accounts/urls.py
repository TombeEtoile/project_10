from rest_framework import routers
from django.urls import path, include

from .views import UserViewSet, ContributorViewSet


# router = routers.DefaultRouter()
# router.register('user', UserViewSet, basename='user')
# router.register('contributor', ContributorViewSet, basename='contributor')

urlpatterns = [
    # path('', include(router.urls)),
]
