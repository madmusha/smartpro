from django.db import models
from django.utils import timezone
# Create your models here.
from restaurants.models import Restaurant


class Consumable(models.Model):
    name = models.CharField(max_length=240, unique=True)
    active = models.BooleanField(default=True)

    def __str__(self):
        return self.name


class Quantity(models.Model):
    product = models.ForeignKey('Product')
    consumable = models.ForeignKey(Consumable)
    amount = models.PositiveIntegerField()

    def __str__(self):
        return '%s:%s' % (self.consumable, self.amount)


class Product(models.Model):
    name = models.CharField(max_length=240)
    active = models.BooleanField(default=True)
    restaurants = models.ManyToManyField(Restaurant)

    def __str__(self):
        return self.name


class ConsumableIncome(models.Model):
    consumable = models.ForeignKey(Consumable)
    amount = models.PositiveIntegerField()
    restaurant = models.ForeignKey(Restaurant)
    date = models.DateField(default=timezone.now)

    def __str__(self):
        return '%s:%s' % (self.consumable.name, self.restaurant.name)


class CheckoutProduct(models.Model):
    restaurant = models.ForeignKey(Restaurant)
    product = models.ForeignKey(Product)
    amount = models.PositiveIntegerField(null=True)
    date = models.DateField(default=timezone.now)

    def __str__(self):
        return '%s:%s' % (self.product.name, self.amount)


class ReportConsmable(models.Model):
    consumable = models.ForeignKey(Consumable)
    amount = models.PositiveIntegerField(null=True)
    restaurant = models.ForeignKey(Restaurant)
    date = models.DateField(default=timezone.now)

    def __str__(self):
        return '%s:%s' % (self.consumable.name, self.restaurant.name)
