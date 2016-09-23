from __future__ import unicode_literals

from django.db import models


# Create your models here.
class MemberShip(models.Model):
    title = models.CharField(max_length=200)
    kind = models.IntegerField(default=0)


class User(models.Model):
    name = models.CharField(max_length=200)
    lastName = models.CharField(max_length=200)
    email = models.CharField(max_length=200)
    date = models.DateTimeField(auto_now=True)
    member = models.ForeignKey(MemberShip, on_delete=models.CASCADE)


class Photos(models.Model):
    title = models.CharField(max_length=200)
    desc = models.CharField(max_length=200)
    size = models.IntegerField()
    src = models.CharField(max_length=200)
    date = models.DateTimeField(auto_now=True)


class Background(models.Model):
    title = models.CharField(max_length=200)
    src = models.CharField(max_length=200)
    desc = models.CharField(max_length=200)


class Slides(models.Model):
    title = models.CharField(max_length=200)
    desc = models.CharField(max_length=200)
    speed = models.IntegerField()
    user = models.ManyToManyField(User)
    photo = models.ManyToManyField(Photos)
    date = models.DateTimeField(auto_now=True)
    background = models.ForeignKey(Background, on_delete=models.CASCADE)






