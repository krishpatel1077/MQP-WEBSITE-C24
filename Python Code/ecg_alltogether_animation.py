import requests
import csv
from io import StringIO
import matplotlib.pyplot as plt
import time
import pandas as pd

def fetch_csv_data(url_csv, output_file):
    try:
        response_csv = requests.get(url_csv)
        if response_csv.status_code == 200:
            with open(output_file, 'a', newline='') as csvfile:
                csvfile.write(response_csv.text)
            print(f"Data has been successfully written to {output_file}")
        else:
            print(f"Error: Unable to fetch CSV data. Status code: {response_csv.status_code}")
    except requests.ConnectionError:
        print("Error: Unable to establish connection to the server.")
    except requests.RequestException as e:
        print(f"Error: {e}")

def plot_csv_data(input_file, plot_number, max_points=1000):
    timestamps = []
    emg_data = [[] for _ in range(3)]  # Create empty lists for each EMG sensor
    try:
        with open(input_file, 'r') as csvfile:
            reader = csv.reader(csvfile)
            for row in reader:
                timestamps.append(int(row[0]))
                for i in range(1, len(row)):  # Skip the first column (time)
                    emg_data[i - 1].append(float(row[i]))

        if len(timestamps) > max_points:
            timestamps = timestamps[-max_points:]
            emg_data = [sensor[-max_points:] for sensor in emg_data]

        plt.close()
        for i, sensor_data in enumerate(emg_data, start=1):
            plt.plot(timestamps, sensor_data, linestyle='-', label=f'EMG {i}')

        plt.title(f'EMG Data Plot {plot_number}')
        plt.xlabel('Timestamp (ms)')
        plt.ylabel('Value')
        plt.legend()
        plt.savefig(f'plot{plot_number}.png')
        print(f"Plot saved as plot{plot_number}.png")
    except FileNotFoundError:
        print(f"Error: The file '{input_file}' does not exist.")
    except Exception as e:
        print(f"Error: {e}")

def generate_html():
    html_code = """
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta http-equiv="refresh" content="10">
        <title>Data Plots</title>
        <style>
            body {
                margin: 0;
                padding: 0;
                display: flex;
                align-items: center;
                justify-content: center;
                height: 100vh;
                background-color: #f4f4f4;
                overflow: hidden;
            }
            img {
                width: 100%;
                height: 100%;
            }
        </style>
    </head>
    <body>
        <img src="plot1.png" alt="Plot 1">
        <img src="plot2.png" alt="Plot 2">
        <img src="plot3.png" alt="Plot 3">
    </body>
    </html>
    """

    with open('index.html', 'w') as html_file:
        html_file.write(html_code)

url_csv_heart_rate = 'http://192.168.105.245/heart_rate'
url_csv_emg = 'http://192.168.105.245/emg_data_jennifer_20pass.csv'
output_file_heart_rate = 'heart_rate.csv'
output_file_emg = 'emg_data.csv'
sampling_rate = 75

interval = 2

# Initial fetch
initial_csv_heart_rate = requests.get(url_csv_heart_rate)
initial_csv_emg = requests.get(url_csv_emg)

while True:
    fetch_csv_data(url_csv_heart_rate, output_file_heart_rate)
    fetch_csv_data(url_csv_emg, output_file_emg)

    plot_csv_data(output_file_heart_rate, 1)
    plot_csv_data(output_file_emg, 2)

    generate_html()

    time.sleep(interval)
