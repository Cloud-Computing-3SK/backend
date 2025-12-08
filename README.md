**Backend Setup & Authentication Testing**

**Installation**
pip install -r requirements.txt

**Run Migrations**
python manage.py migrate

**Start the Server**
python manage.py runserver

**Test Registration**
curl -X POST http://127.0.0.1:8000/auth/register/ \
  -H "Content-Type: application/json" \
  -d "{\"username\":\"test\", \"email\":\"test@example.com\", \"password\":\"123456\"}"


**Expected Response:**

{"message": "User created successfully"}

**Test Login**
curl -X POST http://127.0.0.1:8000/auth/login/ \
  -H "Content-Type: application/json" \
  -d "{\"username\":\"test\", \"password\":\"123456\"}"


**Expected Response:**

{
  "access": "jwt_token_here",
  "refresh": "refresh_token_here"
}