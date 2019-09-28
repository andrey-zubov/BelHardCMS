from django.contrib import admin

from .models import *


class Subtasks_Inline(admin.StackedInline):
    model = SubTasks
    extra = 1


class Tasks_Admin(admin.ModelAdmin):
    inlines = [Subtasks_Inline]


admin.site.register(Opinion)
admin.site.register(Answer)
admin.site.register(Chat)
admin.site.register(Tasks, Tasks_Admin)


class SexAdmin(admin.ModelAdmin):
    model = Sex


class CitizenshipAdmin(admin.ModelAdmin):
    model = Citizenship


class FamilyStateAdmin(admin.ModelAdmin):
    model = FamilyState


class ChildrenAdmin(admin.ModelAdmin):
    model = Children


class CityAdmin(admin.ModelAdmin):
    model = City


class EducationWordAdmin(admin.ModelAdmin):
    model = EducationWord


class SkillsWordAdmin(admin.ModelAdmin):
    model = SkillsWord


class SphereAdmin(admin.ModelAdmin):
    model = Sphere


class CvWordAdmin(admin.ModelAdmin):
    model = CvWord


class EmploymentAdmin(admin.ModelAdmin):
    model = Employment


class TimeJobAdmin(admin.ModelAdmin):
    model = TimeJob


class TypeSalaryAdmin(admin.ModelAdmin):
    model = TypeSalary


admin.site.register(Sex, SexAdmin)
admin.site.register(Citizenship, CitizenshipAdmin)
admin.site.register(FamilyState, FamilyStateAdmin)
admin.site.register(Children, ChildrenAdmin)
admin.site.register(City, CityAdmin)
admin.site.register(EducationWord, EducationWordAdmin)
admin.site.register(SkillsWord, SkillsWordAdmin)
admin.site.register(Sphere, SphereAdmin)
admin.site.register(CvWord, CvWordAdmin)
admin.site.register(Employment, EmploymentAdmin)
admin.site.register(TimeJob, TimeJobAdmin)
admin.site.register(TypeSalary, TypeSalaryAdmin)
