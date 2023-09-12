from django.db import models
from django.urls import reverse

from category_sub.models import Category, SubCategory

from .managers import ProductManager


class Product(models.Model):
    # common factors
    title = models.CharField(max_length=255)
    slug = models.SlugField(max_length=120, null=True, blank=True)
    category = models.ForeignKey(SubCategory, on_delete=models.CASCADE, null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    color = models.CharField(max_length=120, blank=True, null=True)
    initial_price = models.DecimalField(max_digits=20, decimal_places=2, default=0.00, null=True, blank=True)
    discount = models.DecimalField(max_digits=4, decimal_places=2, default=0.00, null=True, blank=True)
    final_price = models.DecimalField(max_digits=20, decimal_places=2, default=0.00, null=True, blank=True)
    main_image = models.ImageField(upload_to='', null=True, blank=True)
    is_upcoming = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    updated = models.DateTimeField(auto_now=True)
    timestamp = models.DateTimeField(auto_now_add=True)

    objects = ProductManager()

    def get_absolute_url(self):
        return reverse('products:detail', kwargs={'slug': self.slug})

    def __str__(self):
        return self.title
