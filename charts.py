# visuals/charts.py
# All charts and graphs of the website

import plotly.graph_objects as go
import plotly.express as px
import pandas as pd


# ============================================
# CHART 1 - AQI GAUGE METER
# ============================================
def create_aqi_gauge(aqi_value, city_name):
    """
    Creates a beautiful speedometer
    style gauge showing AQI level
    """
    # Convert to number
    try:
        aqi_value = int(float(aqi_value))
    except:
        aqi_value = 0    
    # Determine color based on AQI
    if aqi_value <= 50:
        color = "green"
    elif aqi_value <= 100:
        color = "yellow"
    elif aqi_value <= 150:
        color = "orange"
    elif aqi_value <= 200:
        color = "red"
    elif aqi_value <= 300:
        color = "purple"
    else:
        color = "darkred"
    
    fig = go.Figure(go.Indicator(
        mode  = "gauge+number+delta",
        value = aqi_value,
        title = {
            "text" : f"AQI Level - {city_name}",
            "font" : {"size": 20}
        },
        gauge = {
            "axis" : {
                "range"    : [0, 500],
                "tickwidth": 1,
            },
            "bar"  : {"color": color},
            "steps": [
                {"range": [0,   50],  "color": "#00e400"},
                {"range": [51,  100], "color": "#ffff00"},
                {"range": [101, 150], "color": "#ff7e00"},
                {"range": [151, 200], "color": "#ff0000"},
                {"range": [201, 300], "color": "#8f3f97"},
                {"range": [301, 500], "color": "#7e0023"},
            ],
            "threshold": {
                "line" : {
                    "color": "black",
                    "width": 4
                },
                "value": aqi_value
            }
        }
    ))
    
    fig.update_layout(
        height          = 300,
        margin          = dict(t=50, b=0, l=0, r=0),
        paper_bgcolor   = "rgba(0,0,0,0)",
        font            = {"color": "white"}
    )
    
    return fig


# ============================================
# CHART 2 - POLLUTANT BAR CHART
# ============================================
def create_pollutant_chart(data):
    """
    Creates a bar chart showing
    all pollutant levels
    """
    
    # Prepare pollutant data
    pollutants = []
    values     = []
    colors     = []
    
    # Safe limits for each pollutant
    safe_limits = {
        "PM2.5" : 60,
        "PM10"  : 100,
        "NO2"   : 80,
        "SO2"   : 80,
        "CO"    : 4,
        "O3"    : 100
    }
    
    pollutant_map = {
        "pm25" : "PM2.5",
        "pm10" : "PM10",
        "no2"  : "NO2",
        "so2"  : "SO2",
        "co"   : "CO",
        "o3"   : "O3"
    }
    
    for key, label in pollutant_map.items():
        value = data.get(key, "N/A")
        if value != "N/A":
            pollutants.append(label)
            values.append(float(value))
            
            # Color based on safe limit
            limit = safe_limits.get(label, 100)
            if float(value) <= limit * 0.5:
                colors.append("#00e400")  # Green
            elif float(value) <= limit:
                colors.append("#ffff00")  # Yellow
            else:
                colors.append("#ff0000")  # Red
    
    fig = go.Figure(go.Bar(
        x             = pollutants,
        y             = values,
        marker_color  = colors,
        text          = values,
        textposition  = "outside"
    ))
    
    fig.update_layout(
        title           = "🧪 Pollutant Levels",
        xaxis_title     = "Pollutant",
        yaxis_title     = "Concentration (µg/m³)",
        height          = 350,
        paper_bgcolor   = "rgba(0,0,0,0)",
        plot_bgcolor    = "rgba(0,0,0,0)",
        font            = {"color": "white"},
        showlegend      = False
    )
    
    return fig


