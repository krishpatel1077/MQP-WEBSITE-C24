import requests
import csv
from io import StringIO
import matplotlib.pyplot as plt
import time
import neurokit2 as nk
import pandas as pd

def fetch_csv_data(url_csv, output_file):
    try:
        response_csv = requests.get(url_csv)
        if response_csv.status_code == 200:
            csv_data = StringIO(response_csv.text)
            reader = csv.reader(csv_data)
            with open(output_file, 'a', newline='') as csvfile:
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

def plot_csv_data(input_file, plot_number, bpm, max_points=1000):
    timestamps = []
    heart_rates = []
    try:
        with open(input_file, 'r') as csvfile:
            reader = csv.reader(csvfile)
            for row in reader:
                timestamps.append(int(row[0]))
                heart_rates.append(float(row[1]))

        if len(timestamps) > max_points:
            timestamps = timestamps[-max_points:]
            heart_rates = heart_rates[-max_points:]

        plt.close()
        plt.plot(timestamps, heart_rates, linestyle='-')
        plt.title(f'Heart Rate Over Time - BPM: {bpm.mean()}')
        plt.xlabel('Timestamp (ms)')
        plt.ylabel('ECG')
        plt.text(timestamps[-1], heart_rates[-1], f'BPM: {bpm.mean()}', ha='right', va='bottom', color='red')
        plt.savefig(f'plot.png')
        print(f"Plot saved as plot.png")
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
        <title>Heart Rate Plot</title>
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
        <img src="plot.png" alt="Heart Rate Plot">
    </body>
    </html>
    """

    with open('index.html', 'w') as html_file:
        html_file.write(html_code)

def save_bpm_to_csv(bpm, output_file):
    try:
        with open(output_file, 'a', newline='') as csvfile:
            csv_writer = csv.writer(csvfile)
            csv_writer.writerow([time.time(), bpm.mean()])
        print(f"BPM measurements saved to {output_file}")
    except Exception as e:
        print(f"Error: {e}")

url_csv = 'http://192.168.105.245/heart_rate'
output_file = 'heart_rate.csv'
bpm_output_file = 'bpm_measurements.csv'
input_file = 'heart_rate.csv'
sampling_rate = 75

interval = 2
initial_csv = requests.get(url_csv)
while True:
    fetch_csv_data(url_csv, output_file)
    data = pd.read_csv(output_file, header=None)
    data.columns = ["Time", "ECG"]
    r_peaks = nk.ecg_findpeaks(data["ECG"], sampling_rate=sampling_rate)
    bpm = nk.ecg_rate(r_peaks, sampling_rate=sampling_rate, desired_length=len(data))
    plot_csv_data(input_file, 2, bpm)
    generate_html()
    save_bpm_to_csv(bpm, bpm_output_file)
    time.sleep(interval)
