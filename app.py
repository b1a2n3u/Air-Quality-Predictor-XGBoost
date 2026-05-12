# app.py
# Complete Website - Air Pollution Analytics Platform

import streamlit as st
import sys
import os

# Add visuals folder to path
sys.path.append(
    os.path.join(os.path.dirname(__file__), "visuals")
)

from realtime_data import get_air_quality
from realtime_data import get_multiple_cities
from health_risk import get_health_risk
from health_risk import get_pollutant_advice
from health_risk import get_personalized_advice
from model import predict_aqi
from data_loader import get_state_defaults, get_all_cities,get_city_aqi_stats
from charts import (
    create_aqi_gauge,
    create_pollutant_chart,
    create_city_comparison,
    create_weather_chart,
    create_model_comparison_chart,
    create_aqi_category_pie
)
# GLOBAL DATA
import pandas as pd

# Loading dataset
try:
    df = pd.read_csv("city_day.csv") 
except:
    df = pd.DataFrame() 

# list of cities 
cities_list = [
    'Agartala', 'Agra', 'Ahmedabad', 'Aizawl', 'Ajmer', 'Alwar', 'Ambala', 'Amritsar', 
    'Anantapur', 'Ankleshwar', 'Arrah', 'Asansol', 'Aurangabad', 'Baddi', 'Bagalkot', 
    'Baghpat', 'Bahadurgarh', 'Bareilly', 'Bathinda', 'Begusarai', 'Bengaluru', 
    'Bettiah', 'Bhagalpur', 'Bhilai', 'Bhiwadi', 'Bhiwandi', 'Bhopal', 'Bihar Sharif', 
    'Bilaspur', 'Brajrajnagar', 'Bulandshahr', 'Buxar', 'Chandigarh', 'Chandrapur', 
    'Charkhi Dadri', 'Chennai', 'Chhapra', 'Chikkamagaluru', 'Churu', 'Coimbatore', 
    'Damoh', 'Darbhanga', 'Delhi', 'Dewas', 'Dharuhera', 'Dindigul', 'Durgapur', 
    'Firozabad', 'Gadag', 'Gangtok', 'Gaya', 'Ghaziabad', 'Gorakhpur', 'Greater Noida', 
    'Guwahati', 'Gwalior', 'Hajipur', 'Haldia', 'Hapur', 'Haveri', 'Howrah', 'Hyderabad',
    'Jabalpur', 'Jaipur', 'Jalandhar', 'Jhansi', 'Jind', 'Jodhpur', 'Kalaburagi', 
    'Kalyan', 'Kannur', 'Kanpur', 'Karnal', 'Katihar', 'Khanna', 'Khurja', 'Kishanganj', 
    'Kohima', 'Kolar', 'Kolkata', 'Kollam', 'Kota', 'Lucknow', 'Madikeri', 'Mandideep', 
    'Mangalore', 'Meerut', 'Moradabad', 'Motihari', 'Mumbai', 'Munger', 'Muzaffarnagar', 
    'Muzaffarpur', 'NOIDA', 'Nagpur', 'Naharlagun', 'Narnaul', 'Nashik', 'Navi Mumbai', 
    'Ooty', 'Pali', 'Panchkula', 'Pathardih', 'Patiala', 'Patna', 'Pithampur', 
    'Puducherry', 'Pune', 'Raichur', 'Raipur', 'Rajamahendravaram', 'Rajgir', 
    'Ramanathapuram', 'Ratlam', 'Rohtak', 'Rupnagar', 'Sagar', 'Saharsa', 'Satna', 
    'Shillong', 'Shivamogga', 'Siliguri', 'Siwan', 'Sonipat', 'Srinagar', 'Talcher', 
    'Thane', 'Thiruvananthapuram', 'Thoothukudi', 'Thrissur', 'Tirupati', 'Tiruppur', 
    'Udaipur', 'Varanasi', 'Vijayapura', 'Virar', 'Vrindavan', 'Yadgir', 'Yamunanagar'
]
cities_list.sort()

