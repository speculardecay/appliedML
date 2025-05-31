import pytest
from library.library import Library
from library.book import Book

@pytest.fixture
def library():
    database = "./tests/test_database.json"
    library = Library(database)
    library.empty_library()
    return library

def test_get_all_books(library):
    book1 = Book("Dune", "Frank Herbert", "Science Fiction", 1, 0)
    book2 = Book("The Hobbit", "Fantasy", "J. R. R. Tolkien", 1, 0)
    library.add_book_to_library(book1)
    library.add_book_to_library(book2)
    retrieved_books = library.get_all_books()
    names_to_compare = [book1.name, book2.name]
    results = [book_data["name"] for book_id, book_data in retrieved_books["Books"].items()]
    assert names_to_compare == results

def test_search_book(library):
    book = Book("Dune", "Frank Herbert", "Science Fiction", 1, 0)
    library.add_book_to_library(book)
    books_list = library.search_books("Dune")
    assert books_list[0].name == "Dune"

def test_search_retrieved_books(library):
    book = Book("Dune", "Frank Herbert", "Science Fiction", 0, 1)
    library.add_book_to_library(book)
    books_list = library.search_retrieved_books()
    assert books_list[0].user == 1

def test_empty_library(library):
    book = Book("Dune", "Frank Herbert", "Science Fiction", 1, 0)
    library.add_book_to_library(book)
    library.empty_library()
    assert len(library.get_all_books()["Books"].items()) == 0

