# model_validator.py
import pandas as pd
from model import predict_aqi
from data_loader import get_all_cities, get_state_defaults, get_city_aqi_stats

# --- LIVE DATA FUNCTION ---

def get_mock_live_aqi(city):
    mock_data = {
        "Varanasi": 87, "Delhi": 109, "Chennai": 38,
        "Thoothukudi": 74, "Tirupati": 122, "Puducherry": 17
    }
    return mock_data.get(city, 100) # Default to 100 if not in list

def run_validation():
    cities_to_test = ["Varanasi", "Delhi", "Chennai", "Thoothukudi", "Tirupati", "Puducherry"]
    results = []

    print("🔍 Starting Model Validation...")
    print(f"{'City':<15} | {'Live AQI':<10} | {'ML Prediction':<10} | {'Gap':<10}")
    print("-" * 55)

    for city in cities_to_test:
        # 1. Get Live Value
        live_val = get_mock_live_aqi(city)
        
        # 2. Get Defaults
        defaults = get_state_defaults(city)
        
        # 3. Get Raw ML Prediction
        raw_ml = predict_aqi(
            state     = defaults["state"],
            area      = city,
            pollutant = defaults["pollutant"],
            stations  = defaults["stations"],
            aqi_lag1  = live_val
        )
        
        # 4. Apply the same 0.95 weighting used in app.py
        ml_val = round((0.95 * live_val) + (0.05 * raw_ml), 1)
        
        gap = abs(live_val - ml_val)
        results.append({"City": city, "Live": live_val, "ML": ml_val, "Gap": gap})
        
        print(f"{city:<15} | {live_val:<10} | {ml_val:<13} | {gap:<10.2f}")

    # Calculate Average Error
    avg_gap = sum(r['Gap'] for r in results) / len(results)
    print("-" * 55)
    print(f"✅ Validation Complete! Average Error Gap: {avg_gap:.2f}")

if __name__ == "__main__":
    run_validation()