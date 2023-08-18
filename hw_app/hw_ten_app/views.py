import json
from datetime import datetime
from pathlib import Path

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required

from .forms import AuthorForm, TagForm, QuoteForm
from .models import Author, Tag, Quote


# Create your views here.
def index(request):
    quote = Quote.objects.all()
    return render(request, "hw_ten_app/index.html", {"quote": quote})


@login_required
def fill_db(request):
    quotes = Quote.objects.all()
    with open(str(Path(__file__).resolve().parent) + '/static/hw_ten_app/authors.json', 'r', encoding='utf-8') as fh:
        results = json.load(fh)
        for result in results:
            new_author = Author(description=result['description'][:1000],
                                born_date=datetime.strptime(result['born_date'], '%B %d, %Y').date(),
                                born_location=result['born_location'],
                                fullname=result['fullname']
                                )
            new_author.save()

    with open(str(Path(__file__).resolve().parent) + '/static/hw_ten_app/quotes.json', 'r', encoding='utf-8') as fh:
        results = json.load(fh)
        unique_tags = set()
        for result in results:
            [unique_tags.add(current_tag) for current_tag in result['tags']]

        for unique_tag in unique_tags:
            new_tag = Tag(name=unique_tag)
            new_tag.save()

        for result in results:
            new_quote = Quote()
            aut_id = Author.objects.get(fullname=result['author'])
            new_quote.quote = result['quote'][0:500]
            new_quote.author = aut_id
            new_quote.save()

            choice_tags = Tag.objects.filter(name__in=result['tags'])

            [new_quote.tags.add(choice_tag) for choice_tag in choice_tags.iterator()]
            new_quote.save()

    return render(request, 'hw_ten_app/index.html', {"quotes": quotes})


def detail(request, author_id):
    author_ob = get_object_or_404(Author, pk=author_id)
    return render(request, 'hw_ten_app/detail.html', {"author": author_ob})


def authors(request):
    author = Author.objects.all()
    return render(request, 'hw_ten_app/authors.html', {"author": author})


@login_required
def author(request):
    if request.method == "POST":
        form = AuthorForm(request.POST)

        if form.is_valid():
            form.save()
            return redirect(to='hw_ten_app:main')
        return render(request, 'hw_ten_app/author.html', {'form': form})

    return render(request, 'hw_ten_app/author.html', {'form': AuthorForm()})


@login_required
def tag(request):
    if request.method == "POST":
        form = TagForm(request.POST)

        if form.is_valid():
            form.save()
            return redirect(to='hw_ten_app:main')
        return render(request, 'hw_ten_app/tag.html', {'form': form})

    return render(request, 'hw_ten_app/tag.html', {'form': TagForm()})


@login_required
def quote(request):
    tags = Tag.objects.all()
    authors = Author.objects.all()

    if request.method == "POST":
        form = QuoteForm(request.POST)

        if form.is_valid():
            new_quote = Quote()
            new_quote.quote = request.POST.get('quote')
            new_quote.author = Author.objects.get(fullname=request.POST.get('author'))
            new_quote.save()

            choice_tags = Tag.objects.filter(name__in=request.POST.getlist('tags'))

            [new_quote.tags.add(choice_tag) for choice_tag in choice_tags.iterator()]
            new_quote.save()

            quotes = Quote.objects.all()
            return render(request, 'hw_ten_app/index.html', {'quotes': quotes})
        else:
            return render(request, 'hw_ten_app/quote.html', {'tags': tags, 'authors': authors, 'form': form})

    return render(request, 'hw_ten_app/quote.html', {'tags': tags, 'authors': authors, 'form': QuoteForm()})
