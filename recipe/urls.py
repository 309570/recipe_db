from django.urls import path, include
from django.conf.urls import handler404
# from .forms import
from .views import (
    IndexSearch,
    RecipesList,
    CategoryDetail,
    RecipeDetail,
    AboutDetail,
    BlogList,
    ArticleDetail,
    IngredientAutocomplete,
    TitleAutocomplete,
)


urlpatterns = [
    path("", IndexSearch.as_view(), name="index"),
    path("recipes/", RecipesList.as_view(), name="recipes"),
    path(
        "recipes/category/<slug:category_slug>/",
        CategoryDetail.as_view(),
        name="category",
    ),
    path('recipes/recipe/<slug:recipe_slug>/',
         RecipeDetail.as_view(), name="recipe"),
    path("about/", AboutDetail.as_view(), name="about"),
    path("blog/", BlogList.as_view(), name="blog"),
    path("blog/<slug:article_slug>/",
         ArticleDetail.as_view(), name="article"),
    path('ingredient-autocomplete/', IngredientAutocomplete.as_view(), name='ingredient-autocomplete'),
    path('title-autocomplete/', TitleAutocomplete.as_view(), name='title-autocomplete'),
]

handler404 = "recipe.views.my_custom_page_not_found"
