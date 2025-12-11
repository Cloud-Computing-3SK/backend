# Backend Setup & Authentication Testing

## Installation

```bash
pip install -r requirements.txt
```

## Run Migrations

```bash
python manage.py makemigrations
python manage.py migrate
```

## Start the Server

```bash
python manage.py runserver
```

## API Endpoints

### Test Registration

```bash
curl -X POST http://127.0.0.1:8000/auth/register/ \
  -H "Content-Type: application/json" \
  -d '{"username":"test", "email":"test@example.com", "password":"123456"}'
```

**Expected Response:**

```json
{
    "message": "User created successfully",
    "user": {
        "auth_user_id": 1,
        "app_user_id": "generated_id_here",
        "username": "test",
        "email": "test@example.com"
    }
}
```

---

### Test Login

```bash
curl -X POST http://127.0.0.1:8000/auth/login/ \
  -H "Content-Type: application/json" \
  -d '{"username":"test", "password":"123456"}'
```

**Expected Response:**

```json
{
    "refresh": "refresh_token",
    "access": "access_token",
    "auth_user_id": "auth_user_id",
    "app_user_id": "app_user_id",
    "username": "test",
    "email": "test@example.com"
}
```

---

### Test Create Organization (Requires JWT Token)

```bash
curl -X POST http://127.0.0.1:8000/auth/organizations/create/ \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer <access_token>" \
  -d '{"name":"testorg"}'
```

**Expected Response:**

```json
{
    "message": "Organization successfully created",
    "organization": {
        "id": "id_org_here",
        "name": "testorg"
    }
}
```
**Error Handling:**
```json
{
  "error": "You have already created an organization"
}
```
```json
{
  "message": "Failed to create organization",
  "errors": {
    "name": [
      "organization with this name already exists."
    ]
  }
}
```
```json
{
  "detail": "Authentication credentials were not provided."
}
```
> **Note:** One user can only create one organization. The user who creates the organization is automatically assigned to it.

---

### Test Search User by Username (Requires JWT Token)

```bash
curl -X GET "http://127.0.0.1:8000/auth/users/search/?username=s" \
  -H "Authorization: Bearer <access_token>"
```

**Expected Response:**

```json
{
  "message": "Search completed",
  "count": 5,
  "users": [
    {
      "id": "0cb37cd0-64e8-478f-bcee-528c05c4274c",
      "username": "test",
      "email": "test@example.com",
      "organization": {
        "id": "d932d693-d117-41e9-abb3-54ef2a62718b",
        "name": "testorg"
      }
    },
    {
      "id": "bbb5f16f-a79a-439a-87e1-327062b6a574",
      "username": "kenisha",
      "email": "kenishajazlyn@gmail.com",
      "organization": {
        "id": "dd9f778d-f5a4-4d34-91e5-267643bed025",
        "name": "Cloud Computing 3SK"
      }
    },
    {
      "id": "c94b6481-113c-4d69-84cc-3b84a91b9bc5",
      "username": "syifa",
      "email": "syifa@gmail.com",
      "organization": {
        "id": "dd9f778d-f5a4-4d34-91e5-267643bed025",
        "name": "Cloud Computing 3SK"
      }
    },
    {
      "id": "010ed5ee-795a-4492-ac0c-272b4144e330",
      "username": "sitaa",
      "email": "sitaa@gmail.com",
      "organization": null
    },
    {
      "id": "0b613294-6628-41e1-b26b-c3fdd7504e94",
      "username": "sandriarania",
      "email": "sandria@gmail.com",
      "organization": null
    }
  ]
}
```

> **Note:** Search is case-insensitive and supports substring matching.



---

### Test Assign User to Organization (Requires JWT Token)

```bash
curl -X POST "http://127.0.0.1:8000/auth/organizations/assign-user/<id_user_here>/" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer <access_token>"
```

**Expected Response:**

```json
{
  "message": "User successfully assigned to organization",
  "organization": "Cloud Computing 3SK",
  "user": {
    "id": "c94b6481-113c-4d69-84cc-3b84a91b9bc5",
    "username": "syifa",
    "email": "syifa@gmail.com"
  }
}
```
**Error Handling:**
```json
{
  "message": "You are not part of any organization"
}
```
> **Note:** Only users who are already part of an organization can assign other users. The user will be assigned to the assigner's organization.

---

### Test Get All Members in Your Organization (Requires JWT Token)

```bash
curl -X GET "http://127.0.0.1:8000/auth/organizations/users/" \
  -H "Authorization: Bearer <access_token>"
```

**Expected Response:**

```json
{
  "message": "Users successfully retrieved",
  "organization": "Cloud Computing 3SK",
  "count": 2,
  "users": [
    {
      "id": "bbb5f16f-a79a-439a-87e1-327062b6a574",
      "username": "kenisha",
      "email": "kenishajazlyn@gmail.com",
      "organization": {
        "id": "dd9f778d-f5a4-4d34-91e5-267643bed025",
        "name": "Cloud Computing 3SK"
      }
    },
    {
      "id": "c94b6481-113c-4d69-84cc-3b84a91b9bc5",
      "username": "syifa",
      "email": "syifa@gmail.com",
      "organization": {
        "id": "dd9f778d-f5a4-4d34-91e5-267643bed025",
        "name": "Cloud Computing 3SK"
      }
    }
  ]
}
```
**Error Handling:**

```json
{
  "error": "You are not part of any organization"
}
```
> **Note:** Returns all members of the organization that the authenticated user belongs to. If the user is not part of any organization, returns: `{"message": "You are not part of any organization"}`

---

### Test Get Notes (Requires JWT Token)

```bash
curl -X GET "http://127.0.0.1:8000/api/notes/" \
  -H "Authorization: Bearer <access_token>"
```

**Expected Response:**

```json
{
  "organization": "Cloud Computing 3SK",
  "notes": [
    {
      "id": 1,
      "username": "kenisha",
      "title": "Deadline Cloud",
      "notes": "Kumpulka mingu depan",
      "deadline": "2025-12-20",
      "status": "todo",
      "created_at": "2025-12-11T11:19:58.997339Z",
      "updated_at": "2025-12-11T11:37:38.146660Z",
      "user": 2,
      "organization": "dd9f778d-f5a4-4d34-91e5-267643bed025"
    },
    {
      "id": 2,
      "username": "syifa",
      "title": "Deadline Tugas Cloud",
      "notes": "Kumpulkan minggu depan",
      "deadline": "2025-12-20",
      "status": "todo",
      "created_at": "2025-12-11T11:20:22.575371Z",
      "updated_at": "2025-12-11T11:20:22.575403Z",
      "user": 3,
      "organization": "dd9f778d-f5a4-4d34-91e5-267643bed025"
    }
  ]
}
```

> **Note:** Returns all notes from the user's organization (not just their own notes). If user is not part of an organization.
