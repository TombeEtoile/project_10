from rest_framework.serializers import ModelSerializer
from .models import Project, Issues, Comments
# from accounts.serializers import UserSerializer


class ProjectSerializer(ModelSerializer):
    # author = UserSerializer(read_only=True)
    # contributors = UserSerializer(many=True, read_only=True)

    class Meta:
        model = Project
        fields = '__all__'


class IssuesSerializer(ModelSerializer):

    class Meta:
        model = Issues
        fields = '__all__'


class CommentsSerializer(ModelSerializer):

    class Meta:
        model = Comments
        fields = '__all__'
