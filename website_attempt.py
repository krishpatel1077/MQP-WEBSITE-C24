import os
import requests
import csv
from io import StringIO
import time

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

# Set base URLs and output folder
base_url = 'http://192.168.196.245/'
data_types = ['heart_rate', 'temperature', 'emg_data', 'gps_data']

# Set interval for fetching data (in seconds)
interval = 2

# Run the data fetching in a loop
while True:
    name, exercise = get_user_input()
    output_folder = os.path.join('data_', name)
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)
    for data_type in data_types:
        url_csv = f"{base_url}{data_type}"
        output_file = os.path.join(output_folder, f"{data_type}_{name}_{exercise}.csv")
        fetch_csv_data(url_csv, output_file)
    # Wait for the specified interval
    time.sleep(interval)
