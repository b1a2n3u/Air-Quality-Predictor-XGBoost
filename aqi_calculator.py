# aqi_calculator.py
# Calculates AQI from pollutant concentrations

# ============================================
# AQI BREAKPOINTS
# Based on Indian AQI Standards (CPCB)
# ============================================

# Format: (C_low, C_high, I_low, I_high)
AQI_BREAKPOINTS = {
    
    "pm25": [
        (0.0,  12.0,  0,   50),
        (12.1, 35.4,  51,  100),
        (35.5, 55.4,  101, 150),
        (55.5, 150.4, 151, 200),
        (150.5,250.4, 201, 300),
        (250.5,500.4, 301, 500)
    ],
    
    "pm10": [
        (0,   54,   0,   50),
        (55,  154,  51,  100),
        (155, 254,  101, 150),
        (255, 354,  151, 200),
        (355, 424,  201, 300),
        (425, 604,  301, 500)
    ],
    
    "no2": [
        (0,   53,   0,   50),
        (54,  100,  51,  100),
        (101, 360,  101, 150),
        (361, 649,  151, 200),
        (650, 1249, 201, 300),
        (1250,2049, 301, 500)
    ],
    
    "so2": [
        (0,   35,   0,   50),
        (36,  75,   51,  100),
        (76,  185,  101, 150),
        (186, 304,  151, 200),
        (305, 604,  201, 300),
        (605, 1004, 301, 500)
    ],
    
    "co": [
        (0.0,  4.4,  0,   50),
        (4.5,  9.4,  51,  100),
        (9.5,  12.4, 101, 150),
        (12.5, 15.4, 151, 200),
        (15.5, 30.4, 201, 300),
        (30.5, 50.4, 301, 500)
    ],
    
    "o3": [
        (0,   54,   0,   50),
        (55,  70,   51,  100),
        (71,  85,   101, 150),
        (86,  105,  151, 200),
        (106, 200,  201, 300),
        (201, 604,  301, 500)
    ]
}


# ============================================
# FUNCTION 1 - CALCULATE SUB INDEX
# ============================================
def calculate_sub_index(pollutant, concentration):
    """
    Calculates AQI sub-index for
    one pollutant using the formula:
    
    I = ((I_high - I_low) / 
         (C_high - C_low)) * 
        (C - C_low) + I_low
    """
    
    if pollutant not in AQI_BREAKPOINTS:
        return None
    
    if concentration is None:
        return None
    
    try:
        concentration = float(concentration)
    except:
        return None
    
    breakpoints = AQI_BREAKPOINTS[pollutant]
    
    for (c_low, c_high, i_low, i_high) in breakpoints:
        if c_low <= concentration <= c_high:
            
            # AQI Formula from base paper
            sub_index = (
                (i_high - i_low) /
                (c_high - c_low)
            ) * (concentration - c_low) + i_low
            
            return round(sub_index, 2)
    
    # If concentration exceeds all ranges
    return 500


# ============================================
# FUNCTION 2 - CALCULATE OVERALL AQI
# ============================================
def calculate_aqi(pollutant_data):
    """
    Calculates overall AQI from
    multiple pollutant concentrations
    
    Overall AQI = Maximum of all sub-indices
    
    Input example:
    {
        "pm25": 45.0,
        "pm10": 80.0,
        "no2" : 30.0,
        "so2" : 15.0,
        "co"  : 2.5,
        "o3"  : 40.0
    }
    """
    
    sub_indices  = {}
    valid_count  = 0
    
    for pollutant, concentration in pollutant_data.items():
        
        if concentration == "N/A":
            continue
        if concentration is None:
            continue
            
        sub_index = calculate_sub_index(
            pollutant,
            concentration
        )
        
        if sub_index is not None:
            sub_indices[pollutant] = sub_index
            valid_count += 1
    
    if valid_count == 0:
        return None, {}
    
    # Overall AQI = highest sub-index
    overall_aqi = max(sub_indices.values())
    
    return round(overall_aqi, 2), sub_indices


# ============================================
# FUNCTION 3 - GET AQI CATEGORY
# ============================================
def get_aqi_category(aqi):
    """
    Returns AQI category name
    based on AQI value
    """
    
    if aqi <= 50:
        return "Good"
    elif aqi <= 100:
        return "Moderate"
    elif aqi <= 150:
        return "Unhealthy for Sensitive Groups"
    elif aqi <= 200:
        return "Unhealthy"
    elif aqi <= 300:
        return "Very Unhealthy"
    else:
        return "Hazardous"


# ============================================
# FUNCTION 4 - GET DOMINANT POLLUTANT
# ============================================
def get_dominant_pollutant(sub_indices):
    """
    Returns the pollutant with
    highest sub-index value
    (the main cause of pollution)
    """
    
    if not sub_indices:
        return "Unknown"
    
    dominant = max(
        sub_indices,
        key=sub_indices.get
    )
    
    pollutant_names = {
        "pm25": "PM2.5",
        "pm10": "PM10",
        "no2" : "NO2",
        "so2" : "SO2",
        "co"  : "CO",
        "o3"  : "O3"
    }
    
    return pollutant_names.get(dominant, dominant)


# ============================================
# FUNCTION 5 - FULL AQI REPORT
# ============================================
def get_full_aqi_report(pollutant_data):
    """
    Generates a complete AQI report
    with all details
    """
    
    # Calculate AQI
    overall_aqi, sub_indices = calculate_aqi(
        pollutant_data
    )
    
    if overall_aqi is None:
        return {
            "status" : "error",
            "message": "No valid pollutant data!"
        }
    
    # Get category
    category = get_aqi_category(overall_aqi)
    
    # Get dominant pollutant
    dominant = get_dominant_pollutant(sub_indices)
    
    return {
        "status"          : "success",
        "overall_aqi"     : overall_aqi,
        "category"        : category,
        "dominant_pollutant": dominant,
        "sub_indices"     : sub_indices
    }


# ============================================
# TEST WHEN RUN DIRECTLY
# ============================================
if __name__ == "__main__":
    
    print("="*50)
    print("🧪 TESTING AQI CALCULATOR")
    print("="*50)
    
    # Test data
    test_data = {
        "pm25": 55.0,
        "pm10": 120.0,
        "no2" : 45.0,
        "so2" : 20.0,
        "co"  : 3.5,
        "o3"  : 65.0
    }
    
    print("\nInput Pollutants:")
    for p, v in test_data.items():
        print(f"  {p.upper():6} : {v}")
    
    # Get full report
    report = get_full_aqi_report(test_data)
    
    print("\n📊 AQI Report:")
    print(f"  Overall AQI        : {report['overall_aqi']}")
    print(f"  Category           : {report['category']}")
    print(f"  Dominant Pollutant : {report['dominant_pollutant']}")
    print("\n  Sub Indices:")
    for p, i in report["sub_indices"].items():
        print(f"    {p.upper():6} : {i}")