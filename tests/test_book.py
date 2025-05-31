from library.book import Book

def test_book_name()->None:
    book = Book("a", "b", "c", 0, 1)
    assert len(book.name) > 0

def test_book_author()->None:
    book = Book("a", "b", "c", 0, 1)
    assert len(book.author) > 0

def test_book_type()->None:
    book = Book("a", "b", "c", 0, 1)
    assert len(book.type) > 0