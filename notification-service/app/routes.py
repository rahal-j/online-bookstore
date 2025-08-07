from flask import Blueprint, request, jsonify

notify_bp = Blueprint('notify_bp', __name__)

@notify_bp.route('/notify', methods=['POST'])
def notify():
    data = request.json
    ntype = data.get("type")

    if ntype == "registration":
        print(f"🔔 Sending welcome email to {data['email']} for user {data['user']}")
    elif ntype == "order":
        print(f"🔔 Sending order confirmation to {data['email']} for order #{data['order_id']} - total: ${data['total']}")
    else:
        print("🔔 Unknown notification type")

    return jsonify({"message": "Notification processed"}), 200
