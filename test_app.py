from app import app

def test_home():
    response=app.test_client().get("/")

    assert response.status_code == 200
    assert response.is_json
    assert response.get_json() == {"status": "API is up and running!"}


def test_training():
    response=app.test_client().get("/train")

    assert response.status_code==200
    assert response.data==b"Training Successful!"