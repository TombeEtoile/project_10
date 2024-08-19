from rest_framework import serializers
from django.contrib.auth.models import User

from .models import CustomUser, Project, Issue, Comment, Contributor


class CustomUserSerializer(serializers.ModelSerializer):

    class Meta:
        model = CustomUser
        fields = ('age', 'can_be_contacted', 'can_data_be_shared')


class UserSerializer(serializers.ModelSerializer):

    profile = CustomUserSerializer(source='customuser')

    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'date_joined', 'profile')

    def create(self, validated_data):
        profile_data = validated_data.pop('customuser')
        user = User.objects.create(**validated_data)
        CustomUser.objects.create(accounts=user, **profile_data)
        return user


class ProjectListSerializer(serializers.ModelSerializer):

    author = UserSerializer(read_only=True)
    contributors = UserSerializer(many=True, read_only=True)

    class Meta:
        model = Project
        fields = ('id', 'title', 'type', 'author', 'contributors')


class ContributorSerializer(serializers.ModelSerializer):
    user = UserSerializer()
    project = ProjectListSerializer()

    class Meta:
        # model = User
        model = Contributor
        fields = '__all__'
        # depth = 1 A CHECK


class IssueListSerializer(serializers.ModelSerializer):

    project = ProjectListSerializer()
    author = UserSerializer()
    assignee = UserSerializer()

    class Meta:
        model = Issue
        fields = '__all__'


class CommentListSerializer(serializers.ModelSerializer):

    # issue = IssueSerializerT(read_only=True)
    issue = serializers.PrimaryKeyRelatedField(queryset=Issue.objects.all())
    author = UserSerializer(read_only=True)

    class Meta:
        model = Comment
        exclude = ('uuid', )


'''
class ProjectDetailSerializer(serializers.ModelSerializer):

    issues = serializers.SerializerMethodField()

    class Meta:
        model = Project
        fields = ['id', 'title', 'description', 'type', 'author', 'issues']
    
    
    @staticmethod
    def get_issues(instance):
        queryset = Issue.objects.filter(project_id=instance.id)
        return IssueListSerializer(queryset, many=True).data
'''

'''
class IssueDetailSerializer(serializers.ModelSerializer):

    comments = serializers.SerializerMethodField()

    class Meta:
        model = Issue
        fields = ['id', 'created_time', 'title', 'description', 'priority', 'type', 'status', 'author', 'assignee',
                  'project', 'comments']

    
    def get_comments(self, instance):
        queryset = Comment.objects.filter(issue_id=instance.id)
        return CommentListSerializer(queryset, many=True).data
'''


class UserRegistrationSerializer(serializers.ModelSerializer):
    age = serializers.IntegerField(write_only=True)
    can_be_contacted = serializers.BooleanField(write_only=True)
    can_data_be_shared = serializers.BooleanField(write_only=True)

    class Meta:
        model = User
        fields = ('username', 'password', 'email', 'age', 'can_be_contacted', 'can_data_be_shared')
        extra_kwargs = {'password': {'write_only': True}}

    @staticmethod
    def validate_age(value):
        if value < 16:
            raise serializers.ValidationError("You are not old enough to register. You must be at least 16 years old")
        return value

    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            password=validated_data['password']
        )
        CustomUser.objects.create(
            accounts=user,
            age=validated_data['age'],
            can_be_contacted=validated_data['can_be_contacted'],
            can_data_be_shared=validated_data['can_data_be_shared']
        )
        return user
