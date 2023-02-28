from django.db import models
from django.contrib.auth.models import User
from .custom_exceptions import MaxLengthParticipantsException


class Thread(models.Model):
    participants = models.ManyToManyField(User, blank=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    # У Thread можливо лише 2 користувача(participant'а)
    # def save(self, *args, **kwargs):
    #     thread = super().save(*args, **kwargs)
    #     if len(thread.participants) > 2:
    #         raise MaxLengthParticipantsException("The max length of participants in current thread")
    #     return thread


class Message(models.Model):
    # In sender on_delete parameter is SET to SET_NULL to avoid deleting message if user is deleted
    sender = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    text = models.TextField(max_length=2048, blank=True)
    thread = models.ForeignKey(Thread, on_delete=models.CASCADE, blank=True)
    created = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)

    class Meta:
        ordering = ('-created',)

