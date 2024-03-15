from .models import Category, Recipe, Ingredient
from recipe.forms import SearchForm
from django.db.models import Q, Count
from .forms import get_frequent_ingredients_names


def get_check_ingredients(form):

    """Получение ингредиентов для фильтрации и проверка их соответствия условим поиска."""
    input_ingredient = form.cleaned_data.get("ingredient", [])
    # получили ингредиенты из формы в виде списка обьектов.
    frequent_ingredients_selected = form.cleaned_data.get("frequent_ingredients", [])
    all_ingredients = list(input_ingredient) + list(frequent_ingredients_selected)
    all_ingredients = [ingredient.name.lower() for ingredient in all_ingredients]
    # список обьектов преобразовали в список строк имен и привели к нижнему регистру

    if (len(all_ingredients)) > 4:
        # проверили что выбрано не более 4х ингредиентов
        return None, "Будь ласка, виберіть не більше 4х інгредієнтів. Або Ви можете ознайомитись із повним списком рецептів"

    else:
        return all_ingredients, None


def get_select_category(form):
    """Функция для получения категорий."""
    select_category = form.cleaned_data.get("category", [])
    select_category = [category.title for category in select_category]
    return select_category

def handle_search(request):
    recipes = Recipe.objects.all()
    form = SearchForm(request.GET)
    errors = []

    if form.is_valid() and any(value for key, value in request.GET.items()):
        title_recipe = form.cleaned_data.get("title")
        if title_recipe:
            recipes = Recipe.objects.filter(title__icontains=title_recipe.lower())
        else:

            select_category = get_select_category(form)
            ingredient_filter, ingredient_filter_error = get_check_ingredients(form)

            if ingredient_filter_error:
                errors.append(ingredient_filter_error)

            if select_category:
                recipes = recipes.filter(category__title__in=select_category)

            if not ingredient_filter:
                pass
            elif ingredient_filter and not ingredient_filter_error:
                for ingredient_name in ingredient_filter:
                    recipes = recipes.filter(ingredient__name__icontains=ingredient_name)
                if not recipes.exists():
                    errors = errors.append(
                        "За Вашим запитом рецепти не знайдені. Уточніть умови пошуку, можливо, ви ввели інгредієнти, що повторюються."
                    )
            error_message = ' '.join(errors)
            if errors or not recipes.exists():
                return {
                    "form": form,
                    "categories": Category.objects.all(),
                    "frequent_ingredients": get_frequent_ingredients_names(),
                    "errors": error_message,
                }
        if recipes.exists:

            # очищенная  форма, рецепты, категории, частотные ингредиенты
            return {
                "form": form,
                "recipes": recipes.distinct(),
                "categories": Category.objects.all(),
                "frequent_ingredients": get_frequent_ingredients_names(),
            }

    else:
        return {
            "form": form,
            "recipes": Recipe.objects.none(),
            "categories": Category.objects.all(),
            "frequent_ingredients": get_frequent_ingredients_names(),
        }
