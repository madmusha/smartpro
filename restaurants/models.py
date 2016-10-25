from django.db import models
from django.db.models.signals import pre_save
from django.template.defaultfilters import slugify
from django.urls import reverse
from transliterate import translit


# Create your models here.


class Restaurant(models.Model):
    name = models.CharField(max_length=240)
    slug = models.SlugField(unique=True, blank=True)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("rest", kwargs={"slug": self.slug})


def pre_save_reciever(instance, sender, **kwargs):
    trans_name = translit(instance.name, reversed=True)
    instance.slug = slugify(trans_name)


pre_save.connect(pre_save_reciever, sender=Restaurant)
