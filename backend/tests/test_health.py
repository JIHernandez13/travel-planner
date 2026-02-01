def test_root(client):
    response = client.get("/")
    assert response.status_code == 200
    data = response.json()
    assert data["message"] == "Welcome to Travel Planner API"
    assert data["version"] == "1.0.0"
    assert data["status"] == "running"


def test_health_check(client):
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "healthy"}
