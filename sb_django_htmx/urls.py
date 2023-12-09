from django.contrib import admin
from django.urls import include, path

from books import views

urlpatterns = [
    path("__reload__/", include("django_browser_reload.urls")),
    path("admin/", admin.site.urls),
    path("", views.main, name="search_book"),
    path("books/", include("books.urls")),
]
