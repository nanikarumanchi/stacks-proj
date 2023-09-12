import os
import string

from django.utils.text import slugify

from ab_stacks_main.utils import random_string_generator


def get_image_path(filepath):
    base_name = os.path.basename(filepath)
    filename, ext = os.path.splitext(base_name)
    return filename, ext


def upload_image_path(instance, file_name):
    title = slugify(instance.title)
    new_filename = random_string_generator(size=3, chars=string.digits)
    name, ext = get_image_path(file_name)
    final_filename = f'{title}{new_filename}{ext}'
    final_filepath = f'main_images/{title}/{final_filename}'
    return final_filepath
