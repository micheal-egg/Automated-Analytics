import pytest
from app.api import create_app

@pytest.fixture()

def client():
    
    """
    Create a test client for the Flask application.
    """

    app = create_app()
    app.config['TESTING'] = True
    return app.test_client()

def test_health_endpoint(client):
    """
    Confirm the service is alive and returns expected JSON.
    """
    res = client.get("/health")
    assert res.status_code == 200
    assert res.get_json() == {"status": "ok"}


