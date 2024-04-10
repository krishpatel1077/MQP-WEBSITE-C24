# Load NeuroKit and other useful packages
import neurokit2 as nk
import pandas as pd
import matplotlib.pyplot as plt
plt.rcParams['figure.figsize'] = [15, 5]  # Bigger images

# Get data
ecg = pd.read_csv("heart_rate_jennifer_dribble.csv", header=None)

# Rename the columns for clarity
ecg.columns = ["Time", "ECG_Signal"]

# # Visualize signal and save as graph
nk.signal_plot(ecg["ECG_Signal"])
plt.savefig("ecg_signal_resp.png")

# Extract peaks
rpeaks, info = nk.ecg_peaks(ecg["ECG_Signal"], sampling_rate=75)

# Compute rate
ecg_rate = nk.ecg_rate(rpeaks, sampling_rate=75, desired_length=len(ecg))

edr = nk.ecg_rsp(ecg_rate, sampling_rate=75)

# Visual comparison
nk.signal_plot(edr)
plt.savefig("edr_signal_resp.png")

# Clean signal
cleaned = nk.rsp_clean(edr, sampling_rate=75)

# Extract peaks
df, peaks_dict = nk.rsp_peaks(cleaned)
info = nk.rsp_fixpeaks(peaks_dict)
formatted = nk.signal_formatpeaks(info, desired_length=len(cleaned), peak_indices=info["RSP_Peaks"])

# Extract rate
rsp_rate = nk.rsp_rate(cleaned, peaks_dict, sampling_rate=75)

# Plot
nk.signal_plot(rsp_rate, sampling_rate=75)
plt.ylabel('Breaths Per Minute')
plt.savefig("rsp_rate_resp.png")

# Show the plots
plt.show()

# Print the respiratory rate
print(rsp_rate)
