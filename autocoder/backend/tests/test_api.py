"""
Tests for Backend API Endpoints
"""

import pytest
import pytest_asyncio
from httpx import AsyncClient
from app.main import app


@pytest_asyncio.fixture
async def client():
    """FastAPI test client"""
    async with AsyncClient(app=app, base_url="http://test") as ac:
        yield ac


@pytest.mark.asyncio
async def test_health_check(client):
    """Test health check endpoint"""
    response = await client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "ok"


@pytest.mark.asyncio
async def test_root_endpoint(client):
    """Test root endpoint"""
    response = await client.get("/")
    assert response.status_code == 200
    assert "message" in response.json()


@pytest.mark.asyncio
async def test_generate_project_invalid_prompt(client):
    """Test project generation with invalid prompt"""
    response = await client.post(
        "/api/generate",
        json={"prompt": "short"}
    )
    assert response.status_code == 400


@pytest.mark.asyncio
async def test_get_memory(client):
    """Test get memory endpoint"""
    response = await client.get("/api/memory")
    assert response.status_code == 200
    data = response.json()
    assert "project_id" in data
    assert "project_spec" in data
    assert "status" in data


@pytest.mark.asyncio
async def test_get_status(client):
    """Test get status endpoint"""
    response = await client.get("/api/status")
    assert response.status_code == 200
    data = response.json()
    assert "status" in data
    assert "agents_status" in data
    assert "error_count" in data


@pytest.mark.asyncio
async def test_get_logs(client):
    """Test get logs endpoint"""
    response = await client.get("/api/logs")
    assert response.status_code == 200
    data = response.json()
    assert "total" in data
    assert "logs" in data


@pytest.mark.asyncio
async def test_reset_memory(client):
    """Test reset memory endpoint"""
    response = await client.post("/api/reset")
    assert response.status_code == 200
    assert "message" in response.json()


@pytest.mark.asyncio
async def test_logs_with_limit(client):
    """Test logs endpoint with limit parameter"""
    response = await client.get("/api/logs?limit=10")
    assert response.status_code == 200
    data = response.json()
    assert len(data["logs"]) <= 10
