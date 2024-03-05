from django.db.models.signals import pre_save
from django.dispatch import receiver
from django.utils.text import slugify
from .models import Category


@receiver(pre_save, sender=Category)
def pre_save_category_receiver(sender, instance, *args, **kwargs):
    print(f"Вызван pre_save для {instance.title}")
    if not instance.slug:
        instance.slug = slugify(instance.title, allow_unicode=True)
        print(f"Сгенерирован slug: {instance.slug}")
