"""
Example script showing how to use the /retrain API endpoint
to submit new training data and retrain the model.
"""

import requests
import json

# API base URL
BASE_URL = "http://localhost:8080"

def send_single_training_sample():
    """Send a single training sample for retraining"""
    
    # New training data sample
    new_sample = {
        "MedInc": 8.3252,
        "HouseAge": 41.0,
        "AveRooms": 6.984,
        "AveBedrms": 1.024,
        "Population": 322.0,
        "AveOccup": 2.555,
        "Latitude": 37.88,
        "Longitude": -122.23,
        "MedHouseValue": 4.526  # Target value
    }
    
    response = requests.post(f"{BASE_URL}/retrain", json=new_sample)
    
    if response.status_code == 200:
        print("✅ Single sample retraining triggered successfully!")
        print(json.dumps(response.json(), indent=2))
    else:
        print(f"❌ Error: {response.status_code}")
        print(response.json())

def send_multiple_training_samples():
    """Send multiple training samples for retraining"""
    
    # Multiple training data samples
    new_samples = [
        {
            "MedInc": 8.3252,
            "HouseAge": 41.0,
            "AveRooms": 6.984,
            "AveBedrms": 1.024,
            "Population": 322.0,
            "AveOccup": 2.555,
            "Latitude": 37.88,
            "Longitude": -122.23,
            "MedHouseValue": 4.526
        },
        {
            "MedInc": 7.2574,
            "HouseAge": 21.0,
            "AveRooms": 6.238,
            "AveBedrms": 0.971,
            "Population": 2401.0,
            "AveOccup": 2.109,
            "Latitude": 37.86,
            "Longitude": -122.22,
            "MedHouseValue": 3.585
        },
        {
            "MedInc": 5.6431,
            "HouseAge": 52.0,
            "AveRooms": 5.817,
            "AveBedrms": 1.073,
            "Population": 496.0,
            "AveOccup": 2.802,
            "Latitude": 37.85,
            "Longitude": -122.24,
            "MedHouseValue": 3.521
        }
    ]
    
    response = requests.post(f"{BASE_URL}/retrain", json=new_samples)
    
    if response.status_code == 200:
        print("✅ Multiple samples retraining triggered successfully!")
        print(json.dumps(response.json(), indent=2))
    else:
        print(f"❌ Error: {response.status_code}")
        print(response.json())

def check_retraining_status():
    """Check the status of recent retraining jobs"""
    
    response = requests.get(f"{BASE_URL}/retrain/status")
    
    if response.status_code == 200:
        print("📊 Retraining Status:")
        print(json.dumps(response.json(), indent=2))
    else:
        print(f"❌ Error: {response.status_code}")
        print(response.json())

def simulate_data_collection_and_retraining():
    """Simulate collecting new data from production and retraining"""
    
    print("🔄 Simulating new data collection and retraining...")
    
    # Simulate new data collected from production predictions
    # In real scenario, this could come from:
    # - User feedback on predictions
    # - New ground truth data
    # - Data drift detection
    
    production_data = [
        {
            "MedInc": 6.2534,
            "HouseAge": 28.0,
            "AveRooms": 5.847,
            "AveBedrms": 1.067,
            "Population": 1890.0,
            "AveOccup": 2.234,
            "Latitude": 37.92,
            "Longitude": -122.18,
            "MedHouseValue": 3.912  # Actual observed value
        },
        {
            "MedInc": 9.1234,
            "HouseAge": 15.0,
            "AveRooms": 7.234,
            "AveBedrms": 1.123,
            "Population": 456.0,
            "AveOccup": 2.678,
            "Latitude": 37.95,
            "Longitude": -122.15,
            "MedHouseValue": 5.234
        }
    ]
    
    # Send for retraining
    response = requests.post(f"{BASE_URL}/retrain", json=production_data)
    
    if response.status_code == 200:
        print("✅ Production data retraining triggered!")
        print(json.dumps(response.json(), indent=2))
        
        # Wait a moment and check status
        import time
        time.sleep(2)
        print("\n📊 Checking retraining status...")
        check_retraining_status()
    else:
        print(f"❌ Error: {response.status_code}")
        print(response.json())

if __name__ == "__main__":
    print("🚀 California Housing Model Retraining Examples\n")
    
    # Example 1: Send single sample
    print("1️⃣ Sending single training sample...")
    send_single_training_sample()
    print("\n" + "="*50 + "\n")
    
    # Example 2: Send multiple samples
    print("2️⃣ Sending multiple training samples...")
    send_multiple_training_samples()
    print("\n" + "="*50 + "\n")
    
    # Example 3: Check status
    print("3️⃣ Checking retraining status...")
    check_retraining_status()
    print("\n" + "="*50 + "\n")
    
    # Example 4: Simulate production scenario
    print("4️⃣ Simulating production data collection...")
    simulate_data_collection_and_retraining()