# ============================================
# CHART 3 - CITY COMPARISON CHART
# ============================================
def create_city_comparison(cities_data):
    """
    Creates a horizontal bar chart
    comparing AQI of multiple cities
    """
    
    if not cities_data:
        return None
    
    cities = []
    aqis   = []
    colors = []
    
    # Sort by AQI descending
    cities_data = sorted(
        cities_data,
        key    = lambda x: x.get("aqi", 0),
        reverse= True
    )
    
    for city in cities_data:
        cities.append(city.get("city", "Unknown"))
        aqi = city.get("aqi", 0)
        aqis.append(aqi)
        
        # Color based on AQI
        if aqi <= 50:
            colors.append("#00e400")
        elif aqi <= 100:
            colors.append("#ffff00")
        elif aqi <= 150:
            colors.append("#ff7e00")
        elif aqi <= 200:
            colors.append("#ff0000")
        elif aqi <= 300:
            colors.append("#8f3f97")
        else:
            colors.append("#7e0023")
    
    fig = go.Figure(go.Bar(
        x             = aqis,
        y             = cities,
        orientation   = "h",
        marker_color  = colors,
        text          = aqis,
        textposition  = "outside"
    ))
    
    fig.update_layout(
        title           = "🏙️ City AQI Comparison",
        xaxis_title     = "AQI Value",
        yaxis_title     = "City",
        height          = 500,
        paper_bgcolor   = "rgba(0,0,0,0)",
        plot_bgcolor    = "rgba(0,0,0,0)",
        font            = {"color": "white"},
        showlegend      = False
    )
    
    return fig


# ============================================
# CHART 4 - WEATHER PARAMETERS CHART
# ============================================
def create_weather_chart(data):
    """
    Creates a chart showing
    weather parameters
    """
    
    parameters = []
    values     = []
    
    weather_map = {
        "t"  : "Temperature (°C)",
        "h"  : "Humidity (%)",
        "w"  : "Wind Speed (m/s)",
        "p"  : "Pressure (hPa)"
    }
    
    for key, label in weather_map.items():
        value = data.get(key, "N/A")
        if value != "N/A":
            parameters.append(label)
            # Round to 2 decimal places 
            values.append(round(float(value), 2))
    
    fig = go.Figure(go.Bar(
        x            = parameters,
        y            = values,
        marker_color = "#4facfe",
        # Show rounded values on bars 
        text         = [str(v) for v in values],
        textposition = "outside"
    ))
    
    fig.update_layout(
        title         = "",
        height        = 350,
        paper_bgcolor = "rgba(0,0,0,0)",
        plot_bgcolor  = "rgba(0,0,0,0)",
        font          = {"color": "white"},
        showlegend    = False
    )
    
    return fig


# ============================================
# CHART 5 - ML MODEL COMPARISON CHART
# ============================================
def create_model_comparison_chart():
    """
    Creates a chart comparing
    all 4 ML model performances
    """
    
    models = [
        "Linear Regression",
        "Decision Tree",
        "Random Forest",
        "XGBoost"
    ]
    
    r2_scores = [0.8150, 0.9153, 0.9555, 0.9571]
    mae_scores = [20.93, 13.88, 10.69, 10.70]
    
    fig = go.Figure()
    
    # R2 Score bars
    fig.add_trace(go.Bar(
        name         = "R2 Score",
        x            = models,
        y            = r2_scores,
        marker_color = "#4facfe",
        text         = r2_scores,
        textposition = "outside"
    ))
    
    # MAE bars
    fig.add_trace(go.Bar(
        name         = "MAE (÷100)",
        x            = models,
        y            = [m/100 for m in mae_scores],
        marker_color = "#ff6b6b",
        text         = mae_scores,
        textposition = "outside"
    ))
    
    fig.update_layout(
        title         = "🤖 ML Model Comparison",
        barmode       = "group",
        height        = 400,
        paper_bgcolor = "rgba(0,0,0,0)",
        plot_bgcolor  = "rgba(0,0,0,0)",
        font          = {"color": "white"},
        legend        = {"font": {"color": "white"}}
    )
    
    return fig


# ============================================
# CHART 6 - AQI CATEGORY PIE CHART
# ============================================
def create_aqi_category_pie():
    """
    Creates a pie chart showing
    AQI category distribution
    from our dataset
    """
    
    labels = [
        "Good",
        "Moderate", 
        "Unhealthy for Sensitive",
        "Unhealthy",
        "Very Unhealthy",
        "Hazardous"
    ]
    
    values = [15, 25, 20, 20, 12, 8]
    
    colors = [
        "#00e400",
        "#ffff00",
        "#ff7e00",
        "#ff0000",
        "#8f3f97",
        "#7e0023"
    ]
    
    fig = go.Figure(go.Pie(
        labels           = labels,
        values           = values,
        marker_colors    = colors,
        hole             = 0.4,
        textinfo         = "label+percent"
    ))
    
    fig.update_layout(
        title         = "📊 AQI Category Distribution",
        height        = 400,
        paper_bgcolor = "rgba(0,0,0,0)",
        font          = {"color": "white"},
        legend        = {"font": {"color": "white"}}
    )
    
    return fig