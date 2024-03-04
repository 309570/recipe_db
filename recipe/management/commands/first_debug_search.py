from django.core.management.base import BaseCommand
from django.test.client import RequestFactory
from recipe.models import Category, Ingredient, Recipe
from recipe.search_logic import handle_search 


class Command(BaseCommand):
    help = "Отладка функции поиска"

    def handle(self, *args, **options):
        factory = RequestFactory()

        ingredient_id = list(Ingredient.objects.filter(name__in=["яйце", "авокадо"]).values_list("id", flat=True)
        )
        category_id = list(Category.objects.filter(title__in=["Гаряче"]).values_list("id", flat=True))

        # get_params = {"title": "пюре"}
        # get_params = {"category": category_id}
        # get_params = {"ingredient": ingredient_id}
        get_params = {"ingredient": ingredient_id, "category": category_id}
        # get_params = {"title": "борщ", "ingredient": ingredient_id, "category": category_id}
        # get_params = {"title": "пюре", "category": category_id}
        # get_params = {"title": "омлет", "ingredient": ingredient_id}
        print(get_params)

        request = factory.get("/fake-url/", get_params)
        print(request)

        response = handle_search(request)

        self.stdout.write(self.style.SUCCESS(f"Response: {response}"))
