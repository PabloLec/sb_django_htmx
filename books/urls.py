from django.urls import path

from . import views

urlpatterns = [
    path("import", views.import_books, name="import_books"),
]
