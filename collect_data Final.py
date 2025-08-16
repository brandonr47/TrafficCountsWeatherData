# Air Quality and Traffic Data Collection


import pandas as pd
import requests

# API key for PurpleAir
API_KEY = "1E6A51DA-4669-11F0-81BE-42010A80001F"

print("Starting data collection...")

# Get air quality data from PurpleAir
print("Getting air quality data...")

url = "https://api.purpleair.com/v1/sensors?fields=sensor_index,date_created,last_seen,latitude,longitude,humidity,pm2.5&location_type=0&nwlng=-117.3&nwlat=33.2&selng=-116.7&selat=32.5"

response = requests.get(url, headers={"X-API-Key": API_KEY})

if response.status_code == 200:
    data = response.json()
    sensors = data["data"]
    
    # Make dataframe
    air_df = pd.DataFrame(sensors, columns=["sensor_id", "date_created", "last_seen", "latitude", "longitude", "humidity", "pm25"])
    
    # Clean the data
    air_df['latitude'] = pd.to_numeric(air_df['latitude'], errors='coerce')
    air_df['longitude'] = pd.to_numeric(air_df['longitude'], errors='coerce')
    air_df['humidity'] = pd.to_numeric(air_df['humidity'], errors='coerce')
    air_df['pm25'] = pd.to_numeric(air_df['pm25'], errors='coerce')
    
    air_df = air_df.dropna()
    
    print(f"Got {len(air_df)} air quality sensors")
    
else:
    print("Error getting air quality data")
    air_df = pd.DataFrame()

# Load traffic data
print("Loading traffic data...")

traffic_df = pd.read_csv("../traffic_counts.csv")

# Clean traffic data
traffic_df['total_count'] = pd.to_numeric(traffic_df['total_count'], errors='coerce')
traffic_df = traffic_df.dropna(subset=['total_count'])

print(f"Got {len(traffic_df)} traffic records")

# Save the data
air_df.to_csv("air_quality_data.csv", index=False)
traffic_df.to_csv("traffic_data.csv", index=False)

print("Data collection complete!")
print(f"Total samples: {len(air_df) + len(traffic_df)}")

# Show some basic info
print("\nAir Quality Summary:")
print(f"Average PM2.5: {air_df['pm25'].mean():.1f}")
print(f"Average Humidity: {air_df['humidity'].mean():.1f}%")

print("\nTraffic Summary:")
print(f"Average Daily Traffic: {traffic_df['total_count'].mean():.0f}")
print(f"Number of Streets: {traffic_df['street_name'].nunique()}")

