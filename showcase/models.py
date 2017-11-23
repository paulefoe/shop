import os
import pathlib
from uuid import uuid4
import re

from django.db import models
from django.utils.deconstruct import deconstructible
from payments.models import Order


class Color(models.Model):
    color = models.CharField(max_length=10)

    def __str__(self):
        return self.color


class Size(models.Model):
    size = models.CharField(max_length=10)

    def __str__(self):
        return self.size


class Category(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(max_length=50)
    order = models.PositiveIntegerField()
    parent = models.ForeignKey('self', blank=True, null=True, related_name='children')

    class Meta:
        ordering = ['-order']

    def __str__(self):
        return self.name


class Product(models.Model):
    name = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=9, decimal_places=2)
    description = models.TextField()
    category = models.ForeignKey(Category, related_name='categories')
    count = models.PositiveIntegerField(default=0)
    tags = models.CharField(max_length=30)
    size = models.ManyToManyField(Size)
    color = models.ManyToManyField(Color)
    order = models.ForeignKey(Order)

    def __str__(self):
        return self.name


@deconstructible
class FilePathDir(object):

    def __init__(self, subdir=None):
        self.subdir = subdir

    def __call__(self, instance, filename):
        print(filename)
        p = pathlib.Path(filename)
        new_filename = uuid4().hex + ''.join(p.suffix)
        match = re.findall('(.{1,2})', new_filename[:6])
        full_filename = []
        full_filename += match + [new_filename]
        new_path = os.path.join(*full_filename)

        if self.subdir:
            new_path = os.path.join(self.subdir, new_path)
        return new_path


class Image(models.Model):
    image = models.ImageField(upload_to=FilePathDir(subdir='results'))
    product = models.ForeignKey(Product)
    ordering = models.SmallIntegerField()

    def __str__(self):
        return str(self.image)


