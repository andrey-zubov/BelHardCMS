from django.contrib import admin
from .models import *

class Subtasks_Inline(admin.StackedInline):
    model = SubTasks
    extra = 1

class Tasks_Admin(admin.ModelAdmin):
    inlines = [Subtasks_Inline]
    readonly_fields = ['endtime']


admin.site.register(Opinion)
admin.site.register(Answer)
admin.site.register(Chat)
admin.site.register(Tasks, Tasks_Admin)

# Register your models here.
