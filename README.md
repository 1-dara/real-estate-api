# 🏠 Real Estate Listing API

A fully functional real estate listing backend built with **FastAPI**, **PostgreSQL**, and **JWT authentication**.

## 🚀 Features

- **User Authentication** — Register and login with JWT tokens
- **Property Listings** — Full CRUD (Create, Read, Update, Delete)
- **Search & Filters** — Filter properties by city, state, price range, bedrooms, and property type
- **Image Uploads** — Upload multiple images per property
- **Role Based Access** — Only agents can create and manage listings
- **Secure** — Passwords hashed with bcrypt, protected routes with JWT

## 🛠️ Tech Stack

- **Framework** — FastAPI
- **Database** — PostgreSQL
- **ORM** — SQLAlchemy (async)
- **Migrations** — Alembic
- **Authentication** — JWT (python-jose)
- **Password Hashing** — bcrypt (passlib)
- **Validation** — Pydantic

## ⚙️ Setup & Installation

1. **Clone the repository**
```bash
git clone https://github.com/yourusername/real_estate_api.git
cd real_estate_api
```

2. **Create virtual environment**
```bash
python3 -m venv venv
source venv/bin/activate
```

3. **Install dependencies**
```bash
pip install -r requirements.txt
```

4. **Create a `.env` file in the root folder**
```env
DATABASE_URL=postgresql+asyncpg://username@localhost:5432/real_estate_db
SECRET_KEY=your-secret-key
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
```

5. **Run database migrations**
```bash
alembic upgrade head
```

6. **Start the server**
```bash
uvicorn app.main:app --reload
```

7. **Visit the API docs**
http://127.0.0.1:8000/docs
## 🔑 API Endpoints

### Auth
| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/api/auth/register` | Register a new user |
| POST | `/api/auth/login` | Login and get JWT token |

### Properties
| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/properties/` | Get all properties with filters |
| POST | `/api/properties/` | Create a new listing (agents only) |
| GET | `/api/properties/{id}` | Get a single property |
| PUT | `/api/properties/{id}` | Update a property |
| DELETE | `/api/properties/{id}` | Delete a property |

### Uploads
| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/api/uploads/{id}/images` | Upload image for a property |
| GET | `/api/uploads/{id}/images` | Get all images for a property |