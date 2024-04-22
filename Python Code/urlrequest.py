import requests
import csv
from io import StringIO

# Replace 'http://192.168.1.4/data.csv' with the actual URL of the CSV file
url_csv = 'http://192.168.116.245/heart_rate'
output_file = 'heart_rate.csv'

try:
    # Make a GET request to the specified CSV file URL
    response_csv = requests.get(url_csv)

    # Check if the request was successful (status code 200)
    if response_csv.status_code == 200:
        # Use StringIO to create a file-like object for CSV parsing
        csv_data = StringIO(response_csv.text)

        # Use the CSV module to read the data
        reader = csv.reader(csv_data)

        # Open a new CSV file for writing
        with open(output_file, 'w', newline='') as csvfile:
            # Create a CSV writer object
            csv_writer = csv.writer(csvfile)

            # Iterate through rows and write the data to the new file
            for row in reader:
                csv_writer.writerow(row)

        print(f"Data has been successfully written to {output_file}")
    else:
        print(f"Error: Unable to fetch CSV data. Status code: {response_csv.status_code}")

except requests.ConnectionError:
    print("Error: Unable to establish connection to the server.")
except requests.RequestException as e:
    print(f"Error: {e}")
