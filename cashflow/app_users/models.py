from django.contrib.auth.models import AbstractUser
from django.db import models
from django.urls import reverse


class CustomUser(AbstractUser):
    tin = models.CharField(unique=True, max_length=12, verbose_name='TIN')
    balance = models.DecimalField(max_digits=12, decimal_places=2, verbose_name='Balance', default=0)

    def get_absolute_url(self):
        return reverse('user_profile_url')
