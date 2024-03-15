from django.contrib import admin
from .models import Category, Ingredient, Recipe, RecipeIngredient, About, AboutSection, Article
from .forms import RecipeIngredientForm


@admin.register(Ingredient)
class IngredientAdmin(admin.ModelAdmin):
    search_fields = ["name"]


class IngredientInline(admin.TabularInline):
    form = RecipeIngredientForm
    model = RecipeIngredient
    extra = 6


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

class AboutSectionInline(admin.TabularInline):
    model = AboutSection
    extra = 4

@admin.register(About)
class AboutAdmin(admin.ModelAdmin):
    inlines = [AboutSectionInline]

@admin.register(AboutSection)
class AboutSectionInline(admin.ModelAdmin):
    list_display = ['inscription', 'image']


admin.site.register(Category, CategoryAdmin)
# admin.site.register(Ingredient)
admin.site.register(RecipeIngredient)
admin.site.register(Article)
