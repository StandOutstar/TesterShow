import datetime

from django.contrib import admin
from django.db import models


# Create your models here.
from django.utils import timezone


class Job(models.Model):
    name = models.CharField(max_length=100)
    finish_date = models.DateTimeField('date finished')

    def __str__(self):
        return f"{self.name}"

    @admin.display(
        boolean=True,
        ordering='finish_date',
        description='Finished recently?',
    )
    def was_finished_recently(self):
        now = timezone.now()
        return now > self.finish_date >= now - datetime.timedelta(days=1)