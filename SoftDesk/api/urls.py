from rest_framework import routers
from django.urls import path, include
from .views import (UserViewSet, ContributorViewSet,
                    ProjectViewSet, ProjectDetailViewSet,
                    IssueViewSet, IssueDetailViewSet,
                    CommentViewSet,
                    UserRegistrationView,
                    UserDeleteView)

router = routers.DefaultRouter()
router.register('user', UserViewSet, basename='user')
router.register('contributor', ContributorViewSet, basename='contributor')
router.register('project', ProjectViewSet, basename='project')
router.register('issue', IssueViewSet, basename='issue')
router.register('comment', CommentViewSet, basename='comment')

urlpatterns = [
    path('', include(router.urls)),
    path('register/', UserRegistrationView.as_view(), name='user-registration'),
    path('project/<int:pk>/', ProjectDetailViewSet.as_view(), name='project-detail'),
    path('issue/<int:pk>/', IssueDetailViewSet.as_view(), name='issue-detail'),
    path('user/delete/<int:pk>/', UserDeleteView.as_view(), name='user-delete'),
]
