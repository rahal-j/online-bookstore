from app.models import Book

def test_book_model():
    book = Book(title="Test", author="Me", price=10.0, stock=5)
    assert book.title == "Test"
