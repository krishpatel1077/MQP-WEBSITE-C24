import requests
import csv
from io import StringIO
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import time

# Define the IP address and data URLs
ip_address = '192.168.196.245'
emg_data_url = f'http://{ip_address}/emg_data'
heart_rate_data_url = f'http://{ip_address}/heart_rate'
temperature_data_url = f'http://{ip_address}/temperature.csv'
gps_data_url = f'http://{ip_address}/gps_data.csv'

def fetch_csv_data(url_csv, output_file):
    try:
        response_csv = requests.get(url_csv)
        if response_csv.status_code == 200:
            with open(output_file, 'w', newline='') as f:
                f.write(response_csv.text)
            print(f"Data has been successfully written to {output_file}")
            return True
        else:
            print(f"Error: Unable to fetch CSV data. Status code: {response_csv.status_code}")
    except requests.ConnectionError:
        print("Error: Unable to establish connection to the server.")
    except requests.RequestException as e:
        print(f"Error: {e}")
    return False

def calculate_running_average(data):
    return np.mean(data)

def plot_emg_data(input_file, output_html_prefix):
    try:
        df = pd.read_csv(input_file, header=None)
        if df.shape[1] > 1:  # Check if there are columns in the DataFrame
            timestamps = df.iloc[:, 0]
            emg_columns = df.iloc[:, 1:]

            num_plots = emg_columns.shape[1]

            # Initialize figure and axes for plots
            fig, axes = plt.subplots(nrows=num_plots, ncols=1, figsize=(10, 10))
            fig.suptitle('EMG Data')

            for i in range(num_plots):
                emg_data = emg_columns.iloc[:, i]

                # Plot raw EMG
                axes[i].plot(timestamps, emg_data)
                axes[i].set_title(f'EMG {i+1}')
                axes[i].set_xlabel('Time')
                axes[i].set_ylabel('Value')

            plt.tight_layout()
            plt.savefig(f'{output_html_prefix}_emg.png')
            plt.close()

            # Embed the plots in HTML
            with open(f"{output_html_prefix}_emg.html", "w") as html_file:
                html_file.write(f"<html><head>\n")
                html_file.write(f"<meta http-equiv=\"refresh\" content=\"2\">\n")
                html_file.write(f"</head><body>\n")
                html_file.write(f"<h1>EMG Data</h1>\n")
                html_file.write(f'<img src="{output_html_prefix}_emg.png" alt="EMG Plots">\n')
                html_file.write(f"</body></html>\n")
                print(f"EMG HTML file {output_html_prefix}_emg.html created.")

        else:
            print("Error: No data found in the CSV file.")
    except FileNotFoundError:
        print(f"Error: The file '{input_file}' does not exist.")
    except Exception as e:
        print(f"Error: {e}")

def plot_heart_rate_data(input_file, output_html_prefix):
    try:
        df = pd.read_csv(input_file, header=None)
        if df.shape[1] > 1:  # Check if there are columns in the DataFrame
            timestamps = df.iloc[:, 0]
            heart_rate = df.iloc[:, 1]

            plt.plot(timestamps, heart_rate)
            plt.title('Heart Rate Data')
            plt.xlabel('Time')
            plt.ylabel('Heart Rate (BPM)')
            plt.tight_layout()
            plt.savefig(f'{output_html_prefix}_heart_rate.png')
            plt.close()

            # Embed the plot in HTML
            with open(f"{output_html_prefix}_heart_rate.html", "w") as html_file:
                html_file.write(f"<html><head>\n")
                html_file.write(f"<meta http-equiv=\"refresh\" content=\"2\">\n")
                html_file.write(f"</head><body>\n")
                html_file.write(f"<h1>Heart Rate Data</h1>\n")
                html_file.write(f'<img src="{output_html_prefix}_heart_rate.png" alt="Heart Rate Plot">\n')
                html_file.write(f"</body></html>\n")
                print(f"Heart Rate HTML file {output_html_prefix}_heart_rate.html created.")

        else:
            print("Error: No data found in the CSV file.")
    except FileNotFoundError:
        print(f"Error: The file '{input_file}' does not exist.")
    except Exception as e:
        print(f"Error: {e}")

