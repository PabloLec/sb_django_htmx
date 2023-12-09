from django.urls import path

from . import views

urlpatterns = [
    path("", views.main, name="search_book"),
    path("cover", views.get_cover, name="get_cover"),
    path("import", views.import_books, name="import_books"),
]
