from django.urls import path

from . import views

urlpatterns = [
    path("", views.search_book_page, name="search_book"),
    path("import", views.import_books, name="import_books"),
]
