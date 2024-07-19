from django.db import models
from django.contrib.auth.models import User
from features.models import Project


class UserProfile(models.Model):

    accounts = models.OneToOneField(User, on_delete=models.CASCADE, blank=True, null=True)

    age = models.IntegerField()
    can_be_contacted = models.BooleanField()
    can_data_be_shared = models.BooleanField()


class Contributor(models.Model):

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='contributors_set')
    role = models.CharField(max_length=50)

    class Meta:
        unique_together = ('user', 'project')

    def __str__(self):
        return f"{self.user.username} - {self.project.name}"


