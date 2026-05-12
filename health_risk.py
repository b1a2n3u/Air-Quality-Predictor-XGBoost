# health_risk.py
# Calculates health risk based on AQI value

def get_health_risk(aqi):
    """
    Takes AQI value and returns
    complete health risk information
    """
    # Convert to number 
    try:
        aqi = int(float(aqi))
    except: 
        aqi=0
            
    if aqi <= 50:
        return {
            "level"    : "Good",
            "color"    : "green",
            "emoji"    : "😊",
            "message"  : "Air quality is satisfactory",
            "affected" : "No one affected",
            "advice"   : "Perfect day to go outside! Enjoy outdoor activities freely.",
            "aqi_range": "0-50"
        }
    
    elif aqi <= 100:
        return {
            "level"    : "Moderate",
            "color"    : "yellow",
            "emoji"    : "😐",
            "message"  : "Air quality is acceptable",
            "affected" : "Individuals with extreme sensitivity",
            "advice"   : "Sensitive people should consider reducing outdoor activity.",
            "aqi_range": "51-100"
        }
    
    elif aqi <= 150:
        return {
            "level"    : "Unhealthy for Sensitive Groups",
            "color"    : "orange",
            "emoji"    : "😷",
            "message"  : "Sensitive groups may experience effects",
            "affected" : "Vulnerable groups and respiratory patients",
            "advice"   : "Children and elderly should limit outdoor activities. Wear a mask.",
            "aqi_range": "101-150"
        }
    
    elif aqi <= 200:
        return {
            "level"    : "Unhealthy",
            "color"    : "red",
            "emoji"    : "🤧",
            "message"  : "Everyone may experience health effects",
            "affected" : "General public and all sensitive groups",
            "advice"   : "Reduce outdoor activity. Wear N95 mask if going out.",
            "aqi_range": "151-200"
        }
    
    elif aqi <= 300:
        return {
            "level"    : "Very Unhealthy",
            "color"    : "purple",
            "emoji"    : "😰",
            "message"  : "Health alert - serious effects possible",
            "affected" : "Everyone seriously affected",
            "advice"   : "Avoid all outdoor activities. Keep windows closed. Use air purifier.",
            "aqi_range": "201-300"
        }
    
    else:
        return {
            "level"    : "Hazardous",
            "color"    : "darkred",
            "emoji"    : "☠️",
            "message"  : "EMERGENCY - Health warning!",
            "affected" : "Entire population at risk",
            "advice"   : "STAY INDOORS! Avoid ALL outdoor exposure completely.",
            "aqi_range": "301-500"
        }


def get_pollutant_advice(pollutant, value):
    """
    Gives specific advice
    for each pollutant level
    """
    
    if value == "N/A":
        return "Data not available"
    
    try:
        val = float(value)
    except:
        return "Invalid data"
    
    if pollutant == "pm25":
        if val <= 12:
            return "PM2.5 is at safe levels ✅"
        elif val <= 35:
            return "PM2.5 is moderate ⚠️"
        else:
            return "PM2.5 is dangerous! Wear mask ❌"
    
    elif pollutant == "pm10":
        if val <= 54:
            return "PM10 is at safe levels ✅"
        elif val <= 154:
            return "PM10 is moderate ⚠️"
        else:
            return "PM10 is dangerous! ❌"
    
    elif pollutant == "no2":
        if val <= 40:
            return "NO2 is at safe levels ✅"
        elif val <= 80:
            return "NO2 is moderate ⚠️"
        else:
            return "NO2 is high! Avoid traffic ❌"
    
    elif pollutant == "so2":
        if val <= 40:
            return "SO2 is at safe levels ✅"
        elif val <= 80:
            return "SO2 is moderate ⚠️"
        else:
            return "SO2 is dangerous! ❌"
    
    elif pollutant == "co":
        if val <= 4:
            return "CO is at safe levels ✅"
        elif val <= 10:
            return "CO is moderate ⚠️"
        else:
            return "CO is dangerous! ❌"
    
    elif pollutant == "o3":
        if val <= 60:
            return "O3 is at safe levels ✅"
        elif val <= 100:
            return "O3 is moderate ⚠️"
        else:
            return "O3 is dangerous! ❌"
    
    return "Monitor levels regularly"


# Test when run directly
if __name__ == "__main__":
    print("Testing AQI = 175")
    result = get_health_risk(175)
    print(result)


def get_personalized_advice(aqi, age_group, health_condition, activity_level):
    """
    Final optimized logic: Context-aware, disease-specific, and error-shielded.
    """
    try:
        current_aqi = int(float(aqi))
    except (ValueError, TypeError):
        current_aqi = 0

    # 1. Determine Risk Level
    if current_aqi <= 50:
        base_risk = "low"
    elif current_aqi <= 100:
        base_risk = "moderate"
    elif current_aqi <= 150:
        base_risk = "high"
    elif current_aqi <= 200:
        base_risk = "very_high"
    else:
        base_risk = "hazardous"

    advice = []
    warning = []
    
    # Identify user vulnerability
    is_elderly = age_group == "Elderly (60+)"
    is_child = age_group == "Child (0-12)"
    is_sensitive = (health_condition != "None (Healthy)") or is_elderly or is_child

    # Medical Groups
    respiratory = ["Asthma", "COPD(Chronic Obstructive Pulmonary Disease)", "Bronchitis", "Pneumonia", "Allergic Rhinitis", "Acute Sinusitis"]
    cardiac = ["Heart Disease", "Ischemic Heart Disease", "Hypertension", "Stroke History", "Cardiac Arrhythmia"]
    severe_risk = ["Lung Cancer", "Cognitive Decline", "Diabetes"]

    # ── LOGIC STEP 1: INDOOR USERS ──
    if activity_level == "Indoor":
        if base_risk == "low":
            emoji = "😊"
            advice.append("🏠 Your indoor environment is perfectly safe.")
        elif base_risk == "moderate":
            emoji = "😐"
            advice.append("🏠 You are safe indoors. No special precautions needed.")
        else:
            emoji = "😷"
            advice.append("🏠 Stay indoors with windows closed.")
            warning.append("⚠️ ALERT: Outdoor air quality is currently UNSAFE. Avoid leaving the building.")
            if current_aqi > 150:
                advice.append("💨 Use an air purifier to maintain indoor air quality.")
            
            # Contextual Medical Warnings
            if health_condition in respiratory:
                warning.append(f"🚨 Respiratory Alert ({health_condition}): Keep therapy/inhaler nearby.")
            elif health_condition in cardiac:
                warning.append(f"🚨 Cardiac Alert ({health_condition}): Avoid physical stress while indoors.")
            elif health_condition == "Pregnant":
                warning.append("🤰 Maternal Health: Maintain filtered indoor air for safety.")
            elif health_condition in severe_risk:
                warning.append(f"🚨 Clinical Group ({health_condition}): Minimize all exposure to outdoor air leaks.")

    # ── LOGIC STEP 2: OUTDOOR USERS ──
    else:
        # HAZARDOUS SHIELD: Check this first!
        if base_risk in ["hazardous", "very_high"]:
            emoji = "☠️"
            warning.append(f"🚨 EMERGENCY: Stop all {activity_level} immediately!")
            warning.append("🚫 Dangerous air quality. Move to a filtered indoor environment now.")
            if health_condition != "None (Healthy)":
                warning.append(f"🚨 CRITICAL for {health_condition}: Seek medical advice if breathing is difficult.")
        
        elif base_risk == "high":
            emoji = "😷"
            warning.append("😷 Wear a high-quality N95 mask outdoors.")
            if is_sensitive:
                warning.append(f"🚫 High risk for {health_condition}: Move indoors now.")
            else:
                warning.append(f"⚠️ Limit {activity_level} duration and intensity.")

        elif base_risk == "moderate":
            emoji = "😐"
            if is_sensitive:
                warning.append(f"⚠️ Sensitive Group Alert: Limit prolonged {activity_level}.")
            else:
                advice.append(f"✅ {activity_level} is acceptable for healthy adults.")

        else: # low risk
            emoji = "😊"
            advice.append(f"🌳 Perfect conditions for {activity_level}! Enjoy the fresh air.")

    return {
        "emoji": emoji,
        "advice": advice,
        "warning": warning,
        "is_sensitive": is_sensitive
    } 

    # ── STEP 1: INDOOR LOGIC (No 'outdoor') ──
    if activity_level == "Indoor":
        if aqi <= 100:
            emoji = "😊"
            advice.append("🏠 Your indoor environment is safe and healthy.")
        elif aqi <= 200:
            emoji = "😐"
            advice.append("🏠 You are safe indoors. Keep windows closed to maintain air quality.")
            if health_condition == "Asthma":
                warning.append("🚨 Keep your inhaler nearby as a precaution.")
        else:
            emoji = "😷"
            warning.append("🚨 High outdoor pollution! Stay indoors and use an air purifier.")
            if is_sensitive:
                warning.append("🚨 Monitor your breathing closely.")

    # ── STEP 2: OUTDOOR LOGIC ──
    else:
        if aqi <= 50:
            emoji = "😊"
            advice.append(f"🌳 Perfect conditions for {activity_level}! Enjoy the fresh air.")
        elif aqi <= 100:
            emoji = "😐"
            if is_sensitive:
                warning.append(f"⚠️ As a sensitive individual, limit prolonged {activity_level}.")
            else:
                advice.append(f"✅ Conditions are acceptable for {activity_level}.")
        elif aqi <= 200:
            emoji = "😷"
            warning.append(f"🚫 {activity_level} is not recommended. Move indoors.")
            warning.append("😷 Wear a mask if you must be outside.")
        else:
            emoji = "☠️"
            warning.append(f"🚨 EMERGENCY: Stop all {activity_level} immediately and seek shelter.")

    return {
        "emoji": emoji,
        "advice": advice,
        "warning": warning,
        "is_sensitive": is_sensitive
    }