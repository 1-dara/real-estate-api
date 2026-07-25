#  Real Estate Listing API

A fully functional, production-grade real estate listing backend built with **FastAPI** and **PostgreSQL**. Deployed and live. 

 **Live API Docs:** https://real-estate-api-1-6678.onrender.com/docs  
 **GitHub:** https://github.com/1-dara/real-estate-api

---

##  Features

- **JWT Authentication** — Secure register and login with access tokens
- **Role-Based Access Control** — Separate permissions for agents and regular users
- **Property Listings** — Full CRUD (Create, Read, Update, Delete)
- **Search & Filters** — Filter by city, state, price range, bedrooms, and property type
- **Pagination** — Efficient data loading with page and limit controls
- **Reviews System** — Users can leave star ratings and comments with business rules (no self-reviews, no duplicates)
- **Image Uploads** — Permanent cloud image storage via Cloudinary
- **Auto-generated Docs** — Interactive Swagger UI at `/docs`
- **Redis Caching** — GET endpoints cached for 5 minutes with automatic invalidation on create/update/delete
- **Rate Limiting** — 100 requests per minute per IP address to prevent API abuse
- **Docker** — fully containerized with Dockerfile and docker-compose for consistent deployment
- **CI/CD** — GitHub Actions pipeline runs tests automatically on every push to main
- **AI Assistant** — Natural language Q&A endpoint powered by OpenAI (GPT-4o-mini)



---

##  Tech Stack

| Technology | Purpose |
|---|---|
| FastAPI | Web framework |
| PostgreSQL | Database |
| SQLAlchemy (Async) | ORM |
| Alembic | Database migrations |
| JWT / OAuth2 | Authentication |
| bcrypt | Password hashing |
| Cloudinary | Image storage |
| Render | Deployment |
| Pydantic | Data validation |
| Redis | Caching layer for property/product/course listings |
| slowapi | Rate limiting middleware |
| Docker | Containerization |
| OpenAI API | AI-powered natural language responses |
| GitHub Actions | CI/CD pipeline |



---

##  Project Structure

```
real_estate_api/
├── app/
│   ├── main.py               # App entry point
│   ├── database.py           # PostgreSQL connection
│   ├── models/               # Database models
│   │   ├── user.py
│   │   ├── property.py
│   │   ├── property_image.py
│   │   └── review.py
│   ├── schemas/              # Pydantic validation schemas
│   │   ├── user.py
│   │   └── property.py
│   ├── routers/              # API route handlers
│   │   ├── auth.py
│   │   ├── properties.py
│   │   ├── uploads.py
│   │   └── reviews.py
│   └── core/
│       ├── config.py         # Environment settings
│       └── security.py       # JWT & password hashing
├── alembic/                  # Database migrations
├── requirements.txt
├── Procfile
└── README.md
```

---

##  API Endpoints

### Auth
| Method | Endpoint | Description | Auth |
|---|---|---|---|
| POST | `/api/auth/register` | Register a new user | ❌ |
| POST | `/api/auth/login` | Login and get JWT token | ❌ |

### Properties
| Method | Endpoint | Description | Auth |
|---|---|---|---|
| GET | `/api/properties/` | Get all properties with filters & pagination | ❌ |
| POST | `/api/properties/` | Create a new listing | ✅ Agents only |
| GET | `/api/properties/{id}` | Get a single property | ❌ |
| PUT | `/api/properties/{id}` | Update a property | ✅ Owner only |
| DELETE | `/api/properties/{id}` | Delete a property | ✅ Owner only |

### Reviews
| Method | Endpoint | Description | Auth |
|---|---|---|---|
| GET | `/api/properties/{id}/reviews` | Get reviews for a property | ❌ |
| POST | `/api/properties/{id}/reviews` | Leave a review | ✅ |

### Uploads
| Method | Endpoint | Description | Auth |
|---|---|---|---|
| POST | `/api/uploads/{id}/images` | Upload property image | ✅ Owner only |
| GET | `/api/uploads/{id}/images` | Get all images for a property | ❌ |

---
### AI Assistant
| Method | Endpoint | Description | Auth |
|---|---|---|---|
| POST | `/api/ai/ask` | Ask a natural language question and get an AI-generated answer | ✅ |

**Example:**
```bash
curl -X POST http://127.0.0.1:8000/api/ai/ask \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -d '{"question": "What should I look for when buying my first home?"}'
```

**Response:**
```json
{"answer": "Here are key things to consider..."}
```

---

##  Setup & Installation

1. **Clone the repository**
```bash
git clone https://github.com/1-dara/real-estate-api.git
cd real-estate-api
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

4. **Create a `.env` file**
```env
DATABASE_URL=postgresql+asyncpg://username@localhost:5432/real_estate_db
SECRET_KEY=your-secret-key
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
CLOUDINARY_CLOUD_NAME=your-cloud-name
CLOUDINARY_API_KEY=your-api-key
CLOUDINARY_API_SECRET=your-api-secret
OPENAI_API_KEY=your-openai-api-key
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
```
http://127.0.0.1:8000/docs
```

---

##  Author

**Irene Peter-Okon Idara**  
Backend Engineer  
 1ireneokon@gmail.com  
 github.com/1-dara
