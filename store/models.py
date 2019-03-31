from django.db import models

class Genre(models.Model):
    topic  = models.CharField(max_length =255)