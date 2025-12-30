from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Float, Boolean, Enum
from sqlalchemy.orm import relationship
from app import db, app
from datetime import datetime
from flask_login import UserMixin
from enum import Enum as UserEnum


class BaseModel(db.Model):
    __abstract__ = True
    id = Column(Integer, primary_key=True, autoincrement=True)

class Category(BaseModel):
    __tablename__ = 'category'

    name = Column(String(20), nullable=False)
    products = relationship('Product', backref='category', lazy=True)

    def __str__(self):
        return self.name


class Product(BaseModel):
    __tablename__ = 'product'

    name = Column(String(30), nullable=False)
    description = Column(String(255))
    price = Column(Float, nullable=False)
    image = Column(String(100))
    quantity = Column(Integer, nullable=False)
    create_date = Column(DateTime, default=datetime.now)
    active = Column(Boolean, default=True)
    category_id = Column(Integer, ForeignKey(Category.id), nullable=False)
    receipt_detail = relationship('ReceiptDetail', backref='product', lazy=True)

    def __str__(self):
        return self.name

class UserRole(UserEnum):
    ADMIN = 1
    USER = 2

class User(BaseModel, UserMixin):
    __tablename__ = 'user'
    name = Column(String(30), nullable=False)
    username = Column(String(30), nullable=False, unique=True)
    password = Column(String(255), nullable=False)
    email = Column(String(50))
    phone_number = Column(String(10))
    avatar = Column(String(100))
    active = Column(Boolean, default=True)
    join_date = Column(DateTime, default=datetime.now)
    user_role = Column(Enum(UserRole), default=UserRole.USER)
    receipts = relationship('Receipt', backref='user', lazy=True)

    def __str__(self):
        return self.name

class Receipt(BaseModel):
    __tablename__ = 'receipt'
    user_id = Column(Integer, ForeignKey(User.id), nullable=False)
    created_date = Column(DateTime, default=datetime.now)
    details = relationship('ReceiptDetail', backref='receipt', lazy=True)

class ReceiptDetail(db.Model):
    __tablename__ = 'receipt_detail'
    receipt_id = Column(Integer, ForeignKey(Receipt.id), nullable=False, primary_key=True)
    product_id = Column(Integer, ForeignKey(Product.id), nullable=False, primary_key=True)
    quantity = Column(Integer, default=0)
    unit_price = Column(Float, default=0)
    # receipt_date = Column(DateTime, default=datetime.now)

    @property
    def total_amount(self):
        return sum(d.quantity * d.unit_price for d in self.details)


if __name__ == '__main__':
    with app.app_context():
        db.create_all()

    # with app.app_context():
    #     c1 = Category(name = 'Cà phê')
    #     c2 = Category(name = 'Trà')
    #     c3 = Category(name = 'Freeze')
    #
    #     db.session.add(c1)
    #     db.session.add(c2)
    #     db.session.add(c3)
    #
    #     db.session.commit()