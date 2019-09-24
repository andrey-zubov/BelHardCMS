from django.contrib import admin
from .models import Opinion, Answer, Chat, Tasks, Subtasks

class Subtasks_Inline(admin.StackedInline):
    model = Subtasks
    extra = 1

class Tasks_Admin(admin.ModelAdmin):
    inlines = [Subtasks_Inline]

admin.site.register(Opinion)
admin.site.register(Answer)
admin.site.register(Chat)
admin.site.register(Tasks, Tasks_Admin)
#admin.site.register(Subtasks)
# Register your models here.