def display_medical_report(status):
    # Medical database
    risk_db = {
        "Good": {
            "diseases": ["No clinical risks identified."],
            "impact": "Ideal for outdoor exercise and respiratory recovery."
        },
        "Moderate": {
            "diseases": ["Mild Rhinitis", "Eye Irritation", "Seasonal Allergies"],
            "impact": "Sensitive individuals may experience increased mucus production and slight wheezing."
        },
        "Poor": {
            "diseases": ["Chronic Bronchitis", "Acute Sinusitis", "Exacerbation of Asthma"],
            "impact": "Prolonged exposure leads to narrowed airways and decreased lung function."
        },
        "Unhealthy": {
            "diseases": ["COPD (Chronic Obstructive Pulmonary Disease)", "Pneumonia", "Cardiac Arrhythmia", "Hypertension"],
            "impact": "Pollutants enter the bloodstream, causing systemic inflammation and stress on the heart."
        },
        "Hazardous": {
            "diseases": ["Lung Cancer", "Ischemic Heart Disease", "Stroke", "Emphysema", "Neurodegenerative risks"],
            "impact": "Severe risk of permanent DNA damage in lung cells and high probability of cardiovascular collapse."
        }
    }

    # Get data based on status
    data = risk_db.get(status, risk_db["Good"])
    
    c1, c2 = st.columns(2)
    with c1:
        st.error("**Potential Medical Conditions**")
        for disease in data["diseases"]:
            st.markdown(f"• {disease}")
    
    with c2:
        st.warning("**Pathological Impact**")
        st.write(data["impact"])

# ============================================
# PAGE CONFIGURATION
# ============================================
st.set_page_config(
    page_title = "Air Pollution Analytics Platform",
    page_icon  = "🌍",
    layout     = "wide",
    initial_sidebar_state = "expanded"
)

# ============================================
# CUSTOM CSS STYLING
# ============================================
st.markdown("""
    <style>
    .main {
        background: linear-gradient(
            135deg, #0f0c29, #302b63, #24243e
        );
    }
    .big-title {
        font-size: 42px;
        font-weight: bold;
        text-align: center;
        background: linear-gradient(
            90deg, #4facfe, #00f2fe
        );
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        padding: 20px;
    }
    .subtitle {
        text-align: center;
        color: #a0aec0;
        font-size: 18px;
        margin-bottom: 30px;
    }
    .metric-card {
        background: rgba(255,255,255,0.05);
        border-radius: 15px;
        padding: 20px;
        border: 1px solid rgba(255,255,255,0.1);
        text-align: center;
    }
    .section-title {
        font-size: 24px;
        font-weight: bold;
        color: #4facfe;
        margin: 20px 0px;
    }
    .who-card {
        background: rgba(79,172,254,0.1);
        border-radius: 10px;
        padding: 15px;
        border: 1px solid #4facfe;
        margin: 10px 0px;
    }
    </style>
""", unsafe_allow_html=True)


# ============================================
# SIDEBAR NAVIGATION
# ============================================
st.sidebar.image(
    "https://img.icons8.com/fluency/96/000000/air-quality.png",
    width=80
)
st.sidebar.title("🌍 Navigation")
st.sidebar.markdown("---")

page = st.sidebar.radio(
    "Go to:",
    [
        "🏠 Home",
        "📊 Live Dashboard",
        "📈 ML Prediction",
        "🏥 Health Risk",
        "🌍 City Comparison",
        "📖 WHO Guidelines",
        "💬 AI Assistant"

    ]
)

st.sidebar.markdown("---")
st.sidebar.info(
    "Data Sources:\n"
    "- WAQI API (Live)\n"
    "- India AQI Dataset 2022-2025\n"
    "- WHO Guidelines 2021"
)


