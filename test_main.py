from fastapi.testclient import TestClient
from main import app

# Create a test client
client = TestClient(app)

def test_read_root():
    """Check if the root endpoint works (status 200)."""
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "Welcome to StockGuard API - System is running"}

def test_create_item():
    """Test creating a new item."""
    item_payload = {
        "name": "Test Laptop",
        "quantity": 10,
        "price": 1500.00,
        "description": "Test description"
    }
    
    response = client.post("/items", json=item_payload)
    
    # Assertion 1: Is status code 200 OK?
    assert response.status_code == 200
    
    # Assertion 2: Does the response contain our data?
    data = response.json()
    assert data["name"] == "Test Laptop"
    assert "id" in data

def test_read_item():
    """
    Test scenario: Create item -> Retrieve it by ID
    """
    # 1. First, create an item
    create_response = client.post("/items", json={
        "name": "Unique Scanner",
        "quantity": 1,
        "price": 99.99
    })
    item_id = create_response.json()["id"]
    
    # 2. Then, try to retrieve it
    get_response = client.get(f"/items/{item_id}")
    
    assert get_response.status_code == 200
    assert get_response.json()["name"] == "Unique Scanner"