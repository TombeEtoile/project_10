from django.contrib import admin
from .models import UserProfile, Contributor
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User


class UserProfileInLine(admin.StackedInline):

    model = UserProfile


class UserProfileAdmin(UserAdmin):

    inlines = (UserProfileInLine, )


class ContributorAdmin(admin.ModelAdmin):
    list_display = ('project', 'user', 'role')
    search_fields = ('user__username', 'project__name', 'role')
    list_filter = ('role', 'project')


# admin.site.unregister(User)
# admin.site.register(User, UserProfileAdmin)
# admin.site.register(Contributor, ContributorAdmin)
