from django.db import models
from django.db.models import Q


class HobbyCategory(models.Model):
    title = models.CharField(max_length=255)
    created_ts = models.DateTimeField(auto_now_add=True)
    updated_ts = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title


class RequestLogger(models.Model):
    user = models.CharField(max_length=255)
    method = models.CharField(max_length=10)
    request_path = models.CharField(max_length=255)
    body = models.TextField()
    created_ts = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.user
