from django.urls import path, include
from django.conf.urls import handler404
from .views import (
    IndexSearch,
    RecipesList,
    CategoryDetail,
    RecipeDetail,
    AboutDetail,
    BlogList,
    ArticleDetail,
)


urlpatterns = [
    path("", IndexSearch.as_view(), name="index"),
    path("recipes", RecipesList.as_view(), name="recipes"),
    path("recipes/<slug:category_slug>", CategoryDetail.as_view(), name="category"),
    path("recipes/<slug:recipe_slug>", RecipeDetail.as_view, name="recipe"),
    path("about", AboutDetail.as_view(), name="about"),
    path("blog", BlogList.as_view(), name="blog"),
    path("blog/<slug:article_slug>", ArticleDetail.as_view(), name="article"),
]

handler404 = "recipe.views.my_custom_page_not_found"
