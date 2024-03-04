from django import forms
from django.db.models import Count
from .models import Category, Ingredient, Recipe


class SearchForm(forms.Form):
    ingredient = forms.ModelMultipleChoiceField(
        queryset=Ingredient.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=False,
    )
    category = forms.ModelMultipleChoiceField(
        queryset=Category.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=False,
    )
    title = forms.CharField(required=False)

    frequent_ingredients = forms.ModelMultipleChoiceField(
        queryset=Ingredient.objects.none(),  # Начальный набор пуст, будет установлен динамически
        widget=forms.CheckboxSelectMultiple,
        required=False,
    )

    def __init__(self, *args, **kwargs):
        super(SearchForm, self).__init__(*args, **kwargs)
        self.fields["frequent_ingredients"].queryset = Ingredient.objects.filter(
            name__in=get_frequent_ingredients_names()
        )

def get_frequent_ingredients_names():
    return Ingredient.objects.annotate(frequency=Count("recipes")).order_by(
        "-frequency").values_list('name', flat=True)[:12]


# def get_frequent_ingredients_names():
#     # Возвращает список имен часто используемых ингредиентов
#     return (
#         Recipe.objects.values_list("ingredient__name", flat=True)
#         .annotate(frequency=Count("ingredient__name"))
#         .order_by("-frequency")[:12]
#     )
# def __init__(self, *args, **kwargs):
#     super(SearchForm, self).__init__(*args, **kwargs)
#     self.fields["frequent_ingredients"].queryset = Ingredient.objects.annotate(
#         frequency=Count("recipes")
#     ).order_by("-frequency")[:12]
