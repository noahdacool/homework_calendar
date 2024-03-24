from . import db
from flask_login import UserMixin
from sqlalchemy.sql import func

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(150), unique=True)
    password = db.Column(db.String(250))
    first_name = db.Column(db.String(150))

    categories = db.relationship('Category')

class Category(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(1000))
    color = db.Column(db.String(150))
    opacity = db.Column(db.Integer, default=100)
    index = db.Column(db.Integer)
    show = db.Column(db.Boolean, default=True)

    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    assignments = db.relationship('Assignment')

class Assignment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(1000))
    date = db.Column(db.DateTime(timezone=True))
    opacity = db.Column(db.Integer, default=100)
    index = db.Column(db.Integer, default=id)

    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    category_id = db.Column(db.Integer, db.ForeignKey('category.id'))