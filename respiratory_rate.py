# Load NeuroKit and other useful packages
import neurokit2 as nk
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
%matplotlib inline
plt.rcParams['figure.figsize'] = [15, 5]  # Bigger images
# Get data
ecg = pd.read_csv("heart_rate_jennifer_dribble.csv")
# Extract values from the "ECG" column
#ecg = np.array(data["ecg"])
# Visualize signal
nk.signal_plot(ecg)
# Extract peaks
rpeaks, info = nk.ecg_peaks(ecg, sampling_rate=75)
# Compute rate
ecg_rate = nk.ecg_rate(rpeaks, sampling_rate=75, desired_length=len(ecg))
edr = nk.ecg_rsp(ecg_rate, sampling_rate=75)
# Visual comparison
nk.signal_plot(edr)
#Clean signal
cleaned = nk.rsp_clean(edr, sampling_rate=75)
# Extract peaks
df, peaks_dict = nk.rsp_peaks(cleaned)
info = nk.rsp_fixpeaks(peaks_dict)
formatted = nk.signal_formatpeaks(info, desired_length=len(cleaned),peak_indices=info["RSP_Peaks"])
# Extract rate
rsp_rate = nk.rsp_rate(cleaned, peaks_dict, sampling_rate=75)
nk.signal_plot(pd.DataFrame({"RSP_Raw": edr, "RSP_Clean": cleaned}), sampling_rate=75, subplots=True)
candidate_peaks = nk.events_plot(peaks_dict['RSP_Peaks'], cleaned)
fixed_peaks = nk.events_plot(info['RSP_Peaks'], cleaned)
# Extract rate
rsp_rate = nk.rsp_rate(cleaned, peaks_dict, sampling_rate=75)
print(rsp_rate)
# Visualize
nk.signal_plot(rsp_rate, sampling_rate=75)
plt.ylabel('Breaths Per Minute')