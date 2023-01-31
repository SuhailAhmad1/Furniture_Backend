from flask import Blueprint, jsonify, request
from application.models import Furniture, Customer, Order
from flask_jwt_extended import jwt_required, get_jwt_identity
from application.database import db
import json
from application.smtp import sendEmail
from application.logger import logger

order = Blueprint("order", __name__, url_prefix= "/api/v1")

# api to retreive all available furnitures
@order.get("/furnitures")
@jwt_required()
def all():
    try:

        all_furnitures = Furniture.query.all()
        userId = get_jwt_identity()
        user = Customer.query.filter(Customer.userId == userId).first()

        logger.debug("Getting the list of the furntures.")
        furnitures = []
        for fur in all_furnitures:
            furnitures.append({
                "furnitureId": fur.furnitureId,
                "furnitureName": fur.furnitureName,
                "furniturePrice": fur.furniturePrice,
                "furnitureColor": fur.furnitureColor
            })

        logger.debug("Furniture list retrieved successfully.")
        return jsonify({
            "user": {
            "userName": user.userName,
            "emailId": user.emailId
            },
            "furnitures": furnitures
        }),200
    
    except Exception as e:
        logger.error("Something went wrong while getting the list of furnitures.")
        logger.exception(e)
        return jsonify({"error": "Something went wrong."}),500

# api to place new orders
@order.post("/placeorder")
@jwt_required()
def createorder():
    try:
        input_data = json.loads(request.data)
        userId = get_jwt_identity()
        furnitureIds = input_data["furnitureIds"]
        
        # checking if all furnitures are available
        all_furnitures = Furniture.query.all()
        available_furniture_list = []
        for fur in all_furnitures:
            available_furniture_list.append(fur.furnitureId)

        for id in furnitureIds:
            if id not in available_furniture_list:
                logger.error("Not all Furnitures are available.")
                return jsonify({"error": "Some or all furniture ordered are not available currently..."}), 404

        # Creating new orders
        for id in furnitureIds:
            new_order = Order(userId = userId, furnitureId = id, orderStatus = "pending")
            db.session.add(new_order)
        
        db.session.commit()
        logger.info('Orders placed successfully')

        # Getting user email
        customer = Customer.query.filter(Customer.userId == userId).first()
        # Sending Email

        logger.info("Trying to send the email to the user.")
        sendEmail(customer.emailId, "Orders Placed", "Orders Placed Successfully")
        return jsonify({"success": "Orders Placed Successfully. Please Wait for the approval..."}), 200
    
    except Exception as e:
        logger.error("Something went wrong while placing new orders.")
        return jsonify({"error": "Something went wrong."}),500

# Deleting an order if only order status is pending
@order.delete("/cancelorder/<int:orderId>")
@jwt_required()
def deleteorder(orderId):
    try:
        request_user = get_jwt_identity()
        order = Order.query.filter(Order.orderId == orderId).first()

        # checking if the owner of this order itself is trying to delete or not
        if request_user == order.userId:
            if order.orderStatus == "pending":
                db.session.delete(order)
                db.session.commit()

                logger.debug("Order deleted successfully")

                # Getting user email
                customer = Customer.query.filter(Customer.userId == request_user).first()

                logger.info("Trying to send the mail to the user.")
                # Sending Email
                sendEmail(customer.emailId, "Order Canceleed", "Dear Customer Your Order has been Cancelled as per your request.")

                return jsonify({"success": "order deleted successfully..."}), 200
            
            logger.error("Order still in Pending state. Can not delete.")
            return jsonify({"error": "Can not delete order, As it is not in pending state."}), 401
        
        logger.error("Some One else is trying to delete the order")
        return jsonify({"error":"Not authorized user"}), 401
    
    except Exception as e:
        logger.error("Something went wrong while deleting order.")
        logger.exception(e)
        return jsonify({"error": "Something went wrong."}),500
