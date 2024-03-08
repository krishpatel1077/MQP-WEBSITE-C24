import neurokit2 as nk
import pandas as pd
# Load CSV file
data = pd.read_csv("heart_rate.csv", header=None)
# Rename columns
data.columns = ["Time", "ECG"]
# Sampling rate
sampling_rate = 75  # 75 points per second
# Detect R-peaks
r_peaks = nk.ecg_findpeaks(data["ECG"], sampling_rate=sampling_rate)
# Calculate bpm
bpm = nk.ecg_rate(r_peaks, sampling_rate=sampling_rate, desired_length=len(data))
print("Heart rate (bpm):", bpm.mean())