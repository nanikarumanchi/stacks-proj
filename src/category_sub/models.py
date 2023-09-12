from django.db import models

CATEGORY_CHOICES = (
    ('none', 'None'),
    ('electronics', 'Electronics'),
    ('fashion', 'Fashion'),
    ('furniture', 'Furniture'),
    ('books', 'Books'),
)


class Category(models.Model):
    name = models.CharField(max_length=20, default='None', choices=CATEGORY_CHOICES)

    def __str__(self):
        return self.name


class SubCategory(models.Model):
    parent_category = models.ForeignKey(Category, on_delete=models.CASCADE)
    category_keywords = models.CharField(max_length=255, null=True, blank=True)
    name = models.CharField(max_length=120, default='NONE')

    def __str__(self):
        return self.name
