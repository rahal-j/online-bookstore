from flask import Blueprint, request, jsonify
import requests
import json
from .models import Order
from . import db

order_bp = Blueprint('order_bp', __name__)

BOOK_SERVICE_URL = "http://product-service:5050/books"  # External call to product service

@order_bp.route('/orders', methods=['POST'])
def create_order():
    data = request.json  # Expected: { "user": "rahal", "email": "rahal@example.com", "items": [{ "id": 1, "quantity": 2 }] }

    books_info = []
    total_price = 0.0

    for item in data.get("items", []):
        res = requests.get(BOOK_SERVICE_URL)
        books = res.json()
        book = next((b for b in books if b['id'] == item['id']), None)

        if not book:
            return jsonify({"message": f"Book ID {item['id']} not found"}), 404

        subtotal = book["price"] * item["quantity"]
        total_price += subtotal
        books_info.append({
            "id": book["id"],
            "title": book["title"],
            "quantity": item["quantity"],
            "price": book["price"],
            "subtotal": subtotal
        })

    order = Order(books=json.dumps(books_info), total=total_price)
    db.session.add(order)
    db.session.commit()

    # 🔔 Notify user
    try:
        requests.post("http://notification-service:5053/notify", json={
            "type": "order",
            "user": data.get("user"),
            "email": data.get("email"),
            "order_id": order.id,
            "total": total_price
        })
    except Exception as e:
        print("Failed to send order notification:", e)

    return jsonify(order.to_dict()), 201


@order_bp.route('/orders', methods=['GET'])
def get_orders():
    orders = Order.query.all()
    return jsonify([o.to_dict() for o in orders])
