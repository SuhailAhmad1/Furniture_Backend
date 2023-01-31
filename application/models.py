from application.database import db

class Customer(db.Model):
    __tablename__ = 'userdata'
    userId = db.Column(db.Integer, autoincrement=True, primary_key=True)
    userName = db.Column(db.String(45))
    emailId = db.Column(db.String(45), primary_key = True)
    password = db.Column(db.Text())
    userRole = db.Column(db.String(45))
    
class Furniture(db.Model):
    __tablename__ = 'furnituredata'
    furnitureId = db.Column(db.Integer, autoincrement=True, primary_key=True)
    furnitureName = db.Column(db.String(45))
    furniturePrice = db.Column(db.Integer())
    furnitureColor = db.Column(db.String(45))

class Order(db.Model):
    __tablename__ = 'orderdata'
    orderId = db.Column(db.Integer, autoincrement=True, primary_key=True)
    userId = db.Column(db.Integer)
    furnitureId = db.Column(db.Integer)
    orderStatus = db.Column(db.Integer())