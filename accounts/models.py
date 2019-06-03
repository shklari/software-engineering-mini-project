from django.db import models

# Create your models here.

# hirarchy in models
class User(models.Model):

    username = models.CharField(max_length=50)
    password = models.CharField(max_length=50)


class Owner(models.Model):

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    store_name = models.CharField(max_length=50)
