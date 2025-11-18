import pandas as pd
import requests
import io
import plotly.express as px

DATASET_URl="https://raw.githubusercontent.com/maksim-sergienko/data-source/refs/heads/main/jupyter/{{DATASET_ID}}.csv"

print("Notebook for: {{DATASET_NAME}} ({{DATASET_ID}})")

def render_csv_from_url(url, x_col=None, y_col=None):
    try:
        response = requests.get(url)
        response.raise_for_status()
        csv_data = response.content
        df = pd.read_csv(io.StringIO(csv_data.decode('utf-8')))

        display(df)

        if x_col and y_col:
            if x_col in df.columns and y_col in df.columns:
                print(f"Generating a scatter plot with x='{x_col}' and y='{y_col}'...")
                fig = px.scatter(df, x=x_col, y=y_col)
                fig.show()
            else:
                print(f"Error: One or both specified columns ('{x_col}', '{y_col}') not in dataframe.")
        elif df.shape[1] >= 2:
            print("Generating a scatter plot with the first two columns...")
            fig = px.scatter(df, x=df.columns[0], y=df.columns[1])
            fig.show()

    except requests.exceptions.RequestException as e:
        print(f"Error downloading the CSV file: {e}")
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    render_csv_from_url(DATASET_URl)
