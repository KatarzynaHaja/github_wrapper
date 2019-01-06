
from django.db import models
from django.contrib.auth.models import User


class Repos(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=50)
    user =models.ManyToManyField(User)


class Issuses(models.Model):
    id = models.AutoField(primary_key=True)
    repo = models.ForeignKey(Repos, on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    body = models.TextField(max_length=500)
    label = models.CharField(max_length=100)
    milestone = models.CharField(max_length=100)
    assignee = models.CharField(max_length=100)


class Branches(models.Model):
    id = models.AutoField(primary_key=True)
    repo = models.ForeignKey(Repos, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
