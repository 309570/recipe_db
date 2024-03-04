from django.core.management.base import BaseCommand
from django.test.client import RequestFactory
from django.http import QueryDict
from recipe.forms import SearchForm
from recipe.search_logic import get_check_ingredients, get_selected_categories


class Command(BaseCommand):
    help = "Отладка функции поиска"
    def handle(self, *args, **options):
        query_dict = QueryDict("ingredient=2&ingredient=3", mutable=True)
        request = RequestFactory().get("/fake-url/", query_dict)
        form = SearchForm(request.GET)

        if form.is_valid():
            filter_result, filter_error = get_check_ingredients(form)
            print(f"Filter result: {filter_result}, Filter error: {filter_error}")
        else:
            print("Form is not valid:", form.errors)
