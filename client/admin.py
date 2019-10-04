from django.contrib import admin
from .models import *


class Subtasks_Inline(admin.StackedInline):

    model = SubTasks
    extra = 1


class Tasks_Admin(admin.ModelAdmin):

    inlines = [Subtasks_Inline]


class VacancyAdmin(admin.ModelAdmin):

    list_display = (
        'state', 'organization', 'slug', 'address', 'employment', 'description',
        'skills', 'requirements', 'duties', 'conditions',
    )
    list_display_links = (
        'state', 'organization', 'description',
    )
    search_fields = (
        'state', 'organization', 'description',
    )


class ResumeAdmin(admin.ModelAdmin):

    list_display = (
        'state', 'slug',
    )
    list_display_links = (
        'state', 'slug',
    )
    search_fields = (
        'state', 'slug',
    )

## Test settings for Poland
class SettingsAdmin(admin.ModelAdmin):

    list_display = ('name_setting', )
    list_display_links = ('name_setting', )
    search_fields = ('name_setting', )


admin.site.register(Settings, SettingsAdmin)
admin.site.register(Vacancy, VacancyAdmin)
admin.site.register(Resume, ResumeAdmin)
admin.site.register(Help)


admin.site.register(Opinion)
admin.site.register(Answer)
admin.site.register(Chat)
admin.site.register(Tasks, Tasks_Admin)

# Register your models here.
