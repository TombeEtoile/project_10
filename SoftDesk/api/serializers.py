from rest_framework import serializers
from django.contrib.auth import get_user_model

from .models import CustomUser, Project, Issue, Comment, Contributor


'''
class UserSignupSerializer(ModelSerializer):

    tokens = SerializerMethodField()

    class Meta:
        model = User
        fields = ['id', 'first_name', 'last_name', 'email', 'password', 'tokens']

    def validate_email(self, value: str) -> str:
        if User.objects.filter(email=value).exists():
            raise ValidationError("User already exists")
        return value

    def validate_password(self, value: str) -> str:
        if value is not None:
            return make_password(value)
        raise ValidationError("Password is empty")

    def get_tokens(self, user: User) -> dict:
        tokens = RefreshToken.for_user(user)
        data = {
            "refresh": str(tokens),
            "access": str(tokens.access_token)
        }
        return data
'''


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = CustomUser
        fields = ('id', 'username', 'email', 'date_joined', 'age', 'can_be_contacted', 'can_data_be_shared')

    def create(self, validated_data):
        profile_data = validated_data.pop('customuser')
        user = CustomUser.objects.create(**validated_data)
        CustomUser.objects.create(accounts=user, **profile_data)
        return user


class ProjectListSerializer(serializers.ModelSerializer):

    url = serializers.HyperlinkedIdentityField(view_name='project-detail', lookup_field='pk')

    author = serializers.StringRelatedField()
    # contributors = serializers.PrimaryKeyRelatedField(many=True, read_only=True, source='project_contributors')

    class Meta:
        model = Project
        fields = ('id', 'title', 'type', 'author', 'url')


class ProjectDetailSerializer(serializers.ModelSerializer):

    author = serializers.StringRelatedField()
    contributors = serializers.PrimaryKeyRelatedField(many=True, read_only=True, source='project_contributors')

    class Meta:
        model = Project
        fields = ('id', 'title', 'type', 'author', 'contributors', 'created_time')

    def get_issues(self, obj):
        issues = obj.issues.all()  # Utilise le related_name='issues' pour récupérer les issues associées
        return IssueLinkSerializer(issues, many=True, context=self.context).data


class ContributorSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField()
    project = serializers.StringRelatedField()

    class Meta:
        model = Contributor
        fields = ('user', 'project', 'role')
        # depth = 1 A CHECK


class IssueListSerializer(serializers.ModelSerializer):
    project = serializers.PrimaryKeyRelatedField(read_only=True)
    author = serializers.StringRelatedField()
    assignee = serializers.StringRelatedField()

    class Meta:
        model = Issue
        fields = ('id', 'title', 'type', 'priority', 'status', 'project', 'author', 'assignee', 'created_time')


class CommentListSerializer(serializers.ModelSerializer):
    issue = serializers.PrimaryKeyRelatedField(queryset=Issue.objects.all())
    author = serializers.StringRelatedField()

    class Meta:
        model = Comment
        exclude = ('uuid', )


class IssueLinkSerializer(serializers.ModelSerializer):
    url = serializers.HyperlinkedIdentityField(view_name='issue-detail', lookup_field='pk')

    class Meta:
        model = Issue
        fields = ('id', 'title', 'author', 'url')


# REGISTRATION
class UserRegistrationSerializer(serializers.ModelSerializer):
    age = serializers.IntegerField(write_only=True)
    can_be_contacted = serializers.BooleanField(write_only=True)
    can_data_be_shared = serializers.BooleanField(write_only=True)

    class Meta:
        model = CustomUser
        fields = ('username', 'password', 'email', 'age', 'can_be_contacted', 'can_data_be_shared')
        extra_kwargs = {'password': {'write_only': True}}

    @staticmethod
    def validate_age(value):
        if value < 15:
            raise serializers.ValidationError("You are not old enough to register. You must be at least 16 years old")
        return value

    def create(self, validated_data):
        user = CustomUser.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            password=validated_data['password'],
            age=validated_data['age'],
            can_be_contacted=validated_data['can_be_contacted'],
            can_data_be_shared=validated_data['can_data_be_shared']
        )
        return user


User = get_user_model()


class UserDeleteSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = []
