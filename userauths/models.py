from django.db import models

from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    email = models.EmailField(unique=True)
    username = models.CharField(max_length =100)
    bio = models.CharField(max_length = 200, default = "A person driven by art. That is me!")
    USERNAME_FIELD="email"
    REQUIRED_FIELDS = ['username'] # necessary to avoid errors when using createsuperuser

    def __str__(self):
        return self.username