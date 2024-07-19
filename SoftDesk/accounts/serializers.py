from rest_framework import serializers
from django.contrib.auth.models import User
from .models import UserProfile, Contributor
from features.serializers import ProjectSerializer


class UserProfileSerializer(serializers.ModelSerializer):

    class Meta:
        model = UserProfile
        exclude = ('id', )


class UserSerializer(serializers.ModelSerializer):

    profile = UserProfileSerializer(source='userprofile')

    class Meta:
        model = User
        fields = ('id', 'username', 'date_joined', 'user_permissions', 'profile')
        # 'first_name', 'last_name', 'email', 'last_login'


class ContributorSerializer(serializers.ModelSerializer):

    user = UserSerializer()
    project = ProjectSerializer()

    class Meta:
        model = Contributor
        fields = '__all__'
