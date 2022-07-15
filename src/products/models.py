from django.db import models
from django.contrib.auth.models import User
from pandas_datareader import data as web
from yahooquery import Ticker

# Create your models here.

class Info(models.Model):
    ativo = models.CharField(max_length=220)
    date = models.DateTimeField(auto_now_add=True)
    email = models.EmailField(max_length=220)
    inferior = models.FloatField()
    superior = models.FloatField()

    def __str__(self):
        return str(self.ativo)


# class Purchase(models.Model):
#     product = models.ForeignKey(Product, on_delete=models.CASCADE)
#     price = models.PositiveBigIntegerField()
#     quantity = models.PositiveBigIntegerField()
#     total_price = models.PositiveBigIntegerField(blank=True)
#     salesman = models.ForeignKey(User, on_delete=models.CASCADE)
#     date = models.DateTimeField(auto_now_add=True)


#     def save(self, *args, **kwargs):
#         self.total_price = self.price * self.quantity
#         super().save(*args, **kwargs)
        


#     def __self__(self):
#         return "Solled {} - {} for {}".format(self.product.ativo, self.quantity, self.total_price)