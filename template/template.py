import pandas as pd
import requests
import io


print("Notebook for: {{DATASET_NAME}} ({{DATASET_ID}})")
print("Description: {{DESCRIPTION}}")

DATASET_URl="{{DATASET_URL}}"


def render_csv_from_url(url):
    try:
        response = requests.get(url)
        response.raise_for_status()
        csv_data = response.content
        df = pd.read_csv(io.StringIO(csv_data.decode('utf-8')))

        display(df)

    except requests.exceptions.RequestException as e:
        print(f"Error downloading the CSV file: {e}")
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    render_csv_from_url(DATASET_URl)
