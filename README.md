**Backend Setup & Authentication Testing**

**Installation**

pip install -r requirements.txt

**Run Migrations**

python manage.py makemigrations
python manage.py migrate

**Start the Server**

python manage.py runserver

**Test Registration**

curl -X POST http://127.0.0.1:8000/auth/register/ -H "Content-Type: application/json" -d "{\"username\":\"test\", \"email\":\"test@example.com\", \"password\":\"123456\"}"

**Expected Response:**

{
    "message": "User created successfully",
    "user": {
        "auth_user_id": 1,
        "app_user_id": "generated_id_here",
        "username": "test",
        "email": "test@example.com"
    }
}

**Test Login**

curl -X POST http://127.0.0.1:8000/auth/login/ -H "Content-Type: application/json" -d "{\"username\":\"test\", \"password\":\"123456\"}"

**Expected Response:**

{
    "refresh": "refresh_token",
    "access": "access_token",
    "auth_user_id": "auth_user_id",
    "app_user_id": "app_user_id",
    "username": "test",
    "email": "test@example.com"
}

**Test Create Org**

curl -X POST http://127.0.0.1:8000/auth/organizations/create/ -H "Content-Type: application/json" -d "{\"name\":\"testorg\"}"

**Expected Response:**

{"message":"Organization successfully created","organization":{"id":"id_user_here","name":"testorg"}}

**Test Assign User to Organization**

curl -X POST "http://127.0.0.1:8000/auth/organizations/<id_org_here>/assign-user/<id_user_here>/" -H "Content-Type: application/json"

**Expected Response:**
{
    "message": "User successfully assigned to organization",
    "organization": "testorg",
    "user": {
        "id": "id_user_here",
        "username": "test",
        "email": "test@example.com"
    }
}

**Test Get All Members ID by Org**

curl -X GET "http://127.0.0.1:8000/organizations/<id_org_here>/users/"

**Expected Response**

{
    "message": "Users successfully retrieved",
    "organization": "testorg",
    "count": 1,
    "users": [
        {
            "id": "id_user_here",
            "username": "test",
            "email": "test@example.com",
            "organization": {
                "id": "id_org_here",
                "name": "testorg"
            }
        }
    ]
}
