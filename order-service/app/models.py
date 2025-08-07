from . import db
import json

class Order(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    books = db.Column(db.Text, nullable=False)  # JSON string
    total = db.Column(db.Float, nullable=False)

    def to_dict(self):
        return {
            "id": self.id,
            "books": json.loads(self.books),
            "total": self.total
        }
