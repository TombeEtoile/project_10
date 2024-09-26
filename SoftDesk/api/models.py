from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.exceptions import ValidationError
import uuid


class CustomUser(AbstractUser):

    # accounts = models.OneToOneField(User, on_delete=models.CASCADE) --> (inutile grâce à AbstractUser)
    age = models.IntegerField(default=18)
    can_be_contacted = models.BooleanField(default=True)
    can_data_be_shared = models.BooleanField(default=True)

    def clean(self):
        if self.age < 15:
            raise ValidationError("L'utilisateur doit avoir 15 ans minimum.")

    def __str__(self):
        return self.username


class Project(models.Model):

    PROJECT_TYPE = [
        ('backend', 'Back-End'),
        ('frontend', 'Front-End'),
        ('ios', 'iOS'),
        ('android', 'Android'),
    ]

    author = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    title = models.CharField(max_length=35)
    description = models.TextField()
    type = models.CharField(max_length=50, choices=PROJECT_TYPE)
    contributors = models.ManyToManyField(CustomUser, related_name='project_contributors', through='Contributor')
    created_time = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        Contributor.objects.get_or_create(user=self.author, project=self, defaults={'role': 'Author'})

    def __str__(self):
        return self.title


class Contributor(models.Model):

    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    role = models.CharField(max_length=35)

    class Meta:
        unique_together = ('project', 'user')


class Issue(models.Model):
    TYPE_CHOICES = [
        ('bug', 'Bug'),
        ('features', 'Features'),
        ('task', 'Task'),
    ]

    PRIORITY_CHOICES = [
        ('low', 'Low'),
        ('medium', 'Medium'),
        ('hard', 'Hard'),
    ]

    STATUS_CHOICES = [
        ('to_do', 'To Do'),
        ('in_progress', 'In Progress'),
        ('finished', 'Finished'),
    ]

    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='issues')
    author = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='issue_author')
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    assignee = models.ForeignKey(CustomUser, on_delete=models.SET_NULL, null=True, blank=True, related_name='assigned_issue')
    type = models.CharField(max_length=50, choices=TYPE_CHOICES)
    priority = models.CharField(max_length=50, choices=PRIORITY_CHOICES)
    status = models.CharField(max_length=50, choices=STATUS_CHOICES, default='to_do')
    created_time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title


class Comment(models.Model):

    issue = models.ForeignKey(Issue, on_delete=models.CASCADE, related_name='comment')
    author = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='comment_author')
    description = models.TextField(max_length=500)
    uuid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    created_time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Comment by {self.author.username} on {self.issue.title}"

