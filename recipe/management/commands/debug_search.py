from django.core.management.base import BaseCommand
from django.test.client import RequestFactory
from recipe.models import Category, Ingredient
from recipe.views import handle_search


class Command(BaseCommand):
    help = "Debug search functionality"

    def handle(self, *args, **options):
        factory = RequestFactory()

        input_ingredient_ids = list(
            Ingredient.objects.filter(name__in=["йогурт"]).values_list(
                "id", flat=True
            )
        )

        # frequent_ingredient_ids = list(
        #     Ingredient.objects.filter(name__in=["йогурт"]).values_list(
        #         "id", flat=True
        #     )
        # )

        # category_ids = list(
        #     Category.objects.filter(title__in=["гаряче"]).values_list("id", flat=True)
        # )

        get_params = {
            "ingredient": input_ingredient_ids,
            # "frequent_ingredients": frequent_ingredient_ids,
            # "category": category_ids,
            "title": "борщ"
        }

        # Создание и отправка запроса
        request = factory.get("/fake-url/", get_params)
        response = handle_search(request)

        self.stdout.write(self.style.SUCCESS(f"Response: {response}"))
