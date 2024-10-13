# Make sure to import from django.db, not from your local app models
from django.db import models
from django.contrib.auth import get_user_model



class Product(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    available_stock = models.PositiveIntegerField(default=0)
    selected_by = models.ForeignKey(get_user_model(), null=True, blank=True, on_delete=models.SET_NULL, related_name="selected_products")

    def __str__(self):
        return self.name


class ProductReport(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    reported_by = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    reason = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.product.name
