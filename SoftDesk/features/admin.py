from django.contrib import admin
from django.db import models
from .models import Project, Issues, Comments


class ProjectAdmin(admin.ModelAdmin):
    list_display = ('author', 'contributor', 'type', 'created_time')


class IssuesAdmin(admin.ModelAdmin):
    list_display = ('author', 'contributor', 'type', 'collaborators', 'progression', 'created_time')


class CommentsAdmin(admin.ModelAdmin):
    list_display = ('author', 'contributor', 'created_time')


# admin.site.register(Project, ProjectAdmin)
# admin.site.register(Issues, IssuesAdmin)
# admin.site.register(Comments, CommentsAdmin)
