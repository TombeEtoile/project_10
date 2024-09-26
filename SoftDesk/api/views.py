from django.shortcuts import get_object_or_404
from rest_framework import viewsets, generics, permissions
from rest_framework.permissions import IsAuthenticated
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from django.contrib.auth import get_user_model

from .permissions import IsAuthorOrReadOnly, IsSelfOrReadOnly
from .models import CustomUser, Contributor, Project, Issue, Comment
from .serializers import (
    UserSerializer, ContributorSerializer,
    ProjectListSerializer, ProjectDetailSerializer,
    IssueListSerializer, IssueLinkSerializer,
    CommentListSerializer,
    UserRegistrationSerializer,
    UserDeleteSerializer)


class PaginationView(PageNumberPagination):
    page_size = 3
    page_size_query_param = 'page_size'
    max_page_size = 100


'''
class SignupViewSet(APIView):

    """
    Create User. Return 201 code if successfully created
    """

    def post(self, request):
        serializer = UserSignupSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
'''


class UserViewSet(viewsets.ModelViewSet):

    permission_classes = (IsAuthenticated,)
    queryset = CustomUser.objects.all()
    serializer_class = UserSerializer
    pagination_class = PaginationView


class ContributorViewSet(viewsets.ModelViewSet):

    permission_classes = (IsAuthenticated,)
    queryset = Contributor.objects.all()
    serializer_class = ContributorSerializer
    pagination_class = PaginationView


class ProjectViewSet(viewsets.ModelViewSet):

    permission_classes = (IsAuthenticated, IsAuthorOrReadOnly)
    queryset = Project.objects.all()
    pagination_class = PaginationView

    serializer_class = ProjectListSerializer
    detail_serializer_class = ProjectDetailSerializer

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

    def get_serializer_class(self):
        if self.action == 'retrieve':
            return self.detail_serializer_class
        return super().get_serializer_class()


class ProjectDetailViewSet(generics.RetrieveAPIView):

    permission_classes = (IsAuthenticated, IsAuthorOrReadOnly)
    queryset = Project.objects.all()
    serializer_class = ProjectDetailSerializer


class IssueViewSet(viewsets.ModelViewSet):

    permission_classes = (IsAuthenticated, IsAuthorOrReadOnly)
    queryset = Issue.objects.all()
    serializer_class = IssueListSerializer
    pagination_class = PaginationView

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


class IssueDetailViewSet(generics.RetrieveAPIView):

    permission_classes = (IsAuthenticated, IsAuthorOrReadOnly)
    queryset = Issue.objects.all()
    serializer_class = IssueLinkSerializer


class CommentViewSet(viewsets.ModelViewSet):

    permission_classes = (IsAuthenticated, IsAuthorOrReadOnly)
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


User = get_user_model()


class UserDeleteView(generics.DestroyAPIView):
    permission_classes = [permissions.IsAuthenticated, IsSelfOrReadOnly]
    serializer_class = UserDeleteSerializer

    def get_object(self):
        # Récupère l'utilisateur en fonction de l'ID passé dans l'URL
        print("test")
        user = get_object_or_404(CustomUser, pk=self.kwargs['pk'])
        return user

    def destroy(self, request, *args, **kwargs):
        user = self.get_object()  # Récupère l'utilisateur à supprimer

        # Vérifie si l'utilisateur connecté correspond à l'utilisateur à supprimer
        if user != request.user.pk:
            return Response(
                {"detail": "Vous ne pouvez supprimer que votre propre compte."},
                status=status.HTTP_403_FORBIDDEN  # Refuse la requête avec une erreur 403
            )

        user.delete()  # Supprime cet utilisateur
        return Response(
            {"detail": "Votre compte et toutes les données associées ont été supprimés avec succès."},
            status=status.HTTP_204_NO_CONTENT
        )

