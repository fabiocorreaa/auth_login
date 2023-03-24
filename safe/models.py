from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class SecretWord(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='User')
    name = models.CharField(max_length=150, verbose_name='Name of the site/password')
    url = models.CharField(max_length=150, verbose_name='URL')
    pass_word = models.CharField(max_length=500, verbose_name='Password')

    def __str__(self):
        return self.name