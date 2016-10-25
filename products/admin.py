from django.contrib import admin

# Register your models here.
from products.models import CheckoutProduct, Product, Quantity, Consumable, ConsumableIncome, ReportConsmable

admin.site.register(Product)
admin.site.register(Consumable)
admin.site.register(ConsumableIncome)
admin.site.register(Quantity)
admin.site.register(ReportConsmable)
admin.site.register(CheckoutProduct)
