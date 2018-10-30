from django.db import models

# Create your models here.
#图书管理系统，书，作者，出版社


class Publisher(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=64, null=False, unique=True)
    addr = models.CharField(max_length=64, default="苏州吴中区")


class Book(models.Model):
    id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=64, null=False, unique=True)
    publisher_id= models.ForeignKey(to=Publisher)


class Author(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=64, null=False, unique=True)
    book = models.ManyToManyField(to=Book)