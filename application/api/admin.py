from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required, get_jwt_identity
from application.models import Customer, Furniture, Order
import json
from application.database import db
from application.smtp import sendEmail
from application.logger import logger


admin = Blueprint("admin", __name__, url_prefix="/api/v1/admin")


# Editing the details of Customer only admin is allowed to do.
@admin.put("/edit/<int:userId>")
@jwt_required()
def edit(userId):
    try:
        requestUserId = get_jwt_identity()
        requestUser = Customer.query.filter(Customer.userId == requestUserId).first()
        role = requestUser.userRole

        # Checking for role
        logger.debug("Checking for authorization.")
        if role == "admin":
            input_data = json.loads(request.data)

            # Checking if all required data is available with the request
            keys = input_data.keys()
            if "userName" not in keys:
                logger.error("Missing details")
                return jsonify({"error": "Can not update as userName is missing..."}), 400
            if "password" not in keys:
                logger.error("Missing details")
                return jsonify({"error": "Can not update as password is missing..."}), 400
            
            # Checking for the User
            user = Customer.query.filter(Customer.userId == userId).first()
            if not user:
                logger.error("No user found.")
                return jsonify({"error": "Customer Not Found"}), 404
            
            # Updating
            logger.debug("Updating")
            if user:
                user.userName = input_data["userName"]
                user.password = input_data["password"]
                db.session.add(user)
                db.session.commit()
                logger.info("Successfully updated deatils of a customer.")
                return {'success':"Customer details edited successfully"}, 200
        
        logger.error("Unauthorized user")
        return jsonify({"error": "You can not edit Customer Details. Only admin can"}), 401
    
    except Exception as e:
        logger.error("Something went wrong")
        logger.exception(e)
        return jsonify({"error": "Something went wrong."}),500

# Deleting the details of Customer only admin is allowed to do.
@admin.delete("/delete/<int:userId>")
@jwt_required()
def delete(userId):
    try:

        requestUserId = get_jwt_identity()
        requestUser = Customer.query.filter(Customer.userId == requestUserId).first()
        role = requestUser.userRole

        # Checking for role
        if role == "admin":
            user = Customer.query.filter(Customer.userId == userId).first()

            if user:
                # First deleting the orders associated with this user
                orders = Order.query.filter(Order.userId == user.userId).all()
                for order in orders:
                    db.session.delete(order)
                db.session.commit()
                logger.debug("First deleted the orders associated with that customer.")

                # Now deleting the user
                db.session.delete(user)
                db.session.commit()
                logger.debug("User deleted successfully.")
                return jsonify({"success": "User deleted Successfully"}),200
            
            logger.error("User not found")
            return jsonify({"error":"User Not Found"}), 404
        
        logger.error("Unauthorized user")
        return jsonify({"error": "You can not edit Customer Details. Only admin can"}), 401
    
    except Exception as e:
        logger.error("Something went wrong")
        logger.exception(e)
        return jsonify({"error": "Something went wrong."}),500



# Getting the details of all orders
@admin.get("/allorders")
@jwt_required()
def user_orders():

    try:
        requestUserId = get_jwt_identity()
        requestUser = Customer.query.filter(Customer.userId == requestUserId).first()
        role = requestUser.userRole

        # Checking for role
        if role == "admin":
            orders= Order.query.all()
            order_list = []
            for ord in orders:
                user = Customer.query.filter(Customer.userId == ord.userId).first()
                furniture = Furniture.query.filter(Furniture.furnitureId).first()
                order_list.append({
                    "orderId": ord.orderId,
                    "userName": user.userName,
                    "furnitureName": furniture.furnitureName,
                    "orderStatus": ord.orderStatus
                })
            
            logger.debug("Orders retreived successfully")
            return jsonify({
                "all_orders": order_list
            }), 200
        
        logger.error("Unathorized User")
        return jsonify({"error":"Not for Users..."}),401
    
    except Exception as e:
        logger.error("Something went wrong")
        logger.exception(e)
        return jsonify({"error": "Something went wrong."}), 500

# api to approve customer order for admin
@admin.put("/approveorder/<int:order_id>")
@jwt_required()
def approve(order_id):
    try:
        requestUser = get_jwt_identity()
        user = Customer.query.filter(Customer.userId == requestUser).first()
        # Checking for role
        if user.userRole == "admin":
            order = Order.query.filter(Order.orderId == order_id).first()

            if order:
                order.orderStatus = "approved"
                db.session.add(order)
                db.session.commit()

                # Getting the customer details
                customer = Customer.query.filter(Customer.userId == order.userId).first()
                # Sending mail to the customer about approval of order
                print(sendEmail(customer.emailId, "Order Approved", "Dear "+customer.userName+", Your Order has been Approved"))

                logger.debug("Fullfilled and sent mail")
                return jsonify({"success": "Approved successfully..."}), 200
            
            logger.debug("Wrong order id")
            return jsonify({"error":"Can not find the order..."}), 404
        
        logger.debug("Unauthorized User.")
        return jsonify({"error":"Not for Users..."}),401
    except Exception as e:
        logger.error("Something went wrong")
        logger.exception(e)
        return jsonify({"error":"Something went Wrong"}), 500


# api to fullfill customer order for admin
@admin.put("/fullfillorder/<int:order_id>")
@jwt_required()
def fullfill(order_id):
    try:
        requestUser = get_jwt_identity()
        user = Customer.query.filter(Customer.userId == requestUser).first()

        if user.userRole == "admin":
            order = Order.query.filter(Order.orderId == order_id).first()
            if order:
                order.orderStatus = "fullfilled"
                db.session.add(order)
                db.session.commit()

                # Getting the customer details
                customer = Customer.query.filter(Customer.userId == order.userId).first()
                # Sending mail to the customer about approval of order
                print(sendEmail(customer.emailId, "Order Fullfilled", "Dear "+customer.userName+", Your Order has been fullfilled/delivered"))

                logger.debug("Fullfilled and sent mail")
                return jsonify({"success": "Full filled order successfully..."}), 200
            
            logger.debug("Wrong order id")
            return jsonify({"error":"Can not find the order..."}), 404
        
        logger.debug("Unauthorized User.")
        return jsonify({"error":"Not for Users..."}),401
    
    except Exception as e:
        logger.error("Something went wrong")
        logger.exception(e)
        return jsonify({"error": "Something went wrong"}), 500