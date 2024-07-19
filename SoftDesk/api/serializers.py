from rest_framework import serializers
from django.contrib.auth.models import User

from .models import CustomUserT, ProjectT, IssueT, CommentT


class CustomUserSerializerT(serializers.ModelSerializer):

    class Meta:
        model = CustomUserT
        fields = ('age', 'can_be_contacted', 'can_data_be_shared')


class UserSerializerT(serializers.ModelSerializer):

    profile = CustomUserSerializerT(source='customusert')

    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'date_joined', 'profile')


class ProjectSerializerT(serializers.ModelSerializer):

    author = UserSerializerT(read_only=True)
    contributors = UserSerializerT(many=True, read_only=True)

    class Meta:
        model = ProjectT
        fields = ('author', 'title', 'description', 'type', 'contributors', 'created_time')


class ContributorSerializerT(serializers.ModelSerializer):
    user = UserSerializerT()
    project = ProjectSerializerT()

    class Meta:
        model = User
        fields = '__all__'


class IssueSerializerT(serializers.ModelSerializer):

    project = ProjectSerializerT()
    author = UserSerializerT()
    assignee = UserSerializerT()

    class Meta:
        model = IssueT
        fields = '__all__'


class CommentSerializerT(serializers.ModelSerializer):

    # issue = IssueSerializerT(read_only=True)
    issue = serializers.PrimaryKeyRelatedField(queryset=IssueT.objects.all())
    author = UserSerializerT(read_only=True)

    class Meta:
        model = CommentT
        exclude = ('uuid', )
