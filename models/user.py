from datetime import datetime
from . import db
import uuid

class User(db.Model):
    __tablename__ = 'User'
    
    id = db.Column(db.Integer, primary_key=True)
    public_id = db.Column(db.String(50), unique=True, default=lambda: str(uuid.uuid4()))
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    date = db.Column(db.DateTime, default=datetime.now)
    password = db.Column(db.String(120), nullable=False)

    def __init__(self, public_id, name, email, password):
        self.public_id = public_id
        self.name = name
        self.email = email
        self.password = password