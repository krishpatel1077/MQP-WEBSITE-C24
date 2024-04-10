import pandas as pd
import matplotlib.pyplot as plt

# Load CSV file
data = pd.read_csv("heart_rate_jennifer_dribble.csv", header=None)

# Plot ECG signal relative to the number of samples
plt.figure(figsize=(12, 6))  # Set the figure size
plt.plot(data.index, data[1], color='black')  # Assuming the second column is indexed as 1
plt.title('ECG Signal')
plt.xlabel('Samples')
plt.ylabel('ECG Signal (mV)')
plt.grid(True)
plt.show()
