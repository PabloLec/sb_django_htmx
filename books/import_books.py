import csv
import unicodedata
from io import StringIO

import requests

from .models import Book

_URL = "https://www.gutenberg.org/cache/epub/feeds/pg_catalog.csv"


def import_gutenberg_books():
    print("Downloading CSV...")
    csv_data = download_csv()
    print(f"Imported {len(csv_data)} lines from CSV.")
    books = map_to_books(csv_data)
    book_saved_count = save_books(books)
    print(f"Saved {book_saved_count} new books.")


def download_csv() -> list[dict[str, str]]:
    response = requests.get(_URL)
    response.raise_for_status()

    csv_file = StringIO(response.text)
    csv_reader = csv.DictReader(csv_file)

    return [
        {"Issued": row["Issued"], "Title": row["Title"], "Authors": row["Authors"]}
        for row in csv_reader
    ]


def normalize_string(string: str) -> str:
    return (
        unicodedata.normalize("NFKD", string.strip())
        .encode("ASCII", "ignore")
        .decode("ASCII")
    )


def map_to_books(books: list[dict[str, str]]) -> list[Book]:
    return [
        Book(
            title=normalize_string(book["Title"]),
            author=normalize_string(book["Authors"]),
            date=book["Issued"],
        )
        for book in books
        if all(len(s.strip()) > 0 for s in book.values())
    ]


def save_books(books: list[Book]) -> int:
    existing_book_tuples = set(
        Book.objects.filter(
            title__in={book.title for book in books},
            author__in={book.author for book in books},
        ).values_list("title", "author")
    )
    new_books = [
        book for book in books if (book.title, book.author) not in existing_book_tuples
    ]

    Book.objects.bulk_create(new_books)

    return len(new_books)
