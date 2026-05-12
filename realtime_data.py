# realtime_data.py
# Fetches live air quality data from API

import requests
import streamlit as st 

# ⚠️ Replace with YOUR actual API key!
API_KEY =st.secrets["WAQI_API_KEY"]

# ============================================
# CITY NAME MAPPING
# Some cities need specific names for API
# ============================================
CITY_MAPPING = {
    # Problem cities - need country specified
    "kochi"              : "Kochi, India",
    "tura"               : "Tura, India",
    "leh"                : "Leh, India",
    
    # Normal cities
    "naharlagun"         : "Naharlagun",
    "guwahati"           : "Guwahati",
    "patna"              : "Patna",
    "gaya"               : "Gaya",
    "raipur"             : "Raipur",
    "bhilai"             : "Bhilai",
    "ahmedabad"          : "Ahmedabad",
    "gandhinagar"        : "Gandhinagar",
    "faridabad"          : "Faridabad",
    "ambala"             : "Ambala",
    "rohtak"             : "Rohtak",
    "karnal"             : "Karnal",
    "bangalore"          : "Bangalore",
    "mangalore"          : "Mangalore",
    "hubli"              : "Hubli",
    "belgaum"            : "Belgaum",
    "thiruvananthapuram" : "Thiruvananthapuram",
    "bhopal"             : "Bhopal",
    "jabalpur"           : "Jabalpur",
    "gwalior"            : "Gwalior",
    "mumbai"             : "Mumbai",
    "pune"               : "Pune",
    "shillong"           : "Shillong",
    "aizawl"             : "Aizawl",
    "kohima"             : "Kohima",
    "ludhiana"           : "Ludhiana",
    "amritsar"           : "Amritsar",
    "jaipur"             : "Jaipur",
    "jodhpur"            : "Jodhpur",
    "gangtok"            : "Gangtok",
    "chennai"            : "Chennai",
    "coimbatore"         : "Coimbatore",
    "salem"              : "Salem",
    "thoothukudi"        : "Thoothukudi",
    "tiruppur"           : "Tiruppur",
    "dindigul"           : "Dindigul",
    "ramanathapuram"     : "Ramanathapuram",
    "hyderabad"          : "Hyderabad",
    "agartala"           : "Agartala",
    "lucknow"            : "Lucknow",
    "kanpur"             : "Kanpur",
    "dehradun"           : "Dehradun",
    "kolkata"            : "Kolkata",
    "siliguri"           : "Siliguri",
    "delhi"              : "Delhi",
    "noida"              : "Noida",
    "chandigarh"         : "Chandigarh",
    "panchkula"          : "Panchkula",
    "puducherry"         : "Puducherry",
    "srinagar"           : "Srinagar",
}

