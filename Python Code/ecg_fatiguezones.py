import numpy as np
import neurokit2 as nk
import pandas as pd
import matplotlib.pyplot as plt

# Define function to calculate fatigue score
def fatigue_score(bpm):
    max_HR = 220 - 22  # Assuming age is 22

    lowest_nonfatigue_HR = max_HR * 0.64
    highest_nonfatigue_HR = max_HR * 0.77
    lowest_fatigue_HR = max_HR * 0.77

    return (bpm) / max_HR * 100

# Step 1: Read the CSV file
# Load CSV file
data = pd.read_csv("Output files/csv files/ecg/heart_rate_subject6_baseline.csv", header=None)
# Rename columns
data.columns = ["Time", "ECG"]
# Sampling rate
sampling_rate = 100  # 75 points per second
# Detect R-peaks
r_peaks = nk.ecg_findpeaks(data["ECG"], sampling_rate=sampling_rate)

# Step 2: Create chunks of data and calculate scores
chunk_size = len(data) // 6  # Set chunk size to length of data divided by 6
chunk_scores = []

output_text = []  # Store output text

# Create a single figure with 6 subplots
fig, axes = plt.subplots(nrows=2, ncols=3, figsize=(22, 12))
colors = ['green', 'yellow', 'red']  # Fatigue score color codes

for i, ax in enumerate(axes.flatten()):
    start_index = i * chunk_size
    end_index = (i + 1) * chunk_size
    chunk_data = data["ECG"][start_index:end_index]
    chunk_r_peaks = nk.ecg_findpeaks(chunk_data, sampling_rate=sampling_rate)
    if len(chunk_r_peaks) > 0:  # Check if there are R-peaks in the chunk
        chunk_bpm = nk.ecg_rate(chunk_r_peaks, sampling_rate=sampling_rate, desired_length=len(chunk_data))
        average_bpm = chunk_bpm.mean()
        chunk_score = fatigue_score(average_bpm)
        chunk_scores.append(chunk_score)
        # Append chunk info to output text
        output_text.append(f"Chunk {i+1} - Score: {chunk_score:.4f}, BPM: {average_bpm:.2f}")

        # Plot individual graphs for each chunk
        ax.plot(chunk_data, color=colors[int(np.digitize(chunk_score, [64, 77]))])  # Color code signal
        ax.set_xlabel('Sample #', fontsize=14)
        ax.set_ylabel('Amplitude (mV)', fontsize=14)
        ax.set_title(f'Chunk {i+1} - ECG Signal & Fatigue Score', fontsize=16)
        ax.grid(True)

        # Display fatigue score and BPM on each subplot
        ax.text(0.05, 0.05, f"Score: {chunk_score:.4f}", transform=ax.transAxes, fontsize=16, fontweight='bold',
                bbox=dict(facecolor='white', edgecolor='black', boxstyle='round,pad=0.5'))
        ax.text(0.65, 0.05, f"BPM: {average_bpm:.2f}", transform=ax.transAxes, fontsize=16, fontweight='bold',
                bbox=dict(facecolor='white', edgecolor='black', boxstyle='round,pad=0.5'))


# Adjust layout
plt.tight_layout()

# Show plot
plt.show()

# Step 3: Calculate total fatigue score
total_fatigue_score = np.mean(chunk_scores)

# Step 4: Print the output text to a file
with open("output.txt", "w") as file:
    for line in output_text:
        file.write(line + "\n")

# Print total fatigue score
print("Total Fatigue Score:", total_fatigue_score)
