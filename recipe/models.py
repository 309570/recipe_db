from django.db import models
from django.utils.text import slugify


class Category(models.Model):
    title = models.CharField(max_length=225)
    slug = models.SlugField(unique=True, blank=True)

    def save(self, *args, **kwargs):
        print("Сохранение категории:", self.title)  # Вывод для отладки
        self.title = self.title.lower()
        super(Category, self).save(*args, **kwargs)
        # if not self.slug:
        #     self.slug = slugify(self.title)
            # original_slug = self.slug
            # num = 1
            # while Category.objects.filter(slug=self.slug).exists():
            #     self.slug = f'{original_slug}-{num}'
            #     num += 1

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
    title_image = models.ImageField(upload_to="site_images/", null=True, blank=True)
    ingredient = models.ManyToManyField(
        Ingredient,
        through="RecipeIngredient",
        related_name="recipes",
        through_fields=("recipe", "ingredient"),
    )
    body_image = models.ImageField(upload_to="site_images/", null=True, blank=True)
    preparation = models.TextField()
    category = models.ManyToManyField(Category, blank=True)
    reviews = models.IntegerField(default=12)
    slug = models.SlugField(unique=True, blank=True)

    def save(self, *args, **kwargs):
        self.title = self.title.lower()
        if not self.slug:
            self.slug = slugify(self.title)
        self.preparation = self.preparation.lower()
        super(Recipe, self).save(*args, **kwargs)

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
    description_text = models.TextField()
    image = models.ImageField(upload_to="site_images/", blank=True, null=True)

    def __str__(self):
        return self.text


class Article(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    image = models.ImageField(upload_to="site_images/", blank=True, null=True)
    link = models.URLField(blank=True)
    slug = models.SlugField(unique=True, blank=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super(Article, self).save(*args, **kwargs)

    def __str__(self):
        return self.title
