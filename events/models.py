from django.db.models import Model
from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User


class task(Model):
    user = models.ForeignKey(User, on_delete = models.CASCADE)
    title = models.CharField(max_length = 300)
    completed = models.BooleanField(default = False, blank=True)
    created_at = models.DateTimeField(default = timezone.now, blank=True)
    due_at = models.DateTimeField(blank=True, null=True)
    percentage_completed = models.PositiveIntegerField(default=0)
    remind_at = models.DateTimeField(blank = True, null=True)
    def __str__(self):
        return self.title


class users(Model):
    username = models.CharField(max_length=20)
    email = models.EmailField()
    password = models.CharField(max_length=20, blank = True)

    def __str__(self):
        return self.username