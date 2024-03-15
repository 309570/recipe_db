from django import forms
from django.db.models import Count
from .models import Category, Ingredient, Recipe, RecipeIngredient
from dal import autocomplete


# class SearchForm(forms.Form):
#     ingredient = forms.CharField(
#         widget=forms.TextInput(
#             attrs={"class": "select2", "data-url": reverse("ingredient-autocomplete")}
#         ),
#         required=False,
#     )


class RecipeIngredientForm(forms.Form):
    ingredient = forms.CharField(
        widget=forms.TextInput(attrs={"id": "ingredient_input", "autocomplete": "off"}),
        label="Ingredient",
    )
    ingredients_list = forms.CharField(
        widget=forms.HiddenInput(attrs={"id": "ingredients_list"}), required=False
    )


from django import forms


class FormSearching(forms.Form):
    title = forms.CharField(
        max_length=255,
        widget=autocomplete.ListSelect2(url="title-autocomplete"),
        label="Название рецепта",
        required=False,
    )
    ingredient = forms.CharField(
        widget=autocomplete.ListSelect2(url="ingredient-autocomplete"),
        label="Ингредиент",
        required=False,
    )
    ingredients_list = forms.CharField(
        widget=forms.HiddenInput(attrs={"id": "ingredients_list"}), required=False
    )


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
        widget=autocomplete.ModelSelect2Multiple(url="ingredient-autocomplete"),
        # widget=forms.CheckboxSelectMultiple,
        required=False,
    )

    category = forms.ModelMultipleChoiceField(
        queryset=Category.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=False,
    )

    title = forms.CharField(
        widget=autocomplete.ListSelect2(url="title-autocomplete"),
        label="Title",
        required=False,
    )

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
    return (
        Ingredient.objects.annotate(frequency=Count("recipes"))
        .order_by("-frequency")
        .values_list("name", flat=True)[:12]
    )
