from django.shortcuts import render, get_object_or_404

from .models import CV, Client


# There is Poland's mixins #####################################################################
class ObjectResumeMixin:
    template = None

    def get(self, request, id_c):
        # client = get_object_or_404(Client, user_client=request.user)
        # resume = CV.objects.filter(client_cv=client).filter(id=id_c)
        resume = get_object_or_404(CV, id=id_c)

        return render(request, self.template, context={'resume': resume})

# End Poland ###################################################################################