def get_air_quality(city):
    """
    Fetches live air quality data
    for any given city
    """
    
    # Convert city to lowercase
    city_lower = city.lower().strip()
    
    # Get mapped city name
    mapped_city = CITY_MAPPING.get(
        city_lower,
        city_lower
    )
    
    # Try multiple URL formats
    urls_to_try = [
        f"https://api.waqi.info/feed/{mapped_city}/?token={API_KEY}",
        f"https://api.waqi.info/feed/@{mapped_city}/?token={API_KEY}",
        f"https://api.waqi.info/feed/{city}/?token={API_KEY}",
    ]
    
    for url in urls_to_try:
        try:
            response = requests.get(url, timeout=10)
            data     = response.json()
            
            if data["status"] == "ok":
                
                aqi       = data["data"]["aqi"]
                city_name = data["data"]["city"]["name"]
                iaqi      = data["data"].get("iaqi", {})

                # If AQI is "-" or invalid
                # calculate from pollutants! ✅
                if str(aqi) == "-" or aqi == "" or aqi is None:
                    # Try to get from dominant pollutant
                    pollutant_values = []
                    for poll in ["pm25","pm10","no2","so2","co","o3"]:
                        v = iaqi.get(poll, {}).get("v", None)
                        if v is not None:
                            try:
                                pollutant_values.append(
                                    float(v)
                                )
                            except:
                                pass
                    if pollutant_values:
                        aqi = int(max(pollutant_values))
                    else:
                        aqi = 0
                else:
                    try:
                        aqi = int(float(aqi))
                    except:
                        aqi = 0
                
                # Pollutants
                pm25 = iaqi.get("pm25", {}).get("v", "N/A")
                pm10 = iaqi.get("pm10", {}).get("v", "N/A")
                no2  = iaqi.get("no2",  {}).get("v", "N/A")
                so2  = iaqi.get("so2",  {}).get("v", "N/A")
                co   = iaqi.get("co",   {}).get("v", "N/A")
                o3   = iaqi.get("o3",   {}).get("v", "N/A")
                
                # Weather parameters
                t  = iaqi.get("t",  {}).get("v", "N/A")
                h  = iaqi.get("h",  {}).get("v", "N/A")
                w  = iaqi.get("w",  {}).get("v", "N/A")
                p  = iaqi.get("p",  {}).get("v", "N/A")
                wd = iaqi.get("wd", {}).get("v", "N/A")
                wg = iaqi.get("wg", {}).get("v", "N/A")
                
                return {
                    "status"  : "success",
                    "city"    : city_name,
                    "aqi"     : aqi,
                    # Pollutants
                    "pm25"    : pm25,
                    "pm10"    : pm10,
                    "no2"     : no2,
                    "so2"     : so2,
                    "co"      : co,
                    "o3"      : o3,
                    # Weather
                    "t"       : t,
                    "h"       : h,
                    "w"       : w,
                    "p"       : p,
                    "wd"      : wd,
                    "wg"      : wg
                }
        
        except Exception as e:
            continue
    
    # If all URLs failed
    # Try search API as last resort
    try:
        search_url = (
            f"https://api.waqi.info/search/"
            f"?token={API_KEY}&keyword={city}"
        )
        search_response = requests.get(
            search_url,
            timeout=10
        )
        search_data = search_response.json()
        
        if (search_data["status"] == "ok" and
            len(search_data["data"]) > 0):
            
            # Get first result's station ID
            station_id = search_data["data"][0]["uid"]
            
            # Fetch data for that station
            station_url = (
                f"https://api.waqi.info/feed/"
                f"@{station_id}/?token={API_KEY}"
            )
            station_response = requests.get(
                station_url,
                timeout=10
            )
            station_data = station_response.json()
            
            if station_data["status"] == "ok":
                
                aqi       = data["data"]["aqi"]
                city_name = data["data"]["city"]["name"]
                iaqi      = data["data"].get("iaqi", {})

                # If AQI is "-" or invalid
                # calculate from pollutants! ✅
                if str(aqi) == "-" or aqi == "" or aqi is None:
                    # Try to get from dominant pollutant
                    pollutant_values = []
                    for poll in ["pm25","pm10","no2","so2","co","o3"]:
                        v = iaqi.get(poll, {}).get("v", None)
                        if v is not None:
                            try:
                                pollutant_values.append(
                                    float(v)
                                )
                            except:
                                pass
                    if pollutant_values:
                        aqi = int(max(pollutant_values))
                    else:
                        aqi = 0
                else:
                    try:
                        aqi = int(float(aqi))
                    except:
                        aqi = 0
                
                pm25 = iaqi.get("pm25", {}).get("v", "N/A")
                pm10 = iaqi.get("pm10", {}).get("v", "N/A")
                no2  = iaqi.get("no2",  {}).get("v", "N/A")
                so2  = iaqi.get("so2",  {}).get("v", "N/A")
                co   = iaqi.get("co",   {}).get("v", "N/A")
                o3   = iaqi.get("o3",   {}).get("v", "N/A")
                t    = iaqi.get("t",    {}).get("v", "N/A")
                h    = iaqi.get("h",    {}).get("v", "N/A")
                w    = iaqi.get("w",    {}).get("v", "N/A")
                p    = iaqi.get("p",    {}).get("v", "N/A")
                wd   = iaqi.get("wd",   {}).get("v", "N/A")
                wg   = iaqi.get("wg",   {}).get("v", "N/A")
                
                return {
                    "status"  : "success",
                    "city"    : city_name,
                    "aqi"     : aqi,
                    "pm25"    : pm25,
                    "pm10"    : pm10,
                    "no2"     : no2,
                    "so2"     : so2,
                    "co"      : co,
                    "o3"      : o3,
                    "t"       : t,
                    "h"       : h,
                    "w"       : w,
                    "p"       : p,
                    "wd"      : wd,
                    "wg"      : wg
                }
    
    except Exception as e:
        pass
    
    return {
        "status" : "error",
        "message": f"City '{city}' not found! Try another city name."
    }


def get_multiple_cities():
    """
    Fetches live data for all
    major Indian cities
    """
    
    cities = [
        "delhi",
        "mumbai",
        "pune",
        "chennai",
        "kolkata",
        "bangalore",
        "hyderabad",
        "ahmedabad",
        "jaipur",
        "lucknow"
    ]
    
    results = []
    
    for city in cities:
        data = get_air_quality(city)
        if data["status"] == "success":
            results.append(data)
    
    return results


# Test when run directly
if __name__ == "__main__":
    
    print("Testing cities...")
    
    test_cities = [
        "delhi",
        "mumbai",
        "chennai",
        "bangalore"
    ]
    
    for city in test_cities:
        result = get_air_quality(city)
        if result["status"] == "success":
            print(f"✅ {city}: AQI = {result['aqi']}")
        else:
            print(f"❌ {city}: {result['message']}")