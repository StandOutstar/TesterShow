import datetime

from django.db import models


# Create your models here.
from django.utils import timezone


class Job(models.Model):
    name = models.CharField(max_length=100)
    finish_date = models.DateTimeField('date finished')

    def __str__(self):
        return f"{self.name}"

    def was_finished_recently(self):
        now = timezone.now()
        return now > self.finish_date >= now - datetime.timedelta(days=1)