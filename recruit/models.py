from django.db import models
from client.models import Client
from django.contrib.auth import get_user_model

RecruiterModel = get_user_model()


class Recruiter(models.Model):
    recruiter = models.OneToOneField(RecruiterModel, on_delete=models.CASCADE)
    ownclient = models.ForeignKey(Client,on_delete=models.SET_NULL, null=True, blank=True)


