from app import app
import json


def test_home():
    response=app.test_client().get("/")

    assert response.status_code == 200
    assert response.is_json
    assert response.get_json() == {"status": "API is up and running!"}


def test_training():
    response=app.test_client().get("/train")

    assert response.status_code==200
    assert response.data==b"Training Successful!"



def test_predict_tree_model():
    """Test prediction endpoint with tree model."""
    # Create test client
    tester = app.test_client()

    # Prepare request data
    payload = {
        "model": "tree",
        "MedInc": 7.5,
        "HouseAge": 30.0,
        "AveRooms": 6.0,
        "AveBedrms": 1.0,
        "Population": 850.0,
        "AveOccup": 2.5,
        "Latitude": 34.5,
        "Longitude": -120.5
    }

    # Send POST request to /predict
    response = tester.post(
        "/predict",
        data=json.dumps(payload),
        content_type='application/json'
    )

    # Check response
    assert response.status_code == 200
    assert response.is_json, "Response is not JSON"
    response_json = response.get_json()
    assert "model_used" in response_json
    assert "prediction" in response_json
    assert "unit" in response_json

    assert response_json["model_used"] == "tree"
    assert isinstance(response_json["prediction"], (float, int))
    assert response_json["unit"] == "x 100,000"



