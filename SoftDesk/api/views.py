from rest_framework import viewsets
from django.contrib.auth.models import User
from rest_framework.permissions import IsAuthenticated

from .models import ContributorT, ProjectT, IssueT, CommentT
from .serializers import UserSerializerT, ContributorSerializerT, ProjectSerializerT, IssueSerializerT, CommentSerializerT


class UserViewSet(viewsets.ModelViewSet):

    permission_classes = (IsAuthenticated,)
    queryset = User.objects.all()
    serializer_class = UserSerializerT


class ContributorViewSet(viewsets.ModelViewSet):

    permission_classes = (IsAuthenticated,)
    queryset = ContributorT.objects.all()
    serializer_class = ContributorSerializerT


class ProjectViewSet(viewsets.ModelViewSet):

    permission_classes = (IsAuthenticated,)
    queryset = ProjectT.objects.all()
    serializer_class = ProjectSerializerT


class IssueViewSet(viewsets.ModelViewSet):

    permission_classes = (IsAuthenticated,)
    queryset = IssueT.objects.all()
    serializer_class = IssueSerializerT


class CommentViewSet(viewsets.ModelViewSet):

    permission_classes = (IsAuthenticated, )
    queryset = CommentT.objects.all()
    serializer_class = CommentSerializerT

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)
