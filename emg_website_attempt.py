import os
import requests
import csv
from io import StringIO
import time
import matplotlib.pyplot as plt
import pandas as pd

def fetch_csv_data(url_csv, output_file):
    try:
        response_csv = requests.get(url_csv)
        if response_csv.status_code == 200:
            csv_data = StringIO(response_csv.text)
            with open(output_file, 'a', newline='') as csvfile:  # Open file in append mode
                csvfile.write(response_csv.text)
            print(f"Data has been successfully appended to {output_file}")
        else:
            print(f"Error: Unable to fetch CSV data from {url_csv}. Status code: {response_csv.status_code}")
    except requests.ConnectionError:
        print(f"Error: Unable to establish connection to the server at {url_csv}.")
    except requests.RequestException as e:
        print(f"Error: {e}")

# Function to get user input for name and exercise
def get_user_input():
    name = input("Enter your name: ")
    exercise = input("Enter the exercise: ")
    return name, exercise

# Function to plot EMG data
def plot_emg_data(input_file, output_png):
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
            plt.savefig(output_png)
            plt.close()
            print(f"PNG file {output_png} updated.")

        else:
            print("Error: No data found in the CSV file.")
    except FileNotFoundError:
        print(f"Error: The file '{input_file}' does not exist.")
    except Exception as e:
        print(f"Error: {e}")

# Set base URLs and output folder
base_url = 'http://192.168.196.245/'
data_types = ['heart_rate', 'temperature', 'emg_data', 'gps_data']

# Set interval for fetching data (in seconds)
interval = 2

# Get user input for name and exercise
name, exercise = get_user_input()
user_folder = os.path.join('data', name)
exercise_folder = os.path.join(user_folder, exercise)

if not os.path.exists(exercise_folder):
    os.makedirs(exercise_folder, exist_ok=True)

# Run the data fetching and plotting in a loop
while True:
    for data_type in data_types:
        url_csv = f"{base_url}{data_type}"
        output_file = os.path.join(exercise_folder, f"{data_type}_{name}_{exercise}.csv")
        fetch_csv_data(url_csv, output_file)
        
    # Plot EMG data
    emg_data_file = os.path.join(exercise_folder, f"emg_data_{name}_{exercise}.csv")
    output_png = os.path.join(exercise_folder, f"emg_plot_{name}_{exercise}.png")
    plot_emg_data(emg_data_file, output_png)
    
    # Wait for the specified interval
    time.sleep(interval)
