import requests
import csv
from io import StringIO
import matplotlib.pyplot as plt
import pandas as pd
import time

# Define the IP address and EMG data URL
ip_address = '192.168.105.245'
emg_data_url = f'http://{ip_address}/emg_data'

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
            plt.savefig(f'{output_html_prefix}.png')
            plt.close()

            # Embed the plots in HTML
            with open(f"{output_html_prefix}.html", "w") as html_file:
                html_file.write(f"<html><head>\n")
                html_file.write(f"<meta http-equiv=\"refresh\" content=\"2\">\n")
                html_file.write(f"</head><body>\n")
                html_file.write(f"<h1>EMG Data</h1>\n")
                html_file.write(f'<img src="{output_html_prefix}.png" alt="EMG Plots">\n')
                html_file.write(f"</body></html>\n")
                print(f"HTML file {output_html_prefix}.html created.")

        else:
            print("Error: No data found in the CSV file.")
    except FileNotFoundError:
        print(f"Error: The file '{input_file}' does not exist.")
    except Exception as e:
        print(f"Error: {e}")

# Define output HTML file prefix
emg_html_prefix = 'emg'

# Run the data fetching and plotting in a loop
interval = 2
while True:
    # Fetch EMG data
    if fetch_csv_data(emg_data_url, 'emg_data.csv'):
        # Plot EMG data and save to HTML
        plot_emg_data('emg_data.csv', emg_html_prefix)

    # Sleep for a while
    time.sleep(interval)
