from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated
from .models import Project, Issues, Comments
from .serializers import ProjectSerializer, IssuesSerializer, CommentsSerializer


class ProjectViewSet(ModelViewSet):

    queryset = Project.objects.all()
    serializer_class = ProjectSerializer
    permission_classes = (IsAuthenticated, )
    filterset_fields = ['author', 'contributor', 'type']
    search_fields = ['name']


class IssuesViewSet(ModelViewSet):

    queryset = Issues.objects.all()
    serializer_class = IssuesSerializer
    permission_classes = (IsAuthenticated, )
    filterset_fields = ['author', 'contributor', 'type', 'collaborators', 'progression']
    search_fields = ['name']


class CommentsViewSet(ModelViewSet):

    queryset = Comments.objects.all()
    serializer_class = CommentsSerializer
    permission_classes = (IsAuthenticated, )
    filterset_fields = ['author', 'contributor']
    search_fields = ['name']
