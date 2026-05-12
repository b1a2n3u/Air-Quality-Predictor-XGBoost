# model.py
# Complete ML Model

import pandas as pd
import numpy as np
from sklearn.tree import DecisionTreeRegressor
from sklearn.ensemble import RandomForestRegressor
from sklearn.linear_model import LinearRegression
from xgboost import XGBRegressor
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_absolute_error
from sklearn.metrics import r2_score
from sklearn.metrics import mean_squared_error
from sklearn.preprocessing import LabelEncoder
from datetime import datetime
import pickle
import warnings
warnings.filterwarnings("ignore")


# ============================================
# HELPER - GET SEASON FROM MONTH
# ============================================
def get_season(month):
    if month in [12, 1, 2]:
        return 1  # Winter
    elif month in [3, 4]:
        return 2  # Spring
    elif month in [5, 6]:
        return 3  # Summer
    elif month in [7, 8, 9]:
        return 4  # Monsoon
    else:
        return 5  # Autumn


# ============================================
# STEP 1 - LOAD AND PREPARE DATA
# ============================================
def prepare_data():
    print("📂 Loading dataset...")

    df = pd.read_csv("data/aqi.csv")
    df.columns = df.columns.str.strip()
    df = df.dropna(subset=["aqi_value"])
    df["aqi_value"] = pd.to_numeric(
        df["aqi_value"], errors="coerce"
    )
    df = df.dropna(subset=["aqi_value"])

    print(f"✅ Dataset ready!")
    print(f"📊 Total records: {len(df)}")
    return df


# ============================================
# STEP 2 - ENCODE TEXT FEATURES
# ============================================
def encode_features(df):
    print("\n🔄 Converting text to numbers...")

    le_state     = LabelEncoder()
    le_area      = LabelEncoder()
    le_pollutant = LabelEncoder()
    le_status    = LabelEncoder()

    df["state"] = df["state"].fillna("Unknown")
    df["area"]  = df["area"].fillna("Unknown")
    df["prominent_pollutants"] = df[
        "prominent_pollutants"
    ].fillna("Unknown")
    df["air_quality_status"] = df[
        "air_quality_status"
    ].fillna("Unknown")

    df["state_encoded"] = le_state.fit_transform(
        df["state"]
    )
    df["area_encoded"] = le_area.fit_transform(
        df["area"]
    )
    df["pollutant_encoded"] = le_pollutant.fit_transform(
        df["prominent_pollutants"]
    )
    df["status_encoded"] = le_status.fit_transform(
        df["air_quality_status"]
    )

    # Save encoders
    with open("data/encoders.pkl", "wb") as f:
        pickle.dump({
            "state"    : le_state,
            "area"     : le_area,
            "pollutant": le_pollutant,
            "status"   : le_status
        }, f)

    print("✅ Text converted successfully!")
    return df


# ============================================
# STEP 3 - EXTRACT DATE FEATURES
# ============================================
def extract_date_features(df):
    print("\n📅 Extracting date features...")

    df["date"] = pd.to_datetime(
        df["date"],
        dayfirst=True,
        errors="coerce"
    )

    df["month"]       = df["date"].dt.month.fillna(6)
    df["year"]        = df["date"].dt.year.fillna(2023)
    df["day_of_week"] = df["date"].dt.dayofweek.fillna(0)
    df["season"]      = df["month"].apply(get_season)
    # Sort by date for lag features
    df = df.sort_values("date")
    
    # Previous AQI value (lag feature)
    df["aqi_lag1"] = df.groupby(
        "area"
    )["aqi_value"].shift(1).fillna(
        df["aqi_value"].mean()
    )
    
    # Rolling average of last 7 records
    df["aqi_rolling_mean"] = df.groupby(
        "area"
    )["aqi_value"].transform(
        lambda x: x.rolling(7, min_periods=1).mean()
    )
    
    # Rolling max of last 7 records
    df["aqi_rolling_max"] = df.groupby(
        "area"
    )["aqi_value"].transform(
        lambda x: x.rolling(7, min_periods=1).max()
    )
    
    # Is winter? (1=yes, 0=no)
    df["is_winter"] = df["month"].apply(
        lambda x: 1 if x in [12, 1, 2] else 0
    )
    
    # Is monsoon? (1=yes, 0=no)
    df["is_monsoon"] = df["month"].apply(
        lambda x: 1 if x in [7, 8, 9] else 0
    )

    print("✅ Date features extracted!")
    print(f"   Months  : {sorted(df['month'].unique())}")
    print(f"   Seasons : {sorted(df['season'].unique())}")
    return df


