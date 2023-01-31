# Furniture_Backend
Hi,  
So This is the backend(apis) for a furniture company.  
After cloning this repo. Create and activate the virtual env.  
And run `pip intsall -r requuirement.txt`, It will install all the necessary libraries used in this project.

## Main libraries used are :
1. Flask : For creating the server and the apis.
2. flask-sqlalchemy : ORM.
3. smtplib : For sending email notification to the users.
4. flask-extended-jwt : For implementing token based authentication.
5. logging : To create log files

**MySQL** database is used.

## Authentication and login apis:

##### 1. To create new User. Both user and admin can access this.
    localhost:5000/api/v1/auth/register
    Use the "POST" method on this endpoint and add a raw payload with your request in the form:
    {
        "userName": "Sayar Ahmad Rather",
        "emailId":"suhiinu1@gmail.com",
        "password": "331998ss"
    }
    This api will create new User if the user is not registered already and   
    will send the user a mail notification about successfull registration.
      
    The response will be like:
    {
    "success": "New customer created Successfully"
    } 

#### 2. To login . Same endpoint for both user and admin.
    localhost:5000/api/v1/auth/login
    "POST" request on it with a raw payload of the form:
    {
        "emailId":"suhiinu@gmail.com",
        "password":"331998ss"
    } 
    If login details are correct it will create JWT token and send it with json as response like:
    {
    "user": {
        "access": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJmcmVzaCI6ZmFsc2UsImlhdCI6MTY3NTE3MTEwOSwianRpIjoiMjA1MTQyYjgtZTU2MS00ZmZmLTkwZDktZDc2NzViODA0N2MyIiwidHlwZSI6ImFjY2VzcyIsInN1YiI6MTEsIm5iZiI6MTY3NTE3MTEwOSwiZXhwIjoxNjc1MTcyMDA5fQ.StdRWpZUzi99DS6uoyFEXgoLWD-4wkPdNMjLe-qpkkM",
        "email": "suhiinu@gmail.com",
        "username": "Suhail Ahmad Bhat"
    }
    }
    The user/admin has to use this access token to access other apis


## Customer APIs:
#### 1. Api to retrieve all the furniture.
    localhost:5000/api/v1/furnitures

    "GET" request on this endpoint with the token recieved during login and if everything is right, The response will be like:
    {
    "furnitures": [
        {
            "furnitureColor": "Blue",
            "furnitureId": 1,
            "furnitureName": "Bed",
            "furniturePrice": 100
        },
        {
            "furnitureColor": "Red",
            "furnitureId": 2,
            "furnitureName": "Sofa",
            "furniturePrice": 1000
        },
    ],
    "user": {
        "emailId": "suhiinu@gmail.com",
        "userName": "Suhail Ahmad Bhat"
    }

#### 2. API to place an Order:
    localhost:5000/api/v1/placeorder

    "POST" request on this endpoint with the token recieved during login, with payload having the furniture Ids for order, of format:
    {
    "furnitureIds": [2,3]
    }
    If success the email notification will be sent to the user for placing the order and response will be like:
    Response after no error will be like
    {
    "success": "Orders Placed Successfully. Please Wait for the approval..."
    }

#### 3. API to Delete an order if only status is pending:
    localhost:5000/api/v1/cancelorder/<orderNo>

    "DELETE" request on this endpoint and change orderNo with the orderId which has to be deleted and also send the access token   
    recieved during login.
    The response after no error will be like
    {
    "success": "order deleted successfully..."
    }
    

## Admin APIs (Role Based authentication Done in every admin api)
#### 1. Api to edit / update customer details like username and password:
    localhost:5000/api/v1/admin/edit/<customerId>

    "PUT" request on this endpoint and change customerId with a customerId whose details has to be edited. Also give access token 
    and payload with updated values for username and password, of format
    {
    "userName": "Hil Bhat",
    "password": "12345"
    }

    Response after no error will be like
    {
    "success": "Customer details edited successfully"
    }

#### 2. API to Delete a User:
    localhost:5000/api/v1/admin/delete/<customerId>
    "DELETE" request on this endpoint and change customerId with the userId who has to be deleted and also send the access token  
    recieved during login.
    
    Response after no error will be like
    {
    "success": "User deleted successfully"
    }
    
#### 3. API to view all orders from all customers
    localhost:5000/api/v1/admin/allorders

    "GET" request on this endpoint with the token recieved during login and if everything is right, The response will be like:
    {
    "all_orders": [
        {
            "furnitureName": "Bed",
            "orderId": 1,
            "orderStatus": "pending",
            "userName": "Hil Bhat"
        },
        {
            "furnitureName": "Bed",
            "orderId": 2,
            "orderStatus": "fullfilled",
            "userName": "Khalid"
        },
        {
            "furnitureName": "Bed",
            "orderId": 3,
            "orderStatus": "fullfilled",
            "userName": "Suhail Ahmad Bhat"
        }
    ]
    }

#### 4. API to approve order:
    localhost:5000/api/v1/admin/approveorder/<order_id>

    "PUT" request on this endpoint and change order_id with an orderId that has to be approved. Also give access token 
    If no error it will send an email notification to the user about the status change. And the response will be like
    {
    "success": "Approved successfully..."
    }

#### 5. API to fullfill order:
    localhost:5000/api/v1/admin/fullfillorder/<order_id>

    "PUT" request on this endpoint and change order_id with an orderId that has to be approved. Also give access token 
    If no error it will send an email notification to the user about the status change. And the response will be like
    {
    "success": "Full filled order successfully..."
    }
