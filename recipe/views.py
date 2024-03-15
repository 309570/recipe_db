from typing import Any
from django.db.models.query import QuerySet
from django.http import HttpResponse, HttpResponseNotFound, Http404
from django.views.generic import ListView, DetailView, View, TemplateView
from django.shortcuts import render, redirect, get_list_or_404
from recipe.models import Category, Ingredient, Recipe, About, AboutSection, Article
from .forms import SearchForm
from .search_logic import handle_search
from django.shortcuts import get_object_or_404
from dal import autocomplete


class IngredientAutocomplete(autocomplete.Select2QuerySetView):
    def get_queryset(self):
        qs = Ingredient.objects.all()
        if self.q:
            qs = qs.filter(name__istartswith=self.q)
            print("покажи ответ", self.q)
            return qs


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
        context['form'] = SearchForm(self.request.GET or None)
        search_result = handle_search(self.request)
        context.update(search_result)
        return context

    # def get(self, request, *args, **kwargs):
    #     context = handle_search(request)
    #     return render(request, self.template_name, context)
        # context.update(
        #     {
        #         "form": search_result.get("form"),
        #         "categories": search_result.get("categories"),
        #         "frequent_ingredients": search_result.get("frequent_ingredients"),
        #         "recipes": search_result.get("recipes"),
        #         "errors": search_result.get("recipes"),
        #         "title": "Пошук рецептів",
        #         "title_content": "Пошук рецептів за інгредієнтами та категоріями",
        #     }
        # )
        # return context


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
        context["title"] = f"Категорія {category.title}"
        context["title_content"] = f"Рецепти в категорії {category.title}"
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
            f"{ri.ingredient.name} - {ri.unit if ri.unit else ''}" + (f"  можна замінити на{ri.substitutes}" if ri.substitutes else "")
            for ri in ingredients_data
        ]
        context["category_name"] = [
            category.title for category in recipe.category.all()
        ]
        context["title"] = "Пошук рецептів"
        context["title_content"] = "Шукаємо рецепти та ідеї за інгредієнтами!"
        return context


class AboutDetail(TemplateView):
    template_name = "recipe/about.html"
    

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        about_site = About.objects.first()
        context["about"] = about_site
        context['sections'] = AboutSection.objects.filter(about=about_site)
        context["title"] = "Як користуватися"

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
