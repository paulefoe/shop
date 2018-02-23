from django.db import models
from showcase.models import Product


class Order(models.Model):
    # TODO должна быть вся инфа, имейл, что за продукт, сколько,
    # какого цвета и размера потом в гет методе клирить сессии и всё записывать в ордер, а из колбека
    #  доставать ордер айди и присваивать оплате значение тру
    paid = models.BooleanField(default=False)
    email = models.EmailField()
    address = models.CharField(max_length=250)

    def __str__(self):
        return str(self.id)


class OrderItem(models.Model):
    order = models.ForeignKey(Order)
    product = models.ForeignKey(Product)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    quantity = models.PositiveIntegerField(default=1)
    color = models.CharField(max_length=30)
    size = models.CharField(max_length=20)

    def __str__(self):
        return str(self.product)

    def total_sum(self):
        return self.price * self.quantity
