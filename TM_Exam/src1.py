import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import os


project_root_dir = os.path.dirname(os.path.abspath(__file__))
filepath_alerts = os.path.join(project_root_dir , 'alerts-processed.json')
filepath_jams = os.path.join(project_root_dir , 'jams-processed.json')
alerts_df = pd.read_json(filepath_alerts)
jams_df = pd.read_json(filepath_jams)

# Display the first few rows
print("Alerts Data:")
print(alerts_df.head())
print("\nJams Data:")
print(jams_df.head())

# Basic statistics and data types
print("\nAlerts Data Info:")
print(alerts_df.info())
print("\nJams Data Info:")
print(jams_df.info())

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


# Step 5: Waze Alerts Analysis
plt.figure(figsize=(12, 6))
sns.countplot(data=alerts_df, x='type')
plt.title('Distribution of Alert Types')
plt.xlabel('Alert Type')
plt.ylabel('Count')
plt.show()

plt.figure(figsize=(12, 6))
sns.scatterplot(data=alerts_df, x='reportRating', y='reliability')
plt.title('Relationship between Report Rating and Reliability in Alerts')
plt.xlabel('Report Rating')
plt.ylabel('Reliability')
plt.show()

# Step 6: Waze Jams Analysis
plt.figure(figsize=(12, 6))
sns.countplot(data=jams_df, x='type')
plt.title('Distribution of Jam Types')
plt.xlabel('Jam Type')
plt.ylabel('Count')
plt.show()

plt.figure(figsize=(12, 6))
sns.scatterplot(data=jams_df, x='level', y='length')
plt.title('Relationship between Traffic Congestion Level and Jam Length')
plt.xlabel('Traffic Congestion Level')
plt.ylabel('Jam Length')
plt.show()

# Step 7: Correlation Analysis
corr_alerts = alerts_df.corr()
corr_jams = jams_df.corr()