from django.db import models
# from django.contrib.auth.models import User
# import uuid


class Project(models.Model):
    TYPE_CHOICES = [
        ('backend', 'Back-End'),
        ('frontend', 'Front-End'),
        ('ios', 'iOS'),
        ('android', 'Android'),
    ]

    author = models.CharField(max_length=255)
    # author = models.ForeignKey(User, related_name='authored_projects', on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    contributor = models.CharField(max_length=255)
    # contributors = models.ManyToManyField(User, related_name='contributed_projects', through='Contributor')
    type = models.CharField(max_length=50, choices=TYPE_CHOICES)
    created_time = models.fields.DateTimeField(auto_now_add=True)

    '''
    author = models.ForeignKey(User, related_name='authored_projects', on_delete=models.CASCADE)
    contributors = models.ManyToManyField(User, related_name='contributed_projects', through='Contributor')
    type = models.CharField(max_length=50, choices=TYPE_CHOICES)
    created_time = models.DateTimeField(auto_now_add=True)
    '''

    def __str__(self):
        return self.name


class Issues(models.Model):
    TYPE_CHOICES = [
        ('backend', 'Back-End'),
        ('frontend', 'Front-End'),
        ('ios', 'iOS'),
        ('android', 'Android'),
    ]

    COLLABORATOR_CHOICES = [
        ('low', 'Low'),
        ('medium', 'Medium'),
        ('hard', 'Hard'),
        ('bug', 'Bug'),
        ('features', 'Features'),
        ('task', 'Task'),
    ]

    PROGRESSION_CHOICES = [
        ('to_do', 'To Do'),
        ('in_progress', 'In Progress'),
        ('finished', 'Finished'),
    ]

    author = models.CharField(max_length=255)
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    contributor = models.ForeignKey('auth.User', on_delete=models.CASCADE)
    type = models.CharField(max_length=50, choices=TYPE_CHOICES)
    collaborators = models.CharField(max_length=50, choices=COLLABORATOR_CHOICES)
    progression = models.CharField(max_length=50, choices=PROGRESSION_CHOICES, default='to_do')
    created_time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


class Comments(models.Model):
    author = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    contributor = models.ForeignKey('auth.User', on_delete=models.CASCADE)
    # link
    created_time = models.fields.DateTimeField(auto_now_add=True)
