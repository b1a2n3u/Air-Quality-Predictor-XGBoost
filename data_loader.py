# data_loader.py
# This file loads and cleans the dataset

import pandas as pd
import numpy as np

def load_dataset():
    """
    Loads the aqi.csv dataset and
    cleans it for use in our project
    """
    try:
        # Loading the CSV file
        df = pd.read_csv("data/aqi.csv")
        
        print("✅ Dataset loaded successfully!")
        print(f"📊 Total records: {len(df)}")
        print(f"📋 Columns: {list(df.columns)}")
        
        return df
    
    except Exception as e:
        print(f"❌ Error loading dataset: {e}")
        return None


def clean_dataset(df):
    """
    Cleans the dataset by:
    1. Removing missing values
    2. Fixing column names
    3. Converting data types
    """
    
    # Step 1- Remove extra spaces from column names
    df.columns = df.columns.str.strip()
    
    print("✅ Column names fixed!")
    
    # Step 2 - Handle missing values
    # Count missing values before cleaning
    missing_before = df.isnull().sum().sum()
    print(f"⚠️ Missing values found: {missing_before}")
    
    # Fill missing AQI values with median
    if "aqi_value" in df.columns:
        df["aqi_value"] = df["aqi_value"].fillna(
            df["aqi_value"].median()
        )
    
    # Fill missing text columns with "Unknown"
    text_columns = [
        "state", "area", 
        "prominent_pollutants",
        "air_quality_status", "note"
    ]
    
    for col in text_columns:
        if col in df.columns:
            df[col] = df[col].fillna("Unknown")
    
    # Count missing values after cleaning
    missing_after = df.isnull().sum().sum()
    print(f"✅ Missing values after cleaning: {missing_after}")
    
    # Step 3 - Convert date column to datetime
    if "date" in df.columns:
        df["date"] = pd.to_datetime(
            df["date"], dayfirst=True,
            errors="coerce"
        )
        print("✅ Date column converted!")
    
    # Step 4 - Convert AQI to numeric
    if "aqi_value" in df.columns:
        df["aqi_value"] = pd.to_numeric(
            df["aqi_value"], 
            errors="coerce"
        )
        print("✅ AQI values converted to numbers!")
    
    return df


def get_dataset_summary(df):
    """
    Shows a quick summary of the dataset
    """
    print("\n" + "="*50)
    print("📊 DATASET SUMMARY")
    print("="*50)
    print(f"Total Records    : {len(df)}")
    print(f"Total Columns    : {len(df.columns)}")
    print(f"Date Range       : {df['date'].min()} to {df['date'].max()}")
    print(f"Total States     : {df['state'].nunique()}")
    print(f"Total Areas      : {df['area'].nunique()}")
    print(f"AQI Min Value    : {df['aqi_value'].min()}")
    print(f"AQI Max Value    : {df['aqi_value'].max()}")
    print(f"AQI Average      : {df['aqi_value'].mean():.2f}")
    print("="*50)
    
    print("\n📍 States in Dataset:")
    print(df['state'].unique())
    
    print("\n🏭 Prominent Pollutants:")
    print(df['prominent_pollutants'].unique())


def get_state_data(df, state_name):
    """
    Filters dataset for a specific state
    """
    # Filter by state name (case insensitive)
    state_df = df[
        df['state'].str.lower() == state_name.lower()
    ]
    
    if len(state_df) == 0:
        print(f"⚠️ No data found for {state_name}")
        return None
    
    print(f"✅ Found {len(state_df)} records for {state_name}")
    return state_df


def get_aqi_category_counts(df):
    """
    Counts how many records fall in each
    AQI category (Good, Moderate, etc.)
    """
    if "air_quality_status" in df.columns:
        counts = df['air_quality_status'].value_counts()
        return counts
    return None


# Testing - runs only when the gets directly run
if __name__ == "__main__":
    
    print("Loading dataset...")
    df = load_dataset()
    
    if df is not None:
        print("\nCleaning dataset...")
        df = clean_dataset(df)
        
        print("\nGetting summary...")
        get_dataset_summary(df)

def get_state_defaults(city_name):
    """
    Returns state, most common pollutant
    and average monitoring stations
    for a given city from the dataset
    """
    try:
        df = pd.read_csv("data/aqi.csv")
        df.columns = df.columns.str.strip()
        
        # Filter by city
        city_df = df[
            df['area'].str.lower() == city_name.lower()
        ]
        
        if len(city_df) == 0:
            return {
                "state"    : "Unknown",
                "pollutant": "PM2.5",
                "stations" : 5
            }
        
        # Get state of this city
        top_state = (
            city_df['state']
            .value_counts()
            .index[0]
        )
        
        # Most common pollutant
        top_pollutant = (
            city_df['prominent_pollutants']
            .value_counts()
            .index[0]
        )
        
        # Average monitoring stations
        avg_stations = int(
            city_df['number_of_monitoring_stations']
            .fillna(5)
            .mean()
        )
        avg_stations = max(1, min(20, avg_stations))
        
        return {
            "state"    : top_state,
            "pollutant": top_pollutant,
            "stations" : avg_stations
        }
        
    except:
        return {
            "state"    : "Unknown",
            "pollutant": "PM2.5",
            "stations" : 5
        }


def get_all_cities():
    """
    Returns all 291 cities
    from the dataset
    """
    try:
        df = pd.read_csv("data/aqi.csv")
        df.columns = df.columns.str.strip()
        cities = sorted(
            df['area'].dropna().unique().tolist()
        )
        return cities
    except:
        return ["Delhi", "Mumbai", "Chennai"]
    

def get_city_aqi_stats(city_name):
    """
    Returns real historical AQI stats
    for a given city from the dataset
    to use as model input features
    """
    try:
        df = pd.read_csv("data/aqi.csv")
        df.columns = df.columns.str.strip()
        
        # Filter by city
        city_df = df[
            df['area'].str.lower() == city_name.lower()
        ]
        
        if len(city_df) == 0:
            return {
                "aqi_lag1"        : 100,
                "aqi_rolling_mean": 100,
                "aqi_rolling_max" : 150
            }
        
        # Get real AQI values
        aqi_values = pd.to_numeric(
            city_df['aqi_value'], 
            errors='coerce'
        ).dropna()
        
        if len(aqi_values) == 0:
            return {
                "aqi_lag1"        : 100,
                "aqi_rolling_mean": 100,
                "aqi_rolling_max" : 150
            }
        
        avg_aqi = round(aqi_values.mean(), 2)
        max_aqi = round(aqi_values.max(), 2)

        
        #remove corrupted values above 500 
        aqi_values = aqi_values[aqi_values <= 500]
        avg_aqi = round(aqi_values.mean(),2)
        max_aqi = round(aqi_values.quantile(0.75),2)
        
        return {
            "aqi_lag1"        : avg_aqi,
            "aqi_rolling_mean": avg_aqi,
            "aqi_rolling_max" : max_aqi
        }
        
    except:
        return {
            "aqi_lag1"        : 100,
            "aqi_rolling_mean": 100,
            "aqi_rolling_max" : 150
        }    
    
