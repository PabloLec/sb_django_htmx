import random
import re

from django.http import HttpResponse
from django.shortcuts import render

from .import_books import import_gutenberg_books
from .models import Book


def main(request):
    if request.GET.get("title", ""):
        return search(request)
    return render(request, "search_book/search_book.html")


def search(request):
    title_query = request.GET.get("title", "")
    books = Book.objects.filter(title__icontains=title_query)
    return render(request, "search_book/book_table.html", {"books": books})


def get_cover(request):
    title = request.GET.get("title")
    author = request.GET.get("author")
    date_str = request.GET.get("date")

    try:
        year = re.findall(r"\d{4}", date_str)[0]
    except IndexError:
        year = "Unknown"

    color = "#{:06x}".format(random.randint(0, 0xFFFFFF))

    return render(
        request,
        "search_book/book_cover.html",
        {"title": title, "author": author, "date": year, "color": color},
    )


def import_books(request):
    import_gutenberg_books()
    return HttpResponse("Books imported")
