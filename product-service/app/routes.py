from flask import Blueprint, request, jsonify
from .models import Book
from . import db

book_bp = Blueprint('book_bp', __name__)

@book_bp.route('/books', methods=['GET'])
def get_books():
    books = Book.query.all()
    result = [
        {"id": b.id, "title": b.title, "author": b.author, "price": b.price, "stock": b.stock}
        for b in books
    ]
    return jsonify(result)

@book_bp.route('/books', methods=['POST'])
def add_book():
    data = request.json
    book = Book(
        title=data['title'],
        author=data['author'],
        price=data['price'],
        stock=data['stock']
    )
    db.session.add(book)
    db.session.commit()
    return jsonify({"message": "Book added!"}), 201
