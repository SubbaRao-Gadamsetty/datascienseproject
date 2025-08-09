@echo off
echo 🚀 California Housing Model Retraining Demo
echo ==================================================

set BASE_URL=http://localhost:8080

echo.
echo 1️⃣ Sending single training sample...
curl -X POST %BASE_URL%/retrain ^
  -H "Content-Type: application/json" ^
  -d "{\"MedInc\": 8.3252, \"HouseAge\": 41.0, \"AveRooms\": 6.984, \"AveBedrms\": 1.024, \"Population\": 322.0, \"AveOccup\": 2.555, \"Latitude\": 37.88, \"Longitude\": -122.23, \"MedHouseValue\": 4.526}"

echo.
echo.
echo 2️⃣ Checking retraining status...
curl -X GET %BASE_URL%/retrain/status

echo.
echo.
echo 3️⃣ Sending multiple training samples...
curl -X POST %BASE_URL%/retrain ^
  -H "Content-Type: application/json" ^
  -d "[{\"MedInc\": 7.2574, \"HouseAge\": 21.0, \"AveRooms\": 6.238, \"AveBedrms\": 0.971, \"Population\": 2401.0, \"AveOccup\": 2.109, \"Latitude\": 37.86, \"Longitude\": -122.22, \"MedHouseValue\": 3.585}, {\"MedInc\": 5.6431, \"HouseAge\": 52.0, \"AveRooms\": 5.817, \"AveBedrms\": 1.073, \"Population\": 496.0, \"AveOccup\": 2.802, \"Latitude\": 37.85, \"Longitude\": -122.24, \"MedHouseValue\": 3.521}]"

echo.
echo.
echo 🎉 Demo completed! Check the status again...
curl -X GET %BASE_URL%/retrain/status

pause
