import decimal

from django.contrib.postgres.search import SearchVector, TrigramSimilarity
from django.db.models.functions import Greatest
from django.shortcuts import render

from .forms import SearchForm
from .models import PropertyForRent


def main_search(request):
    form = SearchForm()
    query = None
    results = []
    if 'query' in request.GET:
        form = SearchForm(request.GET)
        if form.is_valid():
            cd = form.cleaned_data
            query = cd['query']

            results = PropertyForRent.objects
            if query:
                results = results.annotate(
                    similarity=Greatest(TrigramSimilarity('address', query),
                                        TrigramSimilarity('title', query),
                                        TrigramSimilarity('source_site', query),),
                ).filter(similarity__gt=0.1).order_by('-similarity')
            results = results.filter(rooms__gte=cd['min_rooms'],
                                     rooms__lte=cd['max_rooms'])
            if cd['min_price'] and cd['max_price']:
                results = results.filter(price__gte=cd['min_price'],
                                         price__lte=cd['max_price'])
            for result in results:
                result.price = decimal.Decimal(result.price) / 100
    print(len(results), 'results!')
    return render(request,
                  'search/main.html',
                  {'form': form,
                   'query': query,
                   'results': results})