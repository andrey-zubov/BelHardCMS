from django.db import models
from django.contrib.auth import get_user_model

RecruiterModel = get_user_model()


class Recruiter(models.Model):
    recruiter = models.OneToOneField(RecruiterModel, on_delete=models.CASCADE)




