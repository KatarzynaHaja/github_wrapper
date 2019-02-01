
from django.db import models
from django.contrib.auth.models import User


class Repo(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=50)
    user =models.ManyToManyField(User)


class GitAuthentication(models.Model):
    id = models.AutoField(primary_key=True)
    access_token = models.CharField(max_length=200, unique=True)
    user = models.ManyToManyField(User)


class Issue(models.Model):
    id = models.AutoField(primary_key=True)
    repo = models.ForeignKey(Repo, on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    body = models.TextField(max_length=500)
    label = models.CharField(max_length=100)
    milestone = models.CharField(max_length=100, null=True)
    assignee = models.CharField(max_length=100)
    number = models.IntegerField(null=True)


class Branch(models.Model):
    id = models.AutoField(primary_key=True)
    repo = models.ForeignKey(Repo, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
