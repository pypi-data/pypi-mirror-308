import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient
from fastapi_apm.middleware import MonitorMiddleware
from unittest.mock import AsyncMock, patch

WEBHOOK_URL = "https://mock-webhook-url.com/webhook"  # Mocked webhook URL

# Create a sample FastAPI application with the middleware applied
app = FastAPI()
app.add_middleware(MonitorMiddleware, webhook_url=WEBHOOK_URL)

# Sample routes for testing
@app.get("/success")
async def success_route():
    return {"message": "Success"}

@app.get("/client_error", status_code=400)
async def client_error_route():
    return {"error": "Client Error"}

@app.get("/server_error", status_code=500)
async def server_error_route():
    return {"error": "Server Error"}

# Using FastAPI's TestClient for synchronous testing
client = TestClient(app)


@pytest.fixture
def mock_httpx():
    """Fixture to mock the httpx AsyncClient post method"""
    with patch("httpx.AsyncClient.post", new=AsyncMock()) as mock_post:
        yield mock_post


def test_success_route_does_not_trigger_webhook(mock_httpx):
    """Test that a status code less than 400 does not trigger a webhook call"""
    response = client.get("/success")
    assert response.status_code < 400
    mock_httpx.assert_not_called()  # No webhook should be sent for status code less than 400


def test_client_error_route_triggers_webhook(mock_httpx):
    """Test that a 400 status code triggers a webhook call with the correct data"""
    response = client.get("/client_error")
    assert response.status_code == 400

    # Verify webhook was called once with expected data
    mock_httpx.assert_called_once()
    args, kwargs = mock_httpx.call_args
    assert args[0] == WEBHOOK_URL  # Ensure the webhook URL is correct
    print(WEBHOOK_URL)

    # Check payload structure
    payload = kwargs["json"]
    assert payload["event_name"] != None
    assert payload["message"] != None
    assert payload["username"] != None


def test_server_error_route_triggers_webhook(mock_httpx):
    """Test that a 500 status code triggers a webhook call with the correct data"""
    response = client.get("/server_error")
    assert response.status_code == 500

    # Verify webhook was called once with expected data
    mock_httpx.assert_called_once()
    args, kwargs = mock_httpx.call_args
    assert args[0] == WEBHOOK_URL  # Ensure the webhook URL is correct

    # Check payload structure
    payload = kwargs["json"]
    assert payload["event_name"] != None
    assert payload["message"] != None
    assert payload["username"] != None
