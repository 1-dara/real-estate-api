import pytest
from httpx import AsyncClient, ASGITransport
from app.main import app
import time

BASE_URL = "http://test"


async def get_agent_token():
    agent = {
        "email": f"agent{int(time.time())}@example.com",
        "password": "password123",
        "full_name": "Test Agent",
        "is_agent": True
    }
    async with AsyncClient(transport=ASGITransport(app=app), base_url=BASE_URL) as client:
        await client.post("/api/auth/register", json=agent)
    async with AsyncClient(transport=ASGITransport(app=app), base_url=BASE_URL) as client:
        res = await client.post("/api/auth/login", json={
            "email": agent["email"],
            "password": agent["password"]
        })
        return res.json()["access_token"]


async def get_user_token():
    user = {
        "email": f"user{int(time.time())}@example.com",
        "password": "password123",
        "full_name": "Test User",
        "is_agent": False
    }
    async with AsyncClient(transport=ASGITransport(app=app), base_url=BASE_URL) as client:
        await client.post("/api/auth/register", json=user)
    async with AsyncClient(transport=ASGITransport(app=app), base_url=BASE_URL) as client:
        res = await client.post("/api/auth/login", json={
            "email": user["email"],
            "password": user["password"]
        })
        return res.json()["access_token"]


@pytest.mark.asyncio
async def test_get_properties_public():
    async with AsyncClient(transport=ASGITransport(app=app), base_url=BASE_URL) as client:
        res = await client.get("/api/properties/")
        assert res.status_code == 200
        assert "properties" in res.json()


@pytest.mark.asyncio
async def test_get_properties_with_filter():
    async with AsyncClient(transport=ASGITransport(app=app), base_url=BASE_URL) as client:
        res = await client.get("/api/properties/?city=Lagos")
        assert res.status_code == 200
        assert "properties" in res.json()


@pytest.mark.asyncio
async def test_create_property_as_agent():
    token = await get_agent_token()
    async with AsyncClient(transport=ASGITransport(app=app), base_url=BASE_URL) as client:
        res = await client.post(
            "/api/properties/",
            json={
                "title": "Test Property",
                "description": "A test property",
                "price": 5000000,
                "location": "Lagos Island",
                "city": "Lagos",
                "state": "Lagos",
                "property_type": "apartment",
                "bedrooms": 3,
                "bathrooms": 2,
                "size_sqm": 120,
                "amenities": "Pool, Gym",
                "is_available": True
            },
            headers={"Authorization": f"Bearer {token}"}
        )
        assert res.status_code == 201
        assert res.json()["title"] == "Test Property"


@pytest.mark.asyncio
async def test_create_property_as_user_fails():
    token = await get_user_token()
    async with AsyncClient(transport=ASGITransport(app=app), base_url=BASE_URL) as client:
        res = await client.post(
            "/api/properties/",
            json={
                "title": "Should Fail",
                "description": "User trying to create",
                "price": 1000000,
                "location": "Abuja",
                "city": "Abuja",
                "state": "FCT",
                "property_type": "house",
                "bedrooms": 2,
                "bathrooms": 1,
                "size_sqm": 80,
                "amenities": "None",
                "is_available": True
            },
            headers={"Authorization": f"Bearer {token}"}
        )
        assert res.status_code == 403

BASE_URL = "http://test"


async def get_agent_token():
    agent = {
        "email": f"agent{int(time.time())}@example.com",
        "password": "password123",
        "full_name": "Test Agent",
        "is_agent": True
    }
    async with AsyncClient(transport=ASGITransport(app=app), base_url=BASE_URL) as client:
        await client.post("/api/auth/register", json=agent)
    async with AsyncClient(transport=ASGITransport(app=app), base_url=BASE_URL) as client:
        res = await client.post("/api/auth/login", json={
            "email": agent["email"],
            "password": agent["password"]
        })
        return res.json()["access_token"]


async def get_user_token():
    user = {
        "email": f"user{int(time.time())}@example.com",
        "password": "password123",
        "full_name": "Test User",
        "is_agent": False
    }
    async with AsyncClient(transport=ASGITransport(app=app), base_url=BASE_URL) as client:
        await client.post("/api/auth/register", json=user)
    async with AsyncClient(transport=ASGITransport(app=app), base_url=BASE_URL) as client:
        res = await client.post("/api/auth/login", json={
            "email": user["email"],
            "password": user["password"]
        })
        return res.json()["access_token"]


@pytest.mark.asyncio
async def test_get_properties_public():
    async with AsyncClient(transport=ASGITransport(app=app), base_url=BASE_URL) as client:
        res = await client.get("/api/properties/")
        assert res.status_code == 200
        assert "properties" in res.json()


@pytest.mark.asyncio
async def test_get_properties_with_filter():
    async with AsyncClient(transport=ASGITransport(app=app), base_url=BASE_URL) as client:
        res = await client.get("/api/properties/?city=Lagos")
        assert res.status_code == 200
        assert "properties" in res.json()


@pytest.mark.asyncio
async def test_create_property_as_agent():
    token = await get_agent_token()
    async with AsyncClient(transport=ASGITransport(app=app), base_url=BASE_URL) as client:
        res = await client.post(
            "/api/properties/",
            json={
                "title": "Test Property",
                "description": "A test property",
                "price": 5000000,
                "location": "Lagos Island",
                "city": "Lagos",
                "state": "Lagos",
                "property_type": "apartment",
                "bedrooms": 3,
                "bathrooms": 2,
                "size_sqm": 120,
                "amenities": "Pool, Gym",
                "is_available": True
            },
            headers={"Authorization": f"Bearer {token}"}
        )
        assert res.status_code == 201
        assert res.json()["title"] == "Test Property"


@pytest.mark.asyncio
async def test_create_property_as_user_fails():
    token = await get_user_token()
    async with AsyncClient(transport=ASGITransport(app=app), base_url=BASE_URL) as client:
        res = await client.post(
            "/api/properties/",
            json={
                "title": "Should Fail",
                "description": "User trying to create",
                "price": 1000000,
                "location": "Abuja",
                "city": "Abuja",
                "state": "FCT",
                "property_type": "house",
                "bedrooms": 2,
                "bathrooms": 1,
                "size_sqm": 80,
                "amenities": "None",
                "is_available": True
            },
            headers={"Authorization": f"Bearer {token}"}
        )
        assert res.status_code == 403
