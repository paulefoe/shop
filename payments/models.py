from django.db import models


class Order(models.Model):
    paid = models.BooleanField(default=False)
    count = models.SmallIntegerField(default=1)

    def get_total_price(self):
        res = 0
        for a in self.product_set.all():
            product_price = a.price * a.count
            res += product_price
        return res

    def __str__(self):
        return str(self.id)

