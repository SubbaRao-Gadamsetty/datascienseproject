# Model Retraining API Documentation

## Overview

The `/retrain` endpoint allows you to submit new training data to retrain your California Housing prediction models. The improved implementation includes:

- ✅ Input validation using Pydantic models
- ✅ Proper JSON data storage with timestamps
- ✅ Background processing (non-blocking)
- ✅ Logging and status tracking
- ✅ Support for single or multiple samples
- ✅ Error handling and timeout management

## API Endpoints

### 1. `/retrain` (POST)
Submit new training data for model retraining.

**Request Body:**
- Single sample: JSON object with training features + target
- Multiple samples: JSON array of training objects

**Required Fields:**
```json
{
  "MedInc": float,      // Median income in block group
  "HouseAge": float,    // Median house age in block group
  "AveRooms": float,    // Average number of rooms per household
  "AveBedrms": float,   // Average number of bedrooms per household
  "Population": float,  // Block group population
  "AveOccup": float,    // Average number of household members
  "Latitude": float,    // Block group latitude
  "Longitude": float,   // Block group longitude
  "MedHouseValue": float // Target: Median house value (in hundreds of thousands)
}
```

**Response:**
```json
{
  "status": "Retraining triggered successfully!",
  "samples_received": 1,
  "training_file": "artifacts/retraining/new_training_data_2025-08-05T10-30-45.123456.json",
  "message": "Retraining is running in the background. Check logs for progress."
}
```

### 2. `/retrain/status` (GET)
Check the status of recent retraining jobs.

**Response:**
```json
{
  "recent_retraining_logs": [
    {
      "timestamp": "2025-08-05T10:30:45.123456",
      "sample_count": 3,
      "status": "COMPLETED",
      "stdout": "Training pipeline completed successfully...",
      "stderr": null
    }
  ]
}
```

## Usage Examples

### 1. Python Example

```python
import requests
import json

# Single sample
single_sample = {
    "MedInc": 8.3252,
    "HouseAge": 41.0,
    "AveRooms": 6.984,
    "AveBedrms": 1.024,
    "Population": 322.0,
    "AveOccup": 2.555,
    "Latitude": 37.88,
    "Longitude": -122.23,
    "MedHouseValue": 4.526
}

response = requests.post("http://localhost:8080/retrain", json=single_sample)
print(response.json())

# Multiple samples
multiple_samples = [single_sample, another_sample, ...]
response = requests.post("http://localhost:8080/retrain", json=multiple_samples)
```

### 2. cURL Example

```bash
# Single sample
curl -X POST http://localhost:8080/retrain \
  -H "Content-Type: application/json" \
  -d '{
    "MedInc": 8.3252,
    "HouseAge": 41.0,
    "AveRooms": 6.984,
    "AveBedrms": 1.024,
    "Population": 322.0,
    "AveOccup": 2.555,
    "Latitude": 37.88,
    "Longitude": -122.23,
    "MedHouseValue": 4.526
  }'

# Check status
curl -X GET http://localhost:8080/retrain/status
```

### 3. PowerShell Example

```powershell
$data = @{
    MedInc = 8.3252
    HouseAge = 41.0
    AveRooms = 6.984
    AveBedrms = 1.024
    Population = 322.0
    AveOccup = 2.555
    Latitude = 37.88
    Longitude = -122.23
    MedHouseValue = 4.526
}

$jsonData = $data | ConvertTo-Json
Invoke-RestMethod -Uri "http://localhost:8080/retrain" -Method POST -Body $jsonData -ContentType "application/json"
```

## Data Collection Strategies

### 1. **Feedback Loop Implementation**
```python
# After making predictions, collect actual values
def collect_feedback(prediction_id, actual_value):
    # Store prediction vs actual for retraining
    feedback_data = {
        "prediction_id": prediction_id,
        "actual_value": actual_value,
        "features": get_original_features(prediction_id),
        "timestamp": datetime.now().isoformat()
    }
    # Send to retraining endpoint
    requests.post("/retrain", json=feedback_data)
```

### 2. **Batch Processing from Database**
```python
# Periodically collect new labeled data
def collect_batch_data():
    # Query database for new ground truth data
    new_data = query_database("SELECT * FROM new_housing_data WHERE processed = 0")
    
    # Format for retraining
    training_samples = []
    for row in new_data:
        sample = {
            "MedInc": row.median_income,
            "HouseAge": row.house_age,
            # ... other features
            "MedHouseValue": row.actual_price
        }
        training_samples.append(sample)
    
    # Send batch for retraining
    if training_samples:
        response = requests.post("/retrain", json=training_samples)
        mark_as_processed(new_data)
```

### 3. **Real-time Data Streaming**
```python
# Stream new data as it becomes available
from kafka import KafkaConsumer

consumer = KafkaConsumer('housing_ground_truth')
batch = []

for message in consumer:
    data = json.loads(message.value)
    batch.append(data)
    
    # Process in batches of 100
    if len(batch) >= 100:
        requests.post("/retrain", json=batch)
        batch = []
```

## File Structure After Retraining

```
artifacts/
├── retraining/
│   ├── new_training_data_2025-08-05T10-30-45.json
│   ├── new_training_data_2025-08-05T11-15-23.json
│   └── ...
├── model_trainer/
│   ├── decisiontreemodel.joblib (updated)
│   └── linearregressionmodel.joblib (updated)
└── model_evaluation/
    ├── dt_model_metrics.json (updated)
    └── lr_model_metrics.json (updated)
```

## Database Logging

The system automatically logs retraining activities to SQLite database:

```sql
-- Retraining logs table
CREATE TABLE retraining_logs (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    timestamp TEXT,
    sample_count INTEGER,
    training_file TEXT,
    status TEXT,  -- 'STARTED', 'COMPLETED', 'FAILED'
    stdout TEXT,
    stderr TEXT
);
```

## Error Handling

### Validation Errors (422)
```json
{
  "error": "Invalid training data format",
  "details": [
    {
      "loc": ["MedHouseValue"],
      "msg": "field required",
      "type": "value_error.missing"
    }
  ]
}
```

### Server Errors (400)
```json
{
  "error": "Retraining process failed: [specific error message]"
}
```

## Best Practices

1. **Data Quality**: Ensure new training data follows the same distribution as original data
2. **Batch Size**: Submit data in reasonable batches (10-1000 samples)
3. **Monitoring**: Regularly check `/retrain/status` for job progress
4. **Validation**: Always validate model performance after retraining
5. **Backup**: Keep backups of previous models before retraining

## Integration with CI/CD

```yaml
# GitHub Actions example
- name: Retrain Model
  run: |
    python scripts/collect_new_data.py
    curl -X POST http://api/retrain -d @new_data.json
    python scripts/validate_model.py
```

## Security Considerations

- Implement authentication for retraining endpoints in production
- Validate data sources and prevent data poisoning
- Rate limit retraining requests
- Log all retraining activities for audit trails
