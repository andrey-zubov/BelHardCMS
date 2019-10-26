from django.contrib import admin

from recruit.models import (Recruit, RecruitExperience, RecruitEducation, RecruitSkills)


# TeamRome
class InlineRecruitSkills(admin.TabularInline):
    model = RecruitSkills


# TeamRome
class InlineRecruitEducation(admin.TabularInline):
    model = RecruitExperience


# TeamRome
class InlineRecruitExperience(admin.TabularInline):
    model = RecruitEducation


# TeamRome
class RecruitAdmin(admin.ModelAdmin):
    model = Recruit
    inlines = [InlineRecruitEducation, InlineRecruitExperience, InlineRecruitSkills]


# TeamRome
admin.site.register(Recruit, RecruitAdmin)
