import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

# Load CSV data into a DataFrame without headers
csv_file_path = 'heatmap_test.csv'
df = pd.read_csv(csv_file_path, header=None)

# Rename columns to latitude and longitude
df.columns = ['Latitude', 'Longitude']

# Define the corners of the box
corner_coordinates = [
    (42.276444, -71.810175),  # Top left corner
    (42.276061, -71.809453),  # Top right corner
    (42.275215, -71.81028),   # Bottom left corner
    (42.275599, -71.810996)   # Bottom right corner
]

# Create a heatmap
plt.figure(figsize=(10, 7))

# Set the background color to light green
plt.gca().set_facecolor('#CCFFCC')

ax = sns.kdeplot(data=df, x='Longitude', y='Latitude', fill=False, cmap="Reds", thresh=0, levels=100, cbar_kws={'label': 'Density'})

# Set labels and title
ax.set_xlabel('Longitude')
ax.set_ylabel('Latitude')
ax.set_title('Zoomed-in Density Heatmap of GPS Data with Box Overlay')

# Set limits to show around the corners
min_lat = min([coord[0] for coord in corner_coordinates])
max_lat = max([coord[0] for coord in corner_coordinates])
min_lon = min([coord[1] for coord in corner_coordinates])
max_lon = max([coord[1] for coord in corner_coordinates])
ax.set_xlim(min_lon, max_lon)
ax.set_ylim(min_lat, max_lat)

# Draw rectangle around the corners
rect = plt.Rectangle((min_lon, min_lat), max_lon - min_lon, max_lat - min_lat, fill=False, edgecolor='blue', linewidth=2)
ax.add_patch(rect)

# Show the plot
plt.show()
