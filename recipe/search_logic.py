from .models import Category, Recipe, Ingredient
from recipe.forms import SearchForm
from .forms import get_frequent_ingredients_names


class SearchHandler:
    def __init__(self, form):
        self.form = form
        self.recipes = Recipe.objects.all()

    def get_check_ingredients(self):
        """Получение ингредиентов для фильтрации и проверка их соответствия условим поиска."""
        input_ingredient = self.form.cleaned_data.get("ingredient", [])
        # получили ингредиенты из формы в виде списка обьектов.
        frequent_ingredients_selected = self.form.cleaned_data.get(
            "frequent_ingredients", []
        )
        all_ingredients = list(input_ingredient) + list(frequent_ingredients_selected)
        all_ingredients = [ingredient.name.lower() for ingredient in all_ingredients]
        # список обьектов преобразовали в список строк имен и привели к нижнему регистру
        return all_ingredients

    def get_select_category(self):
        """Функция для получения категорий."""
        select_category = self.form.cleaned_data.get("category", [])
        select_category = [category.title for category in select_category]
        return select_category

    def get_title(self):
        title_recipe = self.form.cleaned_data.get("title")
        return title_recipe

    def process(self):
        select_category = self.get_select_category()
        ingredient_filter = self.get_check_ingredients()
        title_recipe = self.get_title()
        recipes = self.recipes

        if (len(ingredient_filter)) > 4:
            return {
                "form": self.form,
                "categories": Category.objects.all(),
                "frequent_ingredients": get_frequent_ingredients_names(),
                "errors": "Будь ласка, виберіть не більше 4х інгредієнтів.",
            }

        if title_recipe:
            recipes = Recipe.objects.filter(title__icontains=title_recipe.lower())

        else:
            if select_category:
                recipes = recipes.filter(category__title__in=select_category)

            if not ingredient_filter:
                pass
            elif ingredient_filter:
                for ingredient_name in ingredient_filter:
                    recipes = recipes.filter(
                        ingredient__name__icontains=ingredient_name
                    )
                if not recipes.exists():
                    return {
                        "form": self.form,
                        "categories": Category.objects.all(),
                        "frequent_ingredients": get_frequent_ingredients_names(),
                        "errors": "За Вашим запитом рецепти не знайдені. Уточніть умови пошуку.",
                    }

        if not title_recipe and not select_category and not ingredient_filter:
            return {
                "form": self.form,
                "categories": Category.objects.all(),
                "frequent_ingredients": get_frequent_ingredients_names(),
                "recipes": [],
            }

        if recipes:
            return {
                "form": self.form,
                "recipes": recipes.distinct(),
                "categories": Category.objects.all(),
                "frequent_ingredients": get_frequent_ingredients_names(),
            }
