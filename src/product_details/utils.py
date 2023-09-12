import datetime
import string
import os

from django.utils.text import slugify
from ab_stacks_main.utils import random_string_generator
from category_sub.models import SubCategory
from products.models import Product


# util functions
def unique_slug_generator(instance, new_slug=None):
    date = datetime.date.today()
    if new_slug is not None:
        slug = new_slug
    else:
        slug = f'' \
               f'{slugify(instance.name)}' \
               f'-{date.day}-{date.month}-{date.year}' \
               f'{random_string_generator(size=10)}'[:100]
    Klass = instance.__class__
    qs_exists = Klass.objects.filter(slug=slug).exists()
    if qs_exists:
        new_slug = "{slug}-{randstr}".format(
            slug=slug,
            randstr=random_string_generator(size=10)
        )
        return unique_slug_generator(instance, new_slug=new_slug)
    return slug


def get_image_path(filepath):
    base_name = os.path.basename(filepath)
    filename, ext = os.path.splitext(base_name)
    return filename, ext


def upload_image_path(instance, file_name):
    title = slugify(instance.name)
    new_filename = random_string_generator(size=4, chars=string.digits)
    name, ext = get_image_path(file_name)
    final_filename = f'{title}{new_filename}{ext}'
    print(instance._meta.object_name)
    final_filepath = f'products/{instance._meta.object_name}/{title}/{final_filename}'
    return final_filepath


# signal functions
def post_save_details_save_data_to_product_model(sender, instance, *args, **kwargs):
    obj, new_obj = Product.objects.get_or_create(title=instance.name)
    # , color=instance.color, initial_price=instance.initial_price
    obj.title = instance.name
    obj.slug = instance.slug
    obj.category = SubCategory.objects.get(name=sender.__name__)
    obj.description = instance.description
    obj.color = instance.color
    obj.initial_price = instance.initial_price
    obj.discount = instance.discount
    obj.final_price = instance.final_price
    obj.main_image = instance.main_image
    obj.is_upcoming = instance.is_upcoming
    obj.is_active = instance.is_active

    obj.save()
    if instance.product_name is None:
        instance.product_name = obj
        instance.save()


def pre_save_slug_generator(sender, instance, *args, **kwargs):
    if instance.slug is None:
        instance.slug = unique_slug_generator(instance)