def generate_html(emg_html_prefix, heart_rate_html_prefix, temperature_avg, velocity_avg, bpm_avg, rsp_rate_1, rsp_rate_2):
    html_code = f"""
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Data Plots</title>
    <style>
        body {{
            margin: 0;
            padding: 0;
            background-color: #f0f0f0;
            font-family: Arial, sans-serif;
            color: #333;
            display: flex;
            flex-wrap: wrap;
            justify-content: center;
        }}

        .section {{
            background-color: #293241;
            border-radius: 10px;
            box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
            padding: 20px;
            margin: 20px;
            width: 100%;
            max-width: 800px;
        }}

        h1, h2, h3, p {{
            color: #fff;
            text-align: center;
        }}

        img {{
            width: 100%;
            height: auto;
            display: block;
            margin: auto;
            border-radius: 10px;
            box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
        }}

        .data {{
            font-size: 28px;
            margin-top: 20px;
            text-align: center;
        }}

        .row {{
            display: flex;
            flex-wrap: wrap;
            justify-content: center;
            align-items: center;
            margin-bottom: 30px;
        }}

        .col {{
            flex-grow: 1;
            text-align: center;
            padding: 20px;
            max-width: 400px;
        }}
        
        .col.rsp {{
            flex-basis: 50%;
            max-width: 100%;
        }}
    </style>
</head>
<body>
    <div class="section">
        <h1>EMG Signals</h1>
        <img src="{emg_html_prefix}_emg.png" alt="EMG Plots">
    </div>
    <div class="section">
        <h1>Heart Rate</h1>
        <img src="{heart_rate_html_prefix}_heart_rate.png" alt="Heart Rate Plot">
    </div>
    <div class="section">
        <h1>Biometrics</h1>
        <h2>Average Velocity: <h2/>
        <h2 class="data">{velocity_avg:.2f} m/s</h2>
        <h2>Average Temperature: </h2>
        <h2 class="data">{temperature_avg:.2f} °C</h2>
        <h2>Average BPM: </h2>
        <h2 class="data">{bpm_avg:.2f} BPM</h2>
    </div>
    <div class="section">
        <h2>Respiratory Rate Graphs</h2>
        <div class="row">
            <div class="col rsp">
                <h3>Respiratory Rate 1</h3>
                <img src="{rsp_rate_1}.png" alt="Respiratory Rate 1">
            </div>
            <div class="col rsp">
                <h3>Respiratory Rate 2</h3>
                <img src="{rsp_rate_2}.png" alt="Respiratory Rate 2">
            </div>
        </div>
    </div>
</body>
</html>
"""

    with open('final.html', 'w') as html_file:
        html_file.write(html_code)
        print("HTML file final.html created.")


def calculate_running_average(data):
    return np.mean(data)

def main():
    temperature_values = []
    velocity_values = []
    bpm_values = []

    # Initial fetch
    # fetch_csv_data(emg_data_url, 'emg_data.csv')
    # fetch_csv_data(heart_rate_data_url, 'heart_rate.csv')

    while True:
        # Fetch EMG and heart rate data
        # fetch_csv_data(emg_data_url, 'emg_data.csv')
        # fetch_csv_data(heart_rate_data_url, 'heart_rate.csv')

        # # Fetch temperature and GPS data
        # fetch_csv_data(temperature_data_url, 'temperature.csv')
        # fetch_csv_data(gps_data_url, 'gps_data.csv')

        # Calculate running averages for temperature, velocity, and BPM
        temperature_data = pd.read_csv('temperature.csv')
        temperature_values.append(temperature_data.iloc[-1][0])  # Add the latest temperature value
        temperature_avg = calculate_running_average(temperature_values)

        gps_data = pd.read_csv('gps_data.csv', header=None)
        velocity_values.append(gps_data.iloc[-1][3])  # Add the latest velocity value
        velocity_avg = calculate_running_average(velocity_values)

        heart_rate_data = pd.read_csv('heart_rate.csv', header=None)
        bpm_values.append(heart_rate_data.iloc[-1][1])  # Add the latest BPM value
        bpm_avg = calculate_running_average(bpm_values)

        # Plot EMG data
        plot_emg_data('emg_data.csv', 'emg')

        # Plot heart rate data
        plot_heart_rate_data('heart_rate.csv', 'heart_rate')

        # Calculate respiratory rate
        respiratory_rate_data = pd.read_csv('heart_rate.csv', header=None)
        rsp_rate_1, rsp_rate_2 = "edr_signal_resp", "rsp_rate_resp"  # Placeholder filenames for respiratory rate graphs

        # Generate HTML with updated running averages and graphs
        generate_html('emg', 'heart_rate', temperature_avg, velocity_avg, bpm_avg, rsp_rate_1, rsp_rate_2)

        # Sleep for a while
        time.sleep(2)

if __name__ == "__main__":
    main()
