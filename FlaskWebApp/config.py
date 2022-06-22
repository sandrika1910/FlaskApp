from flask_sqlalchemy import SQLAlchemy as sl
from flask_login import UserMixin

db = sl()


class User(db.Model,UserMixin):
	id = db.Column(db.Integer,primary_key=True)
	username = db.Column(db.String(20),nullable=False)
	password = db.Column(db.String(60),nullable=False)

class Books(db.Model):
	id = db.Column(db.Integer,primary_key=True)
	comment = db.Column(db.String(50),nullable=False)
	book_price = db.Column(db.Float,nullable=False)
	book_name = db.Column(db.String(50),nullable=False)
	author_name = db.Column(db.String(30),nullable=False)
	book_img_url = db.Column(db.String(80),nullable=False)