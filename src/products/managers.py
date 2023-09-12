from django.db.models import Q
from django.db import models
from django.utils.text import slugify


class ProductQuerySet(models.query.QuerySet):
    def get_by_slug(self, slug):
        qs = self.filter(slug=slug)
        if qs.count() == 1:
            obj = qs.first()
            return obj
        return None

    def search(self, query):
        sl_query = slugify(query)
        lookups = (Q(title__icontains=query) | Q(description__icontains=query) |
                   Q(mobile__brand__icontains=query) | Q(mobile__ram__icontains=query) |
                   Q(category__category_keywords__icontains=query))
        return self.filter(lookups).distinct()


class ProductManager(models.Manager):
    def get_queryset(self):
        return ProductQuerySet(self.model, using=self._db)

    def get_by_slug(self, slug):
        return self.get_queryset().get_by_slug(slug)

    def search(self, query):
        return self.get_queryset().search(query)
