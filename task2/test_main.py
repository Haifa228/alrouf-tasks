from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def test_create_quote():
    response = client.post(
        "/quote",
        json={
            "client": {"name": "Gulf Eng.", "contact": "omar@client.com", "lang": "en"},
            "currency": "SAR",
            "items": [
                {"sku": "ALR-SL-90W", "qty": 120, "unit_cost": 240.0, "margin_pct": 22},
                {"sku": "ALR-OBL-12V", "qty": 40, "unit_cost": 95.5, "margin_pct": 18}
            ],
            "delivery_terms": "DAP Dammam, 4 weeks",
            "notes": "Client asked for spec compliance with Tarsheed."
        }
    )
    assert response.status_code == 200
    data = response.json()
    assert "grand_total" in data
    assert data["grand_total"] > 0
    assert "email_draft" in data
