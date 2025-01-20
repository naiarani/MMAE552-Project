import requests
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime

# URL for the JSON data
url = "https://services.swpc.noaa.gov/json/goes/primary/xrays-7-day.json"

# Fetch the data
response = requests.get(url)
xray_data = response.json()

# Initialize lists for timestamps and flux values for each wavelength range
timestamps = []
flux_0_1_0_8 = []
flux_0_05_0_4 = []

for entry in xray_data:
    # Parse the timestamp and convert it to a datetime object
    timestamp = datetime.strptime(entry["time_tag"], "%Y-%m-%dT%H:%M:%SZ")
    
    # Append timestamp if it's not already in the list
    if timestamp not in timestamps:
        timestamps.append(timestamp)
    
    # Store flux based on energy range
    if entry["energy"] == "0.1-0.8nm":
        flux_0_1_0_8.append(entry["flux"])
    elif entry["energy"] == "0.05-0.4nm":
        flux_0_05_0_4.append(entry["flux"])

# Ensure both lists have the same length as timestamps
# Fill missing values with None if necessary
if len(flux_0_1_0_8) < len(timestamps):
    flux_0_1_0_8 += [None] * (len(timestamps) - len(flux_0_1_0_8))
if len(flux_0_05_0_4) < len(timestamps):
    flux_0_05_0_4 += [None] * (len(timestamps) - len(flux_0_05_0_4))

# Create a DataFrame for easy plotting
df = pd.DataFrame({
    "Timestamp": timestamps,
    "Flux (0.1-0.8 nm)": flux_0_1_0_8,
    "Flux (0.05-0.4 nm)": flux_0_05_0_4
})
df.set_index("Timestamp", inplace=True)

# Plot the data
plt.figure(figsize=(12, 6))
plt.plot(df.index, df["Flux (0.1-0.8 nm)"], label="0.1-0.8 nm", color="blue")
plt.plot(df.index, df["Flux (0.05-0.4 nm)"], label="0.05-0.4 nm", color="red")
plt.yscale("log")  # Use a log scale for X-ray flux
plt.xlabel("Time")
plt.ylabel("X-ray Flux (W/m²)")
plt.title("GOES X-ray Flux Over the Past 7 Days")
plt.legend()
plt.grid(True)
plt.tight_layout()
plt.show()

##

import numpy as np

# Add a simple temperature proxy based on the log of the X-ray flux
df["Temperature Proxy (0.1-0.8 nm)"] = np.log10(df["Flux (0.1-0.8 nm)"])
df["Temperature Proxy (0.05-0.4 nm)"] = np.log10(df["Flux (0.05-0.4 nm)"])

# Calculate correlation between X-ray flux and temperature proxy
correlation_0_1_0_8 = df["Flux (0.1-0.8 nm)"].corr(df["Temperature Proxy (0.1-0.8 nm)"])
correlation_0_05_0_4 = df["Flux (0.05-0.4 nm)"].corr(df["Temperature Proxy (0.05-0.4 nm)"])
print(f"Correlation between X-ray flux (0.1-0.8 nm) and temperature proxy: {correlation_0_1_0_8}")
print(f"Correlation between X-ray flux (0.05-0.4 nm) and temperature proxy: {correlation_0_05_0_4}")

# Scatter plot to show correlation
plt.figure(figsize=(12, 6))
plt.scatter(df["Flux (0.1-0.8 nm)"], df["Temperature Proxy (0.1-0.8 nm)"], color="blue", label="0.1-0.8 nm")
plt.scatter(df["Flux (0.05-0.4 nm)"], df["Temperature Proxy (0.05-0.4 nm)"], color="red", label="0.05-0.4 nm")
plt.xlabel("X-ray Flux (W/m²)")
plt.ylabel("Temperature Proxy (log(Flux))")
plt.title("Correlation between X-ray Flux and Temperature Proxy")
plt.legend()
plt.grid(True)
plt.tight_layout()
plt.show()
