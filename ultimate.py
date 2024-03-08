import requests
import csv
from io import StringIO
import matplotlib.pyplot as plt
import pandas as pd
import time
import neurokit2 as nk

def fetch_csv_data(url_csv, output_file):
    try:
        response_csv = requests.get(url_csv)
        if response_csv.status_code == 200:
            csv_data = StringIO(response_csv.text)
            reader = csv.reader(csv_data)
            with open(output_file, 'w', newline='') as csvfile:
                csv_writer = csv.writer(csvfile)
                for row in reader:
                    csv_writer.writerow(row)
            print(f"Data has been successfully written to {output_file}")
        else:
            print(f"Error: Unable to fetch CSV data. Status code: {response_csv.status_code}")
    except requests.ConnectionError:
        print("Error: Unable to establish connection to the server.")
    except requests.RequestException as e:
        print(f"Error: {e}")

def plot_csv_data(input_file, output_plot, title):
    timestamps = []
    values = []
    try:
        with open(input_file, 'r') as csvfile:
            reader = csv.reader(csvfile)
            for row in reader:
                timestamps.append(int(row[0]))
                values.append(float(row[1]))

        plt.plot(timestamps, values)
        plt.title(title)
        plt.xlabel('Timestamp')
        plt.ylabel('Value')
        plt.savefig(output_plot)
        plt.close()
        print(f"Plot saved as {output_plot}")

    except FileNotFoundError:
        print(f"Error: The file '{input_file}' does not exist.")
    except Exception as e:
        print(f"Error: {e}")

def save_measurement_to_csv(measurement, output_file):
    try:
        with open(output_file, 'a', newline='') as csvfile:
            csv_writer = csv.writer(csvfile)
            csv_writer.writerow([time.time(), measurement])
        print(f"Measurement saved to {output_file}")
    except Exception as e:
        print(f"Error while saving measurement: {e}")

# Define URLs and output files
heart_rate_url_csv = 'http://192.168.105.245/heart_rate'
temperature_url_csv = 'http://192.168.105.245/temperature'
heart_rate_output_file = 'heart_rate.csv'
temperature_output_file = 'temperature.csv'
heart_rate_plot_file = 'heart_rate_plot.png'
temperature_plot_file = 'temperature_plot.png'
bpm_output_file = 'bpm_measurements.csv'

# Run the data fetching and plotting in a loop
interval = 10
while True:
    # Fetch heart rate data
    fetch_csv_data(heart_rate_url_csv, heart_rate_output_file)

    # Plot heart rate over time
    plot_csv_data(heart_rate_output_file, heart_rate_plot_file, 'Heart Rate Over Time')

    # Fetch temperature data
    fetch_csv_data(temperature_url_csv, temperature_output_file)

    # Plot temperature over time
    plot_csv_data(temperature_output_file, temperature_plot_file, 'Temperature Over Time')

    # Sleep for a while
    time.sleep(interval)
