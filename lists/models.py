import uuid
from django.urls import reverse
from django.contrib import auth
from django.db import models
from django.contrib.auth import authenticate, login

auth.signals.user_logged_in.disconnect(auth.models.update_last_login)
# Create your models here.

class List(models.Model):
     def get_absolute_url(self):
        return reverse('view_list', args=[self.id])

class Item(models.Model):
    text = models.TextField(default="")
    list = models.ForeignKey(List, default=None, on_delete=models.CASCADE)

    class Meta:
        ordering = ('id',)
        unique_together = ('list', 'text')

    def __str__(self):
        return self.text