from django.db import models

class User(models.Model):
    name = models.CharField(max_length=50)
    password = models.CharField(max_length=50)

class log(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, name='user')
    file_name = models.CharField(max_length=100)
    type = models.CharField(max_length=10)

