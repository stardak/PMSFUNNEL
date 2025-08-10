from datetime import datetime
from flask_sqlalchemy import SQLAlchemy

# Create db instance here, imported by app.py
db = SQLAlchemy()


class Visitor(db.Model):
    __tablename__ = 'visitors'

    id = db.Column(db.Integer, primary_key=True)
    visitor_id = db.Column(db.String(64), unique=True, nullable=False)
    variant = db.Column(db.String(1), nullable=False)  # 'A' or 'B'
    ip_address = db.Column(db.String(45))
    user_agent = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)


class Conversion(db.Model):
    __tablename__ = 'conversions'

    id = db.Column(db.Integer, primary_key=True)
    visitor_id = db.Column(db.String(64), nullable=False)
    variant = db.Column(db.String(1), nullable=False)  # 'A' or 'B'
    conversion_type = db.Column(db.String(20), default='typeform_click')
    ip_address = db.Column(db.String(45))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
