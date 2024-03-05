from django.contrib import admin
from .models import Category, Ingredient, Recipe, RecipeIngredient, About, Article


class IngredientInline(admin.TabularInline):
    model = RecipeIngredient
    extra = 4


@admin.register(Recipe)
class RecipeAdmin(admin.ModelAdmin):
    list_display = [
        "title",
        "get_ingredients",
        "preparation",
        "get_categories",
        "reviews",
    ]
    exclude = ("slug",)
    inlines = [IngredientInline]

    def get_ingredients(self, obj):
        return ", ".join(
            [
                f"{ri.ingredient.name} ({ri.unit}) - {ri.substitutes})"
                for ri in obj.recipeingredient_set.all()
            ]
        )

    get_ingredients.short_description = "Ingredients"

    def get_categories(self, obj):
        return ", ".join([category.title for category in obj.category.all()])

    get_categories.short_description = "Categories"


class CategoryAdmin(admin.ModelAdmin):
    exclude = ("slug",)


admin.site.register(Category, CategoryAdmin)
admin.site.register(Ingredient)
admin.site.register(RecipeIngredient)
admin.site.register(About)
admin.site.register(Article)
