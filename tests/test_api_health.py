from fastapi.testclient import TestClient

import api.main


def test_health_endpoint_uses_cached_data(monkeypatch):
    client = TestClient(api.main.app)

    def fake_cached():
        return {
            "expenses": [{}],
            "donations": [{}],
            "almanot": [{}],
            "investors": [{}],
            "budget_status": {},
            "donor_stats": {},
            "widow_stats": {},
            "network_data": {},
        }

    monkeypatch.setattr(api.main, "get_cached_data", fake_cached)

    response = client.get("/api/health")
    assert response.status_code == 200
    payload = response.json()
    assert payload["status"] == "healthy"
    assert payload["record_counts"]["expenses"] == 1
