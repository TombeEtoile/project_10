from rest_framework import viewsets
from django.contrib.auth.models import User
from rest_framework.permissions import IsAuthenticated
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status

from .permissions import IsAuthorOrReadOnly
from .models import Contributor, Project, Issue, Comment
from .serializers import (
    UserSerializer, ContributorSerializer, ProjectListSerializer, IssueListSerializer, CommentListSerializer,
    UserRegistrationSerializer)


class PaginationView(PageNumberPagination):
    page_size = 3
    page_size_query_param = 'page_size'
    max_page_size = 100


class UserViewSet(viewsets.ModelViewSet):

    permission_classes = (IsAuthenticated,)
    queryset = User.objects.all()
    serializer_class = UserSerializer
    pagination_class = PaginationView


class ContributorViewSet(viewsets.ModelViewSet):

    permission_classes = (IsAuthenticated, IsAuthorOrReadOnly)
    # permission_classes = (IsAuthorOrReadOnly, )
    queryset = Contributor.objects.all()
    serializer_class = ContributorSerializer
    pagination_class = PaginationView


class ProjectViewSet(viewsets.ModelViewSet):

    permission_classes = (IsAuthenticated, IsAuthorOrReadOnly)
    # permission_classes = (IsAuthorOrReadOnly, )
    queryset = Project.objects.all()
    serializer_class = ProjectListSerializer
    pagination_class = PaginationView


class IssueViewSet(viewsets.ModelViewSet):

    permission_classes = (IsAuthenticated, IsAuthorOrReadOnly)
    # permission_classes = (IsAuthorOrReadOnly,)
    queryset = Issue.objects.all()
    serializer_class = IssueListSerializer
    pagination_class = PaginationView


class CommentViewSet(viewsets.ModelViewSet):

    permission_classes = (IsAuthenticated, IsAuthorOrReadOnly)
    # permission_classes = (IsAuthorOrReadOnly,)
    queryset = Comment.objects.all()
    serializer_class = CommentListSerializer
    pagination_class = PaginationView

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


class UserRegistrationView(APIView):
    def post(self, request, *args, **kwargs):
        serializer = UserRegistrationSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "User registered successfully"}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
