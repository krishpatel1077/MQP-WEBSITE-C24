import csv
import matplotlib.pyplot as plt
import neurokit2 as nk

# Replace 'heart_rate.csv' with the actual filename if it's different
input_file = 'heart_rate.csv'

# Lists to store data from the CSV file
timestamps = []
heart_rates = []

try:
    # Open the CSV file for reading
    with open(input_file, 'r') as csvfile:
        # Create a CSV reader object
        reader = csv.reader(csvfile)

        # Skip the header if there is one
        # next(reader, None)

        # Iterate through rows and extract data
        for row in reader:
            timestamps.append(int(row[0]))
            heart_rates.append(float(row[1]))

    # NeuroKit processing
    ecg_signals, info = nk.ecg_process(heart_rates, sampling_rate=1.0 / (timestamps[1] - timestamps[0]))

    # Create a line plot
    plt.plot(ecg_signals['ECG_Rate'], marker='o', linestyle='-')
    plt.title('Heart Rate Over Time (NeuroKit Processed)')
    plt.xlabel('Sample')
    plt.ylabel('Heart Rate')
    plt.grid(True)
    plt.show()

except FileNotFoundError:
    print(f"Error: The file '{input_file}' does not exist.")
except Exception as e:
    print(f"Error: {e}")
