from django.core.management.base import BaseCommand
from django.test.client import RequestFactory
from recipe.models import Recipe, Ingredient, Category


class Command(BaseCommand):
    help = "Получение рецептов по ингредиентам и категории через Django ORM"

    def add_arguments(self, parser):
        parser.add_argument(
            "--ingredients", nargs="+", type=int, help="ID ингредиентов"
        )
        parser.add_argument("--category", type=int, help="ID категории")

    def handle(self, *args, **options):
        ingredients_ids = options["ingredients"]
        category_id = options["category"]

        recipes = Recipe.objects.filter(
            ingredient__id__in=ingredients_ids, category__id=category_id
        ).distinct()

        if recipes:
            self.stdout.write(
                self.style.SUCCESS(f"Найдено рецептов: {recipes.count()}")
            )
            for recipe in recipes:
                self.stdout.write(self.style.SUCCESS(f"Найден рецепт: {recipe.title}"))
        else:
            self.stdout.write(self.style.WARNING("Рецепты не найдены"))
