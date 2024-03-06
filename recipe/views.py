from typing import Any
from django.db.models.query import QuerySet
from django.http import HttpResponse, HttpResponseNotFound, Http404
from django.views.generic import ListView, DetailView, TemplateView
from django.shortcuts import render, redirect, get_list_or_404
from recipe.models import Category, Recipe, About, Article
from .forms import SearchForm
from .search_logic import handle_search


def my_custom_page_not_found(request, exeption):
    return render(
        request,
        "Такої сторінки не знайдено. Можливо, ця помилка має тимчасовий характер. Спробуйте повторити пошук",
        {},
        status=404,
    )


class IndexSearch(TemplateView):
    template_name = "recipe/index.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        search_result = handle_search(self.request)
        context.update(
            {
                "form": search_result.get("form"),
                "categories": search_result.get("categories"),
                "frequent_ingredients": search_result.get("frequent_ingredients"),
                "recipes": search_result.get("recipes"),
                "errors": search_result.get("recipes"),
                "title": "Пошук рецептів",
                "title_content": "Пошук рецептів за інгредієнтами та категоріями",
            }
        )
        return context


class RecipesList(ListView):
    model = Recipe
    template_name = "recipe/recipes.html"
    context_object_name = "recipes"
    queryset = Recipe.objects.order_by("-reviews")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["categories"] = Category.objects.all()
        context["title"] = "Рецепти ПП"
        context["title_content"] = "Рецепти відсортовані за рейтингом"
        return context


class CategoryDetail(DetailView):
    model = Category
    template_name = "recipe/category.html"
    context_object_name = "category"
    slug_field = "slug"
    slug_url_kwarg = "category_slug"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        category = self.get_object()
        recipes = Recipe.objects.filter(category=category)
        context["recipes"] = recipes
        context["title"] = [f"Рецепти у категорії {self.category.title}"]
        context["title_content"] = [f"Рецепти у категорії {self.category.title}"]
        return context


class RecipeDetail(DetailView):
    model = Recipe
    template_name = "recipe/recipe.html"
    context_object_name = "recipe"
    slug_field = "slug"
    slug_url_kwarg = "recipe_slug"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        recipe = context["recipe"]
        ingredients_data = recipe.recipeingredient_set.all()
        context["ingredients_list"] = [
            f"{ri.ingredient.name} - {ri.unit if ri.unit else ''} можна замінити на{ri.substitutes if ri.substitutes else '' }"
            for ri in ingredients_data
        ]
        context["category_name"] = [
            category.title for category in recipe.category.all()
        ]
        context["title"] = "Пошук рецептів"
        return context


class AboutDetail(DetailView):
    model = About
    template_name = "recipe/about.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Про що сайт"
        context["title_content"] = (
            "Як шукати рецепти та ідеї, користуючись усіма можливостями сайту"
        )
        return context


class BlogList(ListView):
    model = Article
    template_name = "recipe/blog.html"
    context_object_name = "articles_list"
    queryset = Article.objects.all()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Блог"
        context["title_content"] = "Блог про корисне харчування"
        return context


class ArticleDetail(DetailView):
    model = Article
    template_name = "recipe/article.html"
    context_object_name = "article"
    slug_field = "slug"
    slug_url_kwarg = "article_slug"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Про ПП харчування"
        return context
