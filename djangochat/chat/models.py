from django.db import models
from django.contrib.auth.models import User


class Thread(models.Model):
    participants = models.ManyToManyField(User, blank=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)


class Message(models.Model):
    # In sender on_delete parameter is SET to SET_NULL to avoid deleting message if user is deleted
    sender = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    text = models.TextField(max_length=2048, blank=True)
    thread = models.ForeignKey(Thread, on_delete=models.CASCADE, blank=True)
    created = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)

    class Meta:
        ordering = ('-created',)

