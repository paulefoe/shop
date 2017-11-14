from django.db import models
from django.conf import settings

from showcase.storage import OverWriteStorage



class Category(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(max_length=50)
    order = models.PositiveIntegerField()
    parent = models.ForeignKey('self', blank=True, null=True, related_name='children')

    class Meta:
        ordering = ['-order']

    def __str__(self):
        return self.name

fs = OverWriteStorage(location=settings.MEDIA_ROOT, base_url=settings.MEDIA_URL)


class Product(models.Model):
    image = models.ImageField(storage=fs, upload_to='products')
    name = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=9, decimal_places=2)
    description = models.TextField()
    category = models.ForeignKey(Category, related_name='categories')

    def __str__(self):
        return self.name


