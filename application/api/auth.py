from flask import Blueprint, request, jsonify
import json
from werkzeug.security import check_password_hash, generate_password_hash
from application.models import Customer, Furniture
from application.database import db
from flask_jwt_extended import create_access_token, jwt_required, unset_jwt_cookies, get_jwt_identity
from application.smtp import sendEmail
from application.logger import logger

auth = Blueprint("auth", __name__, url_prefix="/api/v1/auth")

@auth.post("/register")
def register():
    try:
        input_data = json.loads(request.data)

        # Checking if all required data is available with the request
        keys = input_data.keys()
        if "userName" not in keys:
            logger.error("Required details not given.")
            return jsonify({"error": "Can not create as userName is missing..."}), 400
        if "emailId" not in keys:
            logger.error("Required details not given.")
            return jsonify({"error": "Can not create as emailId is missing..."}), 400
        if "password" not in keys:
            logger.error("Required details not given.")
            return jsonify({"error": "Can not create as password is missing..."}), 400
        
        # Checking if the user might be already registered
        user = Customer.query.filter(Customer.emailId == input_data["emailId"]).first()
        if user:

            logger.error("User already exists")
            return jsonify({"error": "Customer already exists..."}), 409
        
        # Creating new user
        logger.debug("Creating new User")
        new_customer = Customer(userName = input_data["userName"], emailId = input_data["emailId"], password = input_data["password"], userRole = "user")
        db.session.add(new_customer)
        db.session.commit()
        logger.info("New User created")

        # sending user the registartion email
        logger.info("Sending User the mail about Successfull Registration")
        sendEmail(input_data["emailId"], "Registration Successfully Done.", "Your Registration has been Successfull")

        return jsonify({"success": "New customer created Successfully"}), 200
    
    except Exception as e:
        logger.error("Something went wrong while registration.")
        logger.exception(e)
        return jsonify({"error": "Something went wrong."}), 500

@auth.post("/login")
def login():
    try:
        login_data = json.loads(request.data)
        email = login_data["emailId"]
        password = login_data["password"]
        user = Customer.query.filter(Customer.emailId == email).first()

        # checking for correct password
        if user:
            if password == user.password:
                access = create_access_token(identity=user.userId)

                logger.debug("User successfully logged in.")
                return jsonify({
                    'user':{
                    'access': access,
                    'username': user.userName,
                    'email': user.emailId
                    }
                }),200

        logger.error("Wrong Crediantials.")
        return jsonify({"error":"Wrong crendiantials."}), 401
    
    except Exception as e:
        logger.error("Something went wrong while registration.")
        logger.exception(e)
        return jsonify({"error": "Something went wrong."}),500


@auth.get("/logout")
@jwt_required()
def logout():
    unset_jwt_cookies({"logout": "Success"})


