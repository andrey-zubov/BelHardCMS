from django.http import HttpResponse
from django.views.generic import TemplateView


class SkillsDataList(TemplateView):
    def get(self, request, *args, **kwargs):
        print('SkillsDataList.GET: %s' % request.GET)
        response = 0
        return HttpResponse(response)
