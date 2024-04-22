import neurokit2 as nk
import pandas as pd
import requests
from io import StringIO
import matplotlib.pyplot as plt
# URL of the CSV file
url = "http://192.168.105.245/heart_rate"  # Replace this with the actual URL of your CSV file
# Read CSV file from URL
response = requests.get(url)
data = pd.read_csv(StringIO(response.text))
# Process ECG
ecg_signals, info = nk.ecg_process(data.iloc[:, 1], sampling_rate=75)  # Accessing the second column with iloc
# Plot ECG
fig = nk.ecg_plot(ecg_signals[:3000], info)
# Save plot as PNG file
plot_filename = "ecg_plot.png"
fig.savefig(plot_filename)
# Generate HTML code to embed the plot in a webpage
html_code = f"""
<!DOCTYPE html>
<html>
<head>
  <title>ECG Plot</title>
</head>
<body>
  <h2>ECG Plot</h2>
  <img src="{plot_filename}" alt="ECG Plot">
</body>
</html>
"""
# Save HTML code to a file
html_filename = "index.html"
with open(html_filename, "w") as html_file:
    html_file.write(html_code)
print(f"Plot saved as '{plot_filename}'")
print(f"HTML file saved as '{html_filename}'")