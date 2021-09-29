from django.conf import settings
from django.db import models

STATUS_CHOICES = (("IN_STOCK", "In Stock"), ("OUT_OF_STOCK", "Out Of Stock"))

ORDER_BY_CHOICES = (
    ("price_asc", "Price Asc"),
    ("price_desc", "Price Desc"),
    ("max_count", "Max Count"),
    ("max_price", "Max Price"),
)


class Product(models.Model):
    name = models.CharField(max_length=200)
    image = models.ImageField(null=True, blank=True)
    price = models.IntegerField()
    description = models.TextField(default="")
    status = models.CharField(
        max_length=100, choices=STATUS_CHOICES, default="IN_STOCK"
    )
    favorites = models.ManyToManyField(
        settings.AUTH_USER_MODEL, related_name="favorite_products"
    )

    def __str__(self):
        return f"{self.name} - {self.price}"


class Purchase(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    product = models.ForeignKey(
        Product, related_name="purchases", on_delete=models.CASCADE
    )
    count = models.IntegerField()

    def __str__(self):
        return f"{self.user} - {self.product} - {self.count}"
