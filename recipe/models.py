from django.db import models
from django.utils.text import slugify
from pytils.translit import slugify
from django.conf import settings
from PIL import Image
import os
from uuid import uuid4


class Category(models.Model):
    title = models.CharField(max_length=225)
    slug = models.SlugField(unique=True, blank=True)

    def save(self, *args, **kwargs):
        self.title = self.title.lower()
        self.slug = slugify(self.title)
        super(Category, self).save(*args, **kwargs)

    def __str__(self):
        return self.title


class Ingredient(models.Model):
    name = models.CharField(max_length=100, blank=True)

    def save(self, *args, **kwargs):
        self.name = self.name.lower()
        super(Ingredient, self).save(*args, **kwargs)

    def __str__(self):
        return self.name


class Recipe(models.Model):
    title = models.CharField(max_length=150)
    title_image = models.ImageField(upload_to="recipe_images/", null=True, blank=True)
    ingredient = models.ManyToManyField(
        Ingredient,
        through="RecipeIngredient",
        related_name="recipes",
        through_fields=("recipe", "ingredient"),
    )
    body_image = models.ImageField(
        upload_to="recipe/body_image/", blank=True, editable=False
    )
    preparation = models.TextField()
    category = models.ManyToManyField(Category, blank=True)
    reviews = models.IntegerField(default=12)
    slug = models.SlugField(unique=True, blank=True)

    def save(self, *args, **kwargs):
        self.title = self.title.lower()
        self.slug = slugify(self.title)
        super(Recipe, self).save(*args, **kwargs)

        if self.title_image:
            self.make_body_image()

    def make_body_image(self):
        img = Image.open(self.title_image.path)
        output_size = (120, 120)
        img.thumbnail(output_size)

        body_imagename = f"body_image_{uuid4()}.jpg"
        body_image_path = os.path.join("recipe/body_image/", body_imagename)
        img.save(os.path.join(settings.MEDIA_ROOT, body_image_path))

        self.body_image = body_image_path
        super(Recipe, self).save()

    def __str__(self):
        return self.title


class RecipeIngredient(models.Model):
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE)
    ingredient = models.ForeignKey(
        Ingredient, on_delete=models.CASCADE, related_name="recipe_ingredients"
    )
    unit = models.CharField(max_length=100, blank=True)
    substitutes = models.CharField(max_length=100, blank=True)

    def save(self, *args, **kwargs):
        self.unit = self.unit.lower()
        self.substitutes = self.substitutes.lower()
        super(RecipeIngredient, self).save(*args, **kwargs)


class About(models.Model):
    text = models.TextField()


class AboutSection(models.Model):
    about = models.ForeignKey(About, related_name="sections", on_delete=models.CASCADE)
    inscription = models.TextField(blank=True, null=True)
    image = models.ImageField(upload_to="about_images/", blank=True, null=True)

    def __str__(self):
        return self.inscription


class Article(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    image = models.ImageField(upload_to="recipe_images/", blank=True, null=True)
    preview_article = models.ImageField(
        upload_to="articles_images/", blank=True, editable=False
    )
    link = models.URLField(blank=True)
    slug = models.SlugField(unique=True, blank=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super(Article, self).save(*args, **kwargs)

        if self.image:
            self.make_preview_article()

    def make_preview_article(self):
        ar_img = Image.open(self.image.path)
        output_size = (300, 200)
        ar_img.thumbnail(output_size)

        preview_articlename = f"preview_article_{uuid4()}.jpg"
        preview_article_path = os.path.join("articles_images/", preview_articlename)
        ar_img.save(os.path.join(settings.MEDIA_ROOT, preview_article_path))

        self.preview_article = preview_article_path
        super(Article, self).save()

    def __str__(self):
        return self.title
