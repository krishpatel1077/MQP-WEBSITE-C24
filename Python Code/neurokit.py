import neurokit2 as nk
import pandas as pd
import matplotlib.pyplot as plt

# Download example data
data = pd.read_csv("heart_rate.csv")

# Process ecg
ecg_signals, info = nk.ecg_process(data.iloc[:, 1], sampling_rate=75)  # Accessing the second column with iloc

# Plot the graph
plot = nk.ecg_plot(ecg_signals[:3000], info)

# Save the graph
plt.savefig("neurokit_testplot.png")
