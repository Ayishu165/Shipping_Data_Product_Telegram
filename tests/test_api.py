# tests/test_api.py
import pytest
from httpx import AsyncClient
from fastapi.testclient import TestClient
from api.main import app

client = TestClient(app)

def test_root():
    response = client.get("/")
    assert response.status_code == 200

def test_top_products():
    response = client.get("/api/reports/top-products?limit=3")
    assert response.status_code == 200
    assert isinstance(response.json(), list)

def test_channel_activity():
    response = client.get("/api/channels/lobelia4cosmetics/activity")
    assert response.status_code in [200, 404]

def test_search_messages():
    response = client.get("/api/search/messages?query=vitamin")
    assert response.status_code == 200