# ============================================
# PAGE 1 - HOME
# ============================================
if page == "🏠 Home":
    
    st.markdown(
        '<p class="big-title">'
        '🌍 Air Pollution Analytics & '
        'Health Risk Intelligence Platform'
        '</p>',
        unsafe_allow_html=True
    )
    
    st.markdown(
        '<p class="subtitle">'
        'Real-time air quality monitoring, '
        'ML-powered predictions & '
        'personalized health risk assessment'
        '</p>',
        unsafe_allow_html=True
    )
    
    st.markdown("---")
    
    # Feature cards
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.markdown("""
        <div class="metric-card">
            <h2>🏙️</h2>
            <h3>291 Cities</h3>
            <p>Major Cities in India</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class="metric-card">
            <h2>📊</h2>
            <h3>235,785</h3>
            <p>Records in dataset</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown("""
        <div class="metric-card">
            <h2>🤖</h2>
            <h3>95.71% Accurate</h3>
            <p>XGBoost ML Model</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col4:
        st.markdown("""
        <div class="metric-card">
            <h2>⚡</h2>
            <h3>Real-time</h3>
            <p>Live API data</p>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    # About section - Two columns 
    col_left, col_right = st.columns(2)

    with col_left:
        st.markdown(
            '<p class="section-title">'
            '📌 About This Platform'
            '</p>',
            unsafe_allow_html=True
        )
        st.write("""
        This platform is an air quality
        prediction system built as an improvement
        over the base IEEE research paper.

        **Key Improvements over Base Paper:**
        - ✅ Extended from 1 city to 291 cities
        - ✅ Added real-time API data
        - ✅ Added XGBoost model
        - ✅ Added weather parameters
        - ✅ Added health risk intelligence
        - ✅ Added interactive dashboard
        - ✅ Used 2022-2025 fresh dataset
        """)

    with col_right:
        st.markdown(
            '<p class="section-title">'
            '🤖 ML Models Used'
            '</p>',
            unsafe_allow_html=True
        )
        st.markdown("""
        📊 Linear Regression
        \n🌿 Decision Tree
        \n🌲 Random Forest
        \n⭐ XGBoost
        """)

    st.markdown("---")

    # Chart 
    st.markdown(
        '<p class="section-title" '
        'style="text-align:center;">'
        '📈 ML Model Comparison'
        '</p>',
        unsafe_allow_html=True
    )

    # Center the chart using columns 
    _, center_col, _ = st.columns([0.5, 3, 0.5])
    with center_col:
        fig = create_model_comparison_chart()
        st.plotly_chart(
            fig,
            use_container_width=True,key="home_model_comparison"
        )
        
    
    st.markdown("---")
    
    # AQI Scale
    st.markdown(
        '<p class="section-title">'
        '📊 AQI Scale Reference'
        '</p>',
        unsafe_allow_html=True
    )
    
    scale_cols = st.columns(6)
    
    scales = [
        ("0-50",   "Good",        "🟢", "green"),
        ("51-100", "Moderate",    "🟡", "yellow"),
        ("101-150","Sensitive",   "🟠", "orange"),
        ("151-200","Unhealthy",   "🔴", "red"),
        ("201-300","Very Bad",    "🟣", "purple"),
        ("301-500","Hazardous",   "⚫", "darkred"),
    ]
    
    for i, (range_, label, emoji, _) in enumerate(scales):
        with scale_cols[i]:
            st.markdown(f"""
            <div class="metric-card">
                <h3>{emoji}</h3>
                <b>{range_}</b><br>
                <small>{label}</small>
            </div>
            """, unsafe_allow_html=True)

# ============================================
# PAGE 2 - LIVE DASHBOARD
# ============================================
elif page == "📊 Live Dashboard":

    st.markdown(
        '<p class="section-title">'
        '📊 Live Air Quality Dashboard'
        '</p>',
        unsafe_allow_html=True
    )

    

    # Initialize session state
    if "live_city" not in st.session_state:
        st.session_state["live_city"] = None
    if "live_data" not in st.session_state:
        st.session_state["live_data"] = None

    # Get current index
    if st.session_state["live_city"] in cities_list:
        current_index = cities_list.index(
            st.session_state["live_city"]
        )
    else:
        current_index = None

    # City dropdown
    city = st.selectbox(
        "🏙️ Select City:",
        cities_list,
        index=current_index,
        placeholder="Choose a city...",
    )

    # Save immediately on selection
    if city is not None:
        st.session_state["live_city"] = city

    # Stop if no city selected
    if city is None:
        st.info(
            "👆 Please choose a city "
            "from the dropdown above!"
        )
        st.stop()

    # Get Live Data button
    if st.button("🔍 Get Live Data", type="primary"):
        with st.spinner(
            f"Fetching live data for {city}..."
        ):
            st.session_state["live_data"] = (
                get_air_quality(city)
            )

    # Show data if available
    if st.session_state["live_data"] is not None:
        data = st.session_state["live_data"]

        if data["status"] == "success":

            risk = get_health_risk(data["aqi"])        

            st.success(
                f"✅ Live data fetched for "
                f"{data['city']}!"
            )
            st.markdown("---")

            # Top metrics
            col1, col2, col3, col4 = st.columns(4)

            with col1:
                st.metric("🌡️ AQI", data["aqi"])
            with col2:
                # Show full risk level text
                risk_short = (
                    risk["level"]
                    .replace("for Sensitive Groups", "⚠️")
                    .replace("Very Unhealthy", "Very Bad")
                )
                st.metric("⚠️ Risk Level", risk['level'])
            with col3:
                # Round temperature
                temp = data.get('t', 'N/A')
                temp_display = (
                    f"{round(float(temp), 1)}°C"
                    if temp != 'N/A'
                    else 'N/A'
                )
                st.metric("🌡️ Temperature", temp_display)
            with col4:
                # Round humidity
                humidity = data.get('h', 'N/A')
                humidity_display = (
                    f"{round(float(humidity), 1)}%"
                    if humidity != 'N/A'
                    else 'N/A'
                )
                st.metric("💧 Humidity", humidity_display)

            # Gauge and pollutants
            col_left, col_right = st.columns(2)

            with col_left:
                gauge = create_aqi_gauge(
                    data["aqi"],
                    data["city"]
                )
                st.plotly_chart(
                    gauge,
                    use_container_width=True
                )

            with col_right:
                poll_chart = create_pollutant_chart(data)
                st.plotly_chart(
                    poll_chart,
                    use_container_width=True
                )

            st.markdown("---")

            # Health advisory
            st.markdown(
                '<p class="section-title">'
                f'{risk["emoji"]} AQI Overview'
                '</p>',
                unsafe_allow_html=True
            )
            st.info(
                    f"**Summary:** {risk['message']}\n\n"
                    f"**Affected:** {risk['affected']}"
                )
            st.info("ℹ️ **Personalized Analysis:** For specific safety precautions based on age and health conditions, please navigate to the **Health Risk** page.")
            
            st.markdown("---")

            # Weather parameters
            st.markdown(
                '<p class="section-title">'
                '🌤️ Weather Parameters'
                '</p>',
                unsafe_allow_html=True
            )

            weather_chart = create_weather_chart(data)
            st.plotly_chart(
                weather_chart,
                use_container_width=True
            )

        else:
            st.error(f"❌ {data['message']}")


# ============================================
# PAGE 3 - ML PREDICTION
# ============================================
elif page == "📈 ML Prediction":
    
    st.markdown(
        '<p class="section-title">'
        '📈 ML-Powered AQI Prediction'
        '</p>',
        unsafe_allow_html=True
    )
    
    st.info(
        "Our XGBoost model trained on 235,785 records "
        "with 95.71% accuracy predicts AQI for major "
        "cities in India!"
    )
    
    st.markdown("---")
    
    

 # Load all 291 cities from dataset
    all_cities = get_all_cities()

    # Input form - 3 columns
    col1, col2, col3 = st.columns(3)

    with col1:
        selected_city = st.selectbox(
            "🏙️ Select City:",
            all_cities,
            index       = None,
            placeholder = "Choose a city...",
        )

        if selected_city:
            defaults       = get_state_defaults(selected_city)
            auto_state     = defaults["state"]
            auto_pollutant = defaults["pollutant"]
            auto_stations  = defaults["stations"]
            st.caption(f"✅ State: {auto_state}")
        else:
            auto_state     = None
            auto_pollutant = None
            auto_stations  = 5

    with col2:
        pollutant_options = [
            "PM2.5", "PM10", "NO2",
            "SO2", "CO", "O3",
            "PM2.5,PM10", "PM10,NO2"
        ]
        try:
            auto_index = pollutant_options.index(
                auto_pollutant
            )
        except:
            auto_index = None

        pollutant = st.selectbox(
            "🧪 Prominent Pollutant:",
            pollutant_options,
            index       = auto_index,
            placeholder = "Choose a pollutant...",
        )
        if selected_city:
            st.caption(
                f"✅ Auto-filled from {selected_city}'s data"
            )

    with col3:
        stations = st.slider(
            "📡 Monitoring Stations:",
            min_value = 1,
            max_value = 20,
            value     = auto_stations
        )
        if selected_city:
            st.caption(
                f"✅ Average for {selected_city}"
            )

    
    # Predict button
    if st.button("🔮 Predict AQI", type="primary"):

        if selected_city is None:
            st.warning("⚠️ Please select a City first!")
        elif pollutant is None:
            st.warning("⚠️ Please select a Pollutant first!")
        

        else:
            with st.spinner("Analyzing City Data..."):
                city_stats = get_city_aqi_stats(selected_city)
                
                try:
                    # 1. Get the dictionary from API
                    api_response = get_air_quality(selected_city)
                    # 2. Extract ONLY the number (AQI) from the dictionary
                    live_val = api_response.get("aqi") if isinstance(api_response, dict) else api_response
                except:
                    live_val = None

                anchor = live_val if live_val else city_stats["aqi_lag1"]

                raw_ml = predict_aqi(
                    state=auto_state, area=selected_city, 
                    pollutant=pollutant, stations=stations, aqi_lag1=anchor
                )

                if live_val:
                    predicted = round((0.95 * live_val) + (0.05 * raw_ml), 1)
                else:
                    predicted = round(raw_ml, 1)
                        
            if predicted:
                risk = get_health_risk(predicted)
                
                st.markdown("---")
                st.markdown(
                    '<p class="section-title">'
                    '🎯 Prediction Results'
                    '</p>',
                    unsafe_allow_html=True
                )
                
                col1, col2, col3 = st.columns(3)
                
                with col1:
                    st.metric(
                        "🔮 Predicted AQI",
                        predicted
                    )
                with col2:
                    who_limit = 15
                    times_limit = round(predicted/who_limit,1)
                    st.metric(
                        "📡 Safety Multiplier",
                        f"{times_limit}x WHO Limit",
                        delta=f"{round(predicted - who_limit,1)} above safe",
                        delta_color="inverse"
                    )
                with col3:
                    st.metric(
                        "🏥 Status",
                        f"{risk['level']} {risk['emoji']}"
                    )
                
                # Gauge chart
                gauge = create_aqi_gauge(
                    predicted,
                    f"{auto_state}"
                )
                st.plotly_chart(
                    gauge,
                    use_container_width=True,
                    key="ml_gauge"
                )
                
                # --- ACCURACY-CHECKED MEDICAL SECTION ---
                st.markdown("---")
                st.write("### 🏥 Health Impact & Pathological Analysis")
        
                # Standardizing the text to match risk dictionary
                status_check = str(risk['level']).lower().strip()

                if "good" in status_check:
                   meds = "None"
                   path = "Optimal oxygen saturation. No clinical risks identified."
                elif "moderate" in status_check:
                   meds = "Allergic Rhinitis, Minor Irritation"
                   path = "Ultrafine particles trigger minor mucus membrane inflammation."
                elif "poor" in status_check:
                   meds = "Chronic Bronchitis, Asthma flare-ups"
                   path = "Particles penetrate upper respiratory tract, narrowing airways."
                elif "unhealthy" in status_check:
                   meds = "COPD, Pneumonia, Hypertension, Cardiac Arrhythmia"
                   path = "PM2.5 enters the alveolar region, causing systemic inflammation."
                # This 'else' ensures that Hazardous/Very Unhealthy ALWAYS show severe impacts
                else: 
                   meds = "Lung Cancer, Ischemic Heart Disease, Stroke"
                   path = "Toxic particles pass through the bloodstream to vital organs, causing DNA damage and cardiovascular stress."
            
                st.error(f"**Potential Medical Conditions:** {meds}")
                st.warning(f"**Pathological Impact:** {path}")
                st.markdown("---")
                st.info("💡 **Deep Dive:** To understand the health limits of specific pollutants like PM2.5 and PM10, please navigate to the **WHO Guidelines** page.")
    
           
# ============================================
# PAGE 4 - HEALTH RISK
# ============================================
elif page == "🏥 Health Risk":
    
    st.markdown(
        '<p class="section-title">'
        '🏥 Health Risk Intelligence'
        '</p>',
        unsafe_allow_html=True
    )

    # ── Personal Health Profile ──────────────
    st.markdown(
        '<p class="section-title">'
        '👤 Your Personal Health Profile'
        '</p>',
        unsafe_allow_html=True
    )

    col1, col2, col3 = st.columns(3)

    with col1:
        age_group = st.selectbox(
            "👤 Age Group:",
            [
                "Child (0-12)",
                "Teen (13-17)",
                "Adult (18-59)",
                "Elderly (60+)"
            ],
            index=2
        )

    with col2:
        health_condition = st.selectbox(
            "🏥 Health Condition:",
            [
        "None (Healthy)",
        "Asthma",
        "COPD(Chronic Obstructive Pulmonary Disease)",
        "Bronchitis",
        "Pneumonia",
        "Allergic Rhinitis",
        "Acute Sinusitis",
        "Heart Disease", 
        "Ischemic Heart Disease",
        "Hypertension",
        "Stroke History",
        "Cardiac Arrhythmia",
        "Lung Cancer",
        "Cognitive Decline",
        "Diabetes",
        "Pregnant", 
        "Eye/Mucus Irritation"  
            ],
            index=0  
        )

    with col3:
        activity_level = st.selectbox(
            "🚶 Activity Level:",
            [
                "Indoor",
                "Light Outdoor",
                "Heavy Outdoor"
            ],
            index=1
        )


    # ── AQI Slider ───────────────────────────
    aqi_input = st.slider(
        "🎚️ Enter AQI Value:",
        min_value = 0,
        max_value = 500,
        value     = 100
    )

    risk = get_health_risk(aqi_input)

    # Get personalized advice
    personal = get_personalized_advice(
        aqi_input,
        age_group,
        health_condition,
        activity_level
    )

    # ── Personalized Advice ──────────────────
    st.markdown(
        '<p class="section-title">'
        f'{personal["emoji"]} '
        f'Personalized Advice for '
        f'{age_group} | {health_condition} | {activity_level}'
        '</p>',
        unsafe_allow_html=True
    )

    if personal["warning"]:
        for w in personal["warning"]:
            st.warning(w)

    if personal["advice"]:
        for a in personal["advice"]:
            st.success(a)

    if personal["is_sensitive"]:
        st.error(
            "🚨 You are in a SENSITIVE GROUP! "
            "Please take extra precautions!"
        )

    
# ============================================
# PAGE 5 - CITY COMPARISON 
# ============================================
elif page == "🌍 City Comparison":
    st.markdown('<p class="section-title">🌍 City Comparison</p>', unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        # Use Chennai as the default instead of Madurai
        default_index_a = cities_list.index("Chennai") if "Chennai" in cities_list else 0
        city_a = st.selectbox("Select First City", cities_list, key="comp_a", index=default_index_a)
        
        data_a = get_air_quality(city_a)
        aqi_a = data_a.get("aqi") if (data_a and isinstance(data_a, dict)) else df[df['City'] == city_a]['AQI'].iloc[0]

    with col2:
        # Use Delhi as the default instead of Jaipur
        default_index_b = cities_list.index("Delhi") if "Delhi" in cities_list else 0
        city_b = st.selectbox("Select Second City", cities_list, key="comp_b", index=default_index_b)
        
        data_b = get_air_quality(city_b)
        aqi_b = data_b.get("aqi") if (data_b and isinstance(data_b, dict)) else df[df['City'] == city_b]['AQI'].iloc[0]

    st.markdown("---")

    if city_a == city_b:
        st.warning("📍 Please select two different cities.")
    else:
        # Comparison logic
        cleaner, dirtier = (city_a, city_b) if aqi_a < aqi_b else (city_b, city_a)
        low, high = (aqi_a, aqi_b) if aqi_a < aqi_b else (aqi_b, aqi_a)
        
        diff = round(((high - low) / high) * 100) if high != 0 else 0

        st.success(f"### {cleaner} is {diff}% cleaner than {dirtier}")

        cols = st.columns(2)
        for i, city in enumerate([{"name": city_a, "aqi": aqi_a}, {"name": city_b, "aqi": aqi_b}]):
            risk = get_health_risk(city["aqi"])
            color = "#2ecc71" if city['name'] == cleaner else "#e74c3c"
            with cols[i]:
                st.markdown(f"""
                <div class="metric-card">
                    <h3>{city['name']}</h3>
                    <h2 style="color: {color}">{city['aqi']}</h2>
                    <p>{risk['emoji']} {risk['level']}</p>
                </div>
                """, unsafe_allow_html=True)

# ============================================
# PAGE 6 - WHO GUIDELINES
# ============================================
elif page == "📖 WHO Guidelines":
    
    st.markdown(
        '<p class="section-title">'
        '📖 WHO Pollutant Guidelines'
        '</p>',
        unsafe_allow_html=True
    )
    
    st.info(
        "World Health Organization (WHO) 2021 "
        "Air Quality Guidelines for major pollutants"
    )
    
    st.markdown("---")
    
    # Guidelines data
    guidelines = [
        {
            "name"   : "PM2.5 (Fine Particles)",
            "emoji"  : "🔴",
            "safe"   : "5 µg/m³ (annual)",
            "danger" : "Above 15 µg/m³",
            "source" : "Vehicle exhaust, burning",
            "effect" : "Lung & heart disease",
            "note"   : "Most dangerous pollutant!"
        },
        {
            "name"   : "PM10 (Coarse Particles)",
            "emoji"  : "🟠",
            "safe"   : "15 µg/m³ (annual)",
            "danger" : "Above 45 µg/m³",
            "source" : "Dust, construction",
            "effect" : "Respiratory problems",
            "note"   : "Common in Indian cities"
        },
        {
            "name"   : "NO2 (Nitrogen Dioxide)",
            "emoji"  : "🟡",
            "safe"   : "10 µg/m³ (annual)",
            "danger" : "Above 25 µg/m³",
            "source" : "Vehicles, power plants",
            "effect" : "Asthma, lung damage",
            "note"   : "High in traffic areas"
        },
        {
            "name"   : "SO2 (Sulphur Dioxide)",
            "emoji"  : "🟡",
            "safe"   : "40 µg/m³ (24hr)",
            "danger" : "Above 100 µg/m³",
            "source" : "Coal burning, factories",
            "effect" : "Acid rain, breathing issues",
            "note"   : "Industrial areas affected"
        },
        {
            "name"   : "CO (Carbon Monoxide)",
            "emoji"  : "🟠",
            "safe"   : "4 mg/m³ (24hr)",
            "danger" : "Above 10 mg/m³",
            "source" : "Incomplete combustion",
            "effect" : "Headache, can be fatal",
            "note"   : "Odorless and invisible!"
        },
        {
            "name"   : "O3 (Ozone)",
            "emoji"  : "🔵",
            "safe"   : "60 µg/m³ (8hr)",
            "danger" : "Above 100 µg/m³",
            "source" : "Sunlight + other pollutants",
            "effect" : "Chest pain, coughing",
            "note"   : "Worse on sunny days"
        },
        {
            "name"   : "Benzene",
            "emoji"  : "🔴",
            "safe"   : "0-5 µg/m³",
            "danger" : "Above 17 µg/m³",
            "source" : "Vehicle exhaust, fuel",
            "effect" : "Can cause CANCER",
            "note"   : "WHO Class 1 Carcinogen!"
        },
        {
            "name"   : "Toluene",
            "emoji"  : "🟠",
            "safe"   : "Below 260 µg/m³",
            "danger" : "Above 1000 µg/m³",
            "source" : "Paint, adhesives, fuel",
            "effect" : "Nervous system damage",
            "note"   : "Common in urban areas"
        },
        {
            "name"   : "Xylene",
            "emoji"  : "🟡",
            "safe"   : "Below 100 µg/m³",
            "danger" : "Above 870 µg/m³",
            "source" : "Printing, rubber, leather",
            "effect" : "Headaches, dizziness",
            "note"   : "Industrial pollutant"
        }
    ]
    
    # Color mapping per pollutant
    danger_colors = {
        "PM2.5 (Fine Particles)"  : "#ff4444",
        "PM10 (Coarse Particles)" : "#ff7e00",
        "NO2 (Nitrogen Dioxide)"  : "#ffcc00",
        "SO2 (Sulphur Dioxide)"   : "#ffcc00",
        "CO (Carbon Monoxide)"    : "#ff7e00",
        "O3 (Ozone)"              : "#4facfe",
        "Benzene"                 : "#ff4444",
        "Toluene"                 : "#ff7e00",
        "Xylene"                  : "#ffcc00"
    }

    for g in guidelines:
        border_color = danger_colors.get(
            g['name'], "#4facfe"
        )
        with st.expander(
            f"{g['emoji']} {g['name']}",
            expanded=False
        ):
            st.markdown(f"""
            <div style="
                background: rgba(255,255,255,0.05);
                border-left: 4px solid {border_color};
                border-radius: 10px;
                padding: 15px;
                margin: 5px 0;
            ">
                <p>
                    <b style="color:{border_color}">
                        ✅ Safe Limit:
                    </b>
                    {g['safe']}
                </p>
                <p>
                    <b style="color:#ff4444">
                        ❌ Dangerous:
                    </b>
                    {g['danger']}
                </p>
                <p>
                    <b style="color:#4facfe">
                        🏭 Source:
                    </b>
                    {g['source']}
                </p>
                <p>
                    <b style="color:#ff7e00">
                        🏥 Health Effect:
                    </b>
                    {g['effect']}
                </p>
                <p>
                    <b style="color:#a0aec0">
                        ℹ️ Note:
                    </b>
                    {g['note']}
                </p>
            </div>
            """, unsafe_allow_html=True)

# ============================================
# PAGE 7 - AI ASSISTANT
# ============================================
elif page == "💬 AI Assistant":

    st.markdown(
        '<p class="section-title">'
        '💬 AirBot - AI Pollution Research Assistant'
        '</p>',
        unsafe_allow_html=True
    )

    st.info(
        "🤖 Hi! I am AirBot — Your personal Air Pollution "
        "Research Assistant! Ask me anything about air "
        "pollution science, policy, history, technology, "
        "or research. I am here to help!"
    )

    st.markdown("---")

    # Initialize chat history
    if "messages" not in st.session_state:
        st.session_state["messages"] = [
            {
                "role"   : "assistant",
                "content": (
                    "👋 Hello! I am **AirBot** 🤖 — "
                    "Your Air Pollution Research Assistant!\n\n"
                    "I can answer questions about:\n"
                    "- 🔬 Pollution science and chemistry\n"
                    "- 🏛️ Government policies and regulations\n"
                    "- 🌍 Global air quality comparisons\n"
                    "- ⚙️ Technologies to reduce pollution\n"
                    "- 📚 History of air pollution\n"
                    "- 💰 Economic impact of pollution\n\n"
                    "What would you like to know?"
                )
            }
        ]

    # Display chat history
    for msg in st.session_state["messages"]:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])

    # Chat input
    user_input = st.chat_input(
        "Ask AirBot anything about air pollution..."
    )

    if user_input:
        # Add user message
        st.session_state["messages"].append({
            "role"   : "user",
            "content": user_input
        })

        # Display user message
        with st.chat_message("user"):
            st.markdown(user_input)

        # Get AI response
        with st.chat_message("assistant"):
            with st.spinner("AirBot is thinking..."):
                try:
                    import google.generativeai as genai

                    genai.configure(
                        api_key=st.secrets["GEMINI_API_KEY"]

                    )
                    # Force the list to see what is actually available for the key
                    for m in genai.list_models():
                      if 'generateContent' in m.supported_generation_methods:
                        print(m.name)

                    model = genai.GenerativeModel(
                        model_name="gemini-2.5-flash-lite",
                        system_instruction="""
                        You are AirBot, an expert AI Research 
                        Assistant specialized in Air Pollution.
                        
                        You have deep knowledge about:
                        - Air pollution science and chemistry
                        - Pollutants like PM2.5, PM10, NO2, 
                          SO2, CO, O3
                        - Government policies and regulations 
                          worldwide
                        - Global air quality comparisons
                        - Technologies to reduce pollution
                        - History of air pollution events
                        - Economic impact of pollution
                        - Climate change and pollution connection
                        - Research studies and findings
                        - India specific pollution problems
                        
                        You do NOT give basic health advice like 
                        "wear a mask" or "stay indoors" as the 
                        platform already provides that.
                        
                        You focus on deep research, science, 
                        policy, history and technology aspects
                        of air pollution.
                        
                        Keep responses clear, informative and 
                        engaging. Use emojis occasionally.
                        Format responses with bullet points 
                        when listing multiple items.
                        Keep responses concise and to the point.
                        """
                    )

                    # Build conversation history
                    history = []
                    for msg in st.session_state["messages"][:-1]:
                        if msg["role"] != "assistant" or len(history) > 0:
                            history.append({
                                "role": "user" if msg["role"] == "user" else "model",
                                "parts": [msg["content"]]
                            })

                    # Start chat with history
                    chat = model.start_chat(
                        history=history if history else []
                    )

                    # Send message
                    response     = chat.send_message(user_input)
                    ai_response  = response.text

                    # Display response
                    st.markdown(ai_response)

                    # Save to history
                    st.session_state["messages"].append({
                        "role"   : "assistant",
                        "content": ai_response
                    })

                except Exception as e:
                    st.error(
                        f"❌ AirBot is unavailable: {e}"
                    )



# ============================================
# FOOTER
# ============================================
st.markdown("---")
st.markdown("""
<div style='text-align:center; color:#a0aec0;'>
    🌍 Air Pollution Analytics & Health Risk 
    Intelligence Platform<br>
    Data: WAQI API + India AQI Dataset 2022-2025 
    + WHO Guidelines 2021<br>
    Built with Python, Streamlit & XGBoost
</div>
""", unsafe_allow_html=True)