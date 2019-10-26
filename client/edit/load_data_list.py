import json

from django.http import HttpResponse
from django.views.generic import TemplateView

from client.models import (SkillsWord, EducationWord, CvWord)


# TeamRome
class SkillsDataList(TemplateView):
    def get(self, request, *args, **kwargs):
        # print('SkillsDataList.GET: %s' % request.GET)
        words = [i.skills_word for i in SkillsWord.objects.all()]
        json_data = json.dumps({'words': words}, ensure_ascii=False)
        return HttpResponse(json_data)


# TeamRome
class InstitutionDataList(TemplateView):
    def get(self, request, *args, **kwargs):
        # print('InstitutionDataList.GET: %s' % request.GET)
        words = [i.education_word for i in EducationWord.objects.all()]
        json_data = json.dumps({'words': words}, ensure_ascii=False)
        return HttpResponse(json_data)


# TeamRome
class CvPositionDataList(TemplateView):
    def get(self, request, *args, **kwargs):
        # print('CvPositionDataList.GET: %s' % request.GET)
        words = [i.position_word for i in CvWord.objects.all()]
        json_data = json.dumps({'words': words}, ensure_ascii=False)
        return HttpResponse(json_data)
