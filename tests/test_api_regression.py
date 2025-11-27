import pytest 
from app.api import create_app

DAY1 = "2024-11-01"
DAY2 = "2024-11-02"

@pytest.fixture()
def client():
    
    """
    Create a test client for the Flask application.
    """

    app = create_app()
    app.config['TESTING'] = True
    return app.test_client()

def _get_summary(client, date: str) -> dict:
    """Call the API and return JSON, to show a successful response."""
    res = client.get(f"/metrics/daily-summary?date={date}")
    assert res.status_code == 200, f"Expected 200 for date={date}, got {res.status_code}: {res.get_json()}"
    return res.get_json()

def test_transactions_do_not_regress_more_than_5_percent(client):
    """
    This is to test my Regression rule:
    - total_transactions on DAY2 should not drop more than 5% vs DAY1

    """
    d1 = _get_summary(client, DAY1)
    d2 = _get_summary(client, DAY2)

    assert d1["total_transactions"] > 0, "DAY1 total_transactions should be > 0 for this regression test to pass"
    assert d2["total_transactions"] >= d1["total_transactions"] * 0.95

def test_revenue_do_not_regress_more_than_10_percent(client):
    """
    Regression rule:
    - total_revenue on DAY2 should not drop more than 10% vs DAY1

    """
    d1 = _get_summary(client, DAY1)
    d2 = _get_summary(client, DAY2)

    assert d1["total_revenue"] > 0, "DAY1 total_revenue should be > 0 for this regression test to pass"
    assert d2["total_revenue"] >= d1["total_revenue"] * 0.90

def test_avg_rating_does_not_shift_more_than_point_3(client):
    """
    Regression rule:
    - avg_rating should not shift wildly day-to-day..
    """
    d1 = _get_summary(client, DAY1)
    d2 = _get_summary(client, DAY2)

    assert abs(d2["avg_rating"] - d1["avg_rating"]) <= 0.30