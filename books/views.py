from django.http import HttpResponse
from django.shortcuts import render

from .import_books import import_gutenberg_books


def search_book_page(request):
    return render(request, "search_book/search_book.html")


def import_books(request):
    import_gutenberg_books()
    return HttpResponse("Books imported")
