from django import forms
from django.db.models import Count
from .models import Category, Ingredient, Recipe, RecipeIngredient
from dal import autocomplete

class RecipeIngredientForm(forms.ModelForm):
    class Meta:
        model = RecipeIngredient
        fields = "__all__"
        widgets = {
            "ingredient": autocomplete.ModelSelect2(url="ingredient-autocomplete")
        }


class SearchForm(forms.Form):
    ingredient = forms.ModelMultipleChoiceField(
        queryset=Ingredient.objects.all(),
        widget=autocomplete.ModelSelect2Multiple(
            url="ingredient-autocomplete"),
        # widget=forms.CheckboxSelectMultiple,
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


# class SearchingRecipe(forms.Form):
#     user_input = forms.CharField(min_length=3, max_length=10)
