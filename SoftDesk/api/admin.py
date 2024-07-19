from django.contrib import admin
from django.contrib.auth.admin import UserAdmin, User

from .models import ProjectT, ContributorT, CustomUserT, IssueT, CommentT


class CustomUserInLine(admin.StackedInline):

    model = CustomUserT


class UserProfileAdmin(UserAdmin):

    inlines = (CustomUserInLine, )


class ProjectAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'type', 'created_time')
    search_fields = ('name', 'author__username', 'type')
    list_filter = ('type',)


class ContributorAdmin(admin.ModelAdmin):
    list_display = ('user', 'project', 'role')
    search_fields = ('user__username', 'project__name', 'role')
    list_filter = ('role', 'project')


class IssueAdmin(admin.ModelAdmin):
    list_display = ('author', 'title', 'type', 'priority', 'status')
    search_fields = ('user__username', 'type', 'priority', 'status')
    list_filter = ('type', 'priority', 'status')


class CommentAdmin(admin.ModelAdmin):
    list_display = ('author', 'issue', 'created_time')
    search_fields = ('author', 'description')
    list_filter = ('author', 'description', 'created_time')


admin.site.unregister(User)
admin.site.register(User, UserProfileAdmin)
admin.site.register(ProjectT, ProjectAdmin)
admin.site.register(ContributorT, ContributorAdmin)
admin.site.register(IssueT, IssueAdmin)
admin.site.register(CommentT, CommentAdmin)