# ============================================
# STEP 4 - TRAIN ALL 4 MODELS
# ============================================
def train_models():

    # Prepare all data
    df = prepare_data()
    df = encode_features(df)
    df = extract_date_features(df)

    # Fill missing stations
    df["number_of_monitoring_stations"] = df[
        "number_of_monitoring_stations"
    ].fillna(1)

    # All 8 features
    features = [
        "state_encoded",
        "area_encoded",
        "pollutant_encoded",
        "number_of_monitoring_stations",
        "month",
        "year",
        "day_of_week",
        "season",
        "aqi_lag1",
        "aqi_rolling_mean",
        "aqi_rolling_max",
        "is_winter",
        "is_monsoon",
        "status_encoded"    
    ]
    target = "aqi_value"

    X = df[features]
    y = df[target]

    # Split 70% train 30% test
    X_train, X_test, y_train, y_test = train_test_split(
        X, y,
        test_size    = 0.3,
        random_state = 42
    )

    print(f"\n📊 Training records : {len(X_train)}")
    print(f"📊 Testing records  : {len(X_test)}")

    # Define 4 models
    models = {
        "Linear Regression" : LinearRegression(),
        "Decision Tree"     : DecisionTreeRegressor(
                                random_state=42
                              ),
        "Random Forest"     : RandomForestRegressor(
                                n_estimators=100,
                                random_state=42
                              ),
        "XGBoost"           : XGBRegressor(
                                n_estimators=300,
                                learning_rate=0.05,
                                max_depth=8,
                                min_child_weight=3,
                                subsample=0.8,
                                colsample_bytree=0.8,
                                random_state=42,
                                verbosity=0
                              )
                           
    }

    results         = {}
    best_model_name = None
    best_r2         = -999

    print("\n" + "="*55)
    print("🤖 TRAINING ALL 4 ML MODELS")
    print("="*55)

    for name, model in models.items():
        print(f"\n⏳ Training {name}...")

        # Train
        model.fit(X_train, y_train)

        # Predict
        y_pred = model.predict(X_test)

        # Metrics
        mae  = mean_absolute_error(y_test, y_pred)
        rmse = np.sqrt(
                   mean_squared_error(y_test, y_pred)
               )
        r2   = r2_score(y_test, y_pred)

        results[name] = {
            "MAE"  : round(mae,  2),
            "RMSE" : round(rmse, 2),
            "R2"   : round(r2,   4),
            "model": model
        }

        print(f"✅ {name} Done!")
        print(f"   MAE  : {mae:.2f}  (lower is better)")
        print(f"   RMSE : {rmse:.2f} (lower is better)")
        print(f"   R2   : {r2:.4f}  (higher is better)")

        if r2 > best_r2:
            best_r2         = r2
            best_model_name = name

    # Print comparison
    print("\n" + "="*55)
    print("📊 FINAL MODEL COMPARISON")
    print("="*55)
    print(f"{'Model':<25}{'MAE':>8}{'RMSE':>8}{'R2':>8}")
    print("-"*55)

    for name, metrics in results.items():
        marker = " 🏆" if name == best_model_name else ""
        print(
            f"{name:<25}"
            f"{metrics['MAE']:>8}"
            f"{metrics['RMSE']:>8}"
            f"{metrics['R2']:>8}"
            f"{marker}"
        )

    print("="*55)
    print(f"\n🏆 Best Model : {best_model_name}")
    print(f"   R2 Score  : {best_r2:.4f}")

    # Save best model
    best_model_obj = results[best_model_name]["model"]
    with open("data/best_model.pkl", "wb") as f:
        pickle.dump(best_model_obj, f)

    print(f"\n✅ Best model saved!")
    print(f"📁 Location: data/best_model.pkl")

    return results, best_model_name


# ============================================
# STEP 5 - PREDICT AQI FOR NEW INPUT
# ============================================
def predict_aqi(state, area, pollutant, stations=1, aqi_lag1=100, aqi_rolling_mean=100, aqi_rolling_max=150):
    try:
        with open("data/best_model.pkl", "rb") as f:
            model = pickle.load(f)
        with open("data/encoders.pkl", "rb") as f:
            encoders = pickle.load(f)

        state_enc = encoders["state"].transform([state])[0] if state in encoders["state"].classes_ else 0
        area_enc = encoders["area"].transform([area])[0] if area in encoders["area"].classes_ else 0
        poll_enc = encoders["pollutant"].transform([pollutant])[0] if pollutant in encoders["pollutant"].classes_ else 0

        # Inputs for 2026 stability
        month, year, day_of_week, season = 4, 2024, 5, 2
        
        # Dynamic Status (0=Good, 1=Satisfactory, 2=Moderate)
        status_env = 0 if aqi_lag1 < 50 else (1 if aqi_lag1 < 100 else 2)

        input_features = [[
            state_enc, area_enc, poll_enc, stations,
            month, year, day_of_week, season,
            aqi_lag1, aqi_lag1, aqi_lag1 + 5,
            0, 0, status_env
        ]]

        prediction = model.predict(input_features)[0]
        return round(float(prediction), 2)
    except:
        return None


# ============================================
# RUN DIRECTLY
# ============================================
if __name__ == "__main__":

    # Train models
    results, best_model = train_models()

    # Test prediction
    print("\n" + "="*55)
    print("🧪 TESTING PREDICTION")
    print("="*55)

    test = predict_aqi(
        state     = "Delhi",
        area      = "Delhi",
        pollutant = "PM2.5",
        stations  = 5
    )

    print(f"Input         : Delhi, PM2.5, 5 stations")
    print(f"Predicted AQI : {test}")
