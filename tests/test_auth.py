import pytest
from httpx import AsyncClient, ASGITransport
from app.main import app
import time

BASE_URL = "http://test"


@pytest.fixture
def test_user():
    return {
        "email": f"test{int(time.time())}@example.com",
        "password": "password123",
        "full_name": "Test User",
        "is_agent": False
    }


@pytest.fixture
def test_agent():
    return {
        "email": f"agent{int(time.time())}@example.com",
        "password": "password123",
        "full_name": "Test Agent",
        "is_agent": True
    }


@pytest.mark.asyncio
async def test_register_user(test_user):
    async with AsyncClient(transport=ASGITransport(app=app), base_url=BASE_URL) as client:
        res = await client.post("/api/auth/register", json=test_user)
        assert res.status_code == 201
        assert "id" in res.json()
        assert res.json()["email"] == test_user["email"]


@pytest.mark.asyncio
async def test_register_duplicate_email(test_user):
    async with AsyncClient(transport=ASGITransport(app=app), base_url=BASE_URL) as client:
        await client.post("/api/auth/register", json=test_user)
        res = await client.post("/api/auth/register", json=test_user)
        assert res.status_code == 400


@pytest.mark.asyncio
async def test_login_success(test_user):
    async with AsyncClient(transport=ASGITransport(app=app), base_url=BASE_URL) as client:
        await client.post("/api/auth/register", json=test_user)
        res = await client.post("/api/auth/login", json={
            "email": test_user["email"],
            "password": test_user["password"]
        })
        assert res.status_code == 200
        assert "access_token" in res.json()


@pytest.mark.asyncio
async def test_login_wrong_password(test_user):
    async with AsyncClient(transport=ASGITransport(app=app), base_url=BASE_URL) as client:
        await client.post("/api/auth/register", json=test_user)
        res = await client.post("/api/auth/login", json={
            "email": test_user["email"],
            "password": "wrongpassword"
        })
        assert res.status_code == 401
