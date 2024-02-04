import pandas as pd
import json
import matplotlib.pyplot as plt
import seaborn as sns
import geopandas as gpd
from shapely.geometry import Point, LineString
import numpy as np
import os

def load_and_preprocess(file_name):
    try:
        with open(file_name, 'r') as file:
            data = json.load(file)
        df = pd.json_normalize(data)
        
        # Convert pubMillis and request_time to datetime format
        df['pubMillis'] = pd.to_datetime(df['pubMillis'], unit='ms')
        df['request_time'] = pd.to_datetime(df['request_time'], unit='ms')
        
        # Handling different structures for alerts and jams
        if 'location.x' in df.columns and 'location.y' in df.columns:
            # Handling alerts structure
            df['geometry'] = df.apply(lambda row: Point(row['location.x'], row['location.y']), axis=1)
        elif 'line' in df.columns:
            # Handling jams structure
            # Assuming 'line' is a list of coordinate objects
            df['geometry'] = df['line'].apply(lambda coords: LineString([(coord['x'], coord['y']) for coord in coords]))
        else:
            print(f"Location data not found in the file: {file_name}")
            return None
        
        # Drop any rows with missing critical values
        critical_columns = ['uuid', 'type', 'pubMillis', 'geometry']
        df.dropna(subset=critical_columns, inplace=True)
        
        # Drop duplicates based on uuid
        df.drop_duplicates(subset=['uuid'], inplace=True)
        
        return df
    except json.JSONDecodeError as e:
        print(f"Error reading {file_name}: {e}")
        return None

def create_geodataframe(df):
    if df is not None:
        return gpd.GeoDataFrame(df, geometry='geometry')
    else:
        print("Unable to create GeoDataFrame, input DataFrame is None.")
        return NoneS

# Use the relative path from the script to the json files
alerts_df = load_and_preprocess('TM_Exam/alerts-processed.json')
jams_df = load_and_preprocess('TM_Exam/jams-processed.json')

# Create GeoDataFrames if the data was loaded successfully
alerts_gdf = create_geodataframe(alerts_df)
jams_gdf = create_geodataframe(jams_df)

# Check if the DataFrames were created successfully before attempting to print or use them
if alerts_gdf is not None:
    print("Alerts Data:")
    print(alerts_gdf.head())

if jams_gdf is not None:
    print("Jams Data:")
    print(jams_gdf.head())

# Display the first few rows
print("Alerts Data:")
print(alerts_df.head())
print("\nJams Data:")
print(jams_df.head())

# Basic Statistical AnalysisS
print("Basic Statistics for Alerts:")
print(alerts_df.describe())
print("\nBasic Statistics for Jams:")
print(jams_df.describe())

# Step 2: Check for Missing Values
print("\nMissing Values in Alerts Data:")
print(alerts_df.isnull().sum())
print("\nMissing Values in Jams Data:")
print(jams_df.isnull().sum())

# Step 3: Explore Time Trends
alerts_df['pubMillis'] = pd.to_datetime(alerts_df['pubMillis'], unit='ms')
jams_df['pubMillis'] = pd.to_datetime(jams_df['pubMillis'], unit='ms')

# Plotting time trends
plt.figure(figsize=(12, 6))
plt.plot(alerts_df['pubMillis'], alerts_df.index, label='Alerts')
plt.plot(jams_df['pubMillis'], jams_df.index, label='Jams')
plt.title('Time Trends of Alerts and Jams')
plt.xlabel('Time')
plt.ylabel('Count')
plt.legend()
plt.show()


# EDA - Basic Descriptive Statistics
print(alerts_df.describe())

# EDA - Temporal Analysis
alerts_df['hour'] = alerts_df['pubMillis'].dt.hour
plt.figure(figsize=(12, 6))
sns.countplot(x='hour', data=alerts_df)
plt.title('Alerts by Hour')
plt.xlabel('Hour of Day')
plt.ylabel('Number of Alerts')
plt.show()

# EDA - Correlation Analysis
correlation_features = ['reliability', 'reportRating', 'nThumbsUp']
correlation_matrix = alerts_df[correlation_features].corr()
sns.heatmap(correlation_matrix, annot=True)
plt.title('Correlation Matrix of Alerts')
plt.show()

# EDA - Spatial Analysis
fig, ax = plt.subplots(figsize=(10, 10))
alerts_gdf.plot(ax=ax, color='blue', markersize=5)
plt.title('Spatial Distribution of Alerts')
plt.xlabel('Longitude')
plt.ylabel('Latitude')
plt.show()
