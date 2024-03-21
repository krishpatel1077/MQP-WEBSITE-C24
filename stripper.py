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
# Define URLs and output files
heart_rate_url_csv = 'http://192.168.196.245/heart_rate'
temperature_url_csv = 'http://192.168.196.245/temperature'
emg_data_url_csv = 'http://192.168.196.245/emg_data'
gps_data_url_csv = 'http://192.168.196.245/gps_data'
heart_rate_output_file = 'heart_rate_james_suicides.csv'
temperature_output_file = 'temperature_james_suicides.csv'
emg_data_output_file = 'emg_data_james_suicides.csv'
gps_data_output_file = 'gps_data_james_suicides.csv'
# Set interval for fetching data (in seconds)
interval = 10
# Run the data fetching in a loop
while True:
    # Fetch heart rate data
    fetch_csv_data(heart_rate_url_csv, heart_rate_output_file)
    # Fetch temperature data
    fetch_csv_data(temperature_url_csv, temperature_output_file)
    # Fetch EMG data
    fetch_csv_data(emg_data_url_csv, emg_data_output_file)
    # Fetch GPS data
    fetch_csv_data(gps_data_url_csv, gps_data_output_file)
    # Wait for the specified interval
    time.sleep(interval)




