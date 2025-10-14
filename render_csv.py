import pandas as pd
import requests
import io


DATASET_URl="https://raw.githubusercontent.com/maksim-sergienko/data-source/refs/heads/main/jupyter/3.csv"

def render_csv_from_url(url):
    try:
        response = requests.get(url)
        response.raise_for_status()  # Raise an exception for bad status codes
        csv_data = response.content
        df = pd.read_csv(io.StringIO(csv_data.decode('utf-8')))

        df.head()


    except requests.exceptions.RequestException as e:
        print(f"Error downloading the CSV file: {e}")
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    render_csv_from_url(DATASET_URl)
