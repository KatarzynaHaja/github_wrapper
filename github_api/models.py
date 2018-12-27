
from django.db import models
from django.contrib.auth.models import  AbstractBaseUser, BaseUserManager

class MyUserManager(BaseUserManager):
    def create_user(self,name, email,github_name, github_password, password):
        email = self.normalize_email(email)
        user = self.model(name= name, email=email, github_name=github_name, github_password=github_password)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, name, email,github_name, github_password, password):
        user = self.create_user(name = name, email=email, github_password=github_password,
                                github_name=github_name,password=password)
        user.is_superuser = True
        user.is_admin = True
        user.save(using=self._db)
        return user

class MyUser(AbstractBaseUser):
    name = models.CharField(max_length=32, unique=True)
    email = models.EmailField(max_length=32)
    github_name = models.CharField(max_length=100)
    github_password = models.CharField(max_length=50)
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)

    objects = MyUserManager()
    USERNAME_FIELD = 'name'


    def has_perm(self, perm, obj=None):
        return True

    def has_module_perms(self, app_label):
        return True

    @property
    def is_staff(self):
        return self.is_admin



class Repos(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=50)


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
