import os

from django.db import models
from django.conf import settings
from django.utils.crypto import get_random_string


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
    # image = models.ImageField(storage=fs, upload_to='products')
    name = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=9, decimal_places=2)
    description = models.TextField()
    category = models.ForeignKey(Category, related_name='categories')
    count = models.PositiveIntegerField(default=0)
    tags = models.CharField(max_length=30)
    size = models.ManyToManyField(Size)
    color = models.ManyToManyField(Color)

    def __str__(self):
        return self.name


def image_directory_path(instance, filename):
    """Проитерировать все папки в media, если в одной из них меньше 60к файлов, то сохранить туда
    В противном случае создать новую папку и сохранить в неё
    """
    filename = 'picture.' + filename.split('.')[-1]
    for folder in os.listdir(settings.MEDIA_ROOT):
        if len(os.listdir(os.path.join(settings.MEDIA_ROOT, folder))) < 60000:
            return os.path.join(folder, filename)
    new_folder = 'products' + get_random_string(3)
    os.makedirs('media/' + new_folder)
    return os.path.join(new_folder, filename)


class Image(models.Model):
    image = models.ImageField(upload_to=image_directory_path)
    product = models.ForeignKey(Product)
    ordering = models.SmallIntegerField()

    def __str__(self):
        return str(self.image)


