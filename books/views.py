from django.http import HttpResponse

from .import_books import import_gutenberg_books


def import_books(request):
    import_gutenberg_books()
    return HttpResponse("Books imported")
