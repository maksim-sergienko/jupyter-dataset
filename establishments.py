import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Column names for the dataset
column_names = ['month_year', 'establishments']

try:
    # Load the dataset from the URL, skipping the header row
    df = pd.read_csv("1.csv", skiprows=1, names=column_names)
    print(f"✅ Dataset loaded from URL: 1.csv")

    # Convert 'month_year' to datetime objects
    df['date'] = pd.to_datetime(df['month_year'], format='%m-%Y')

    # Sort the dataframe by date
    df = df.sort_values(by='date')

    # Create a line chart
    plt.figure(figsize=(12, 7))
    sns.lineplot(x='date', y='establishments', data=df, marker='o')
    plt.title('Number of Establishments Over Time')
    plt.xlabel('Date')
    plt.ylabel('Number of Establishments')
    plt.grid(True)
    plt.xticks(rotation=45)
    plt.tight_layout()

    plt.show()
except Exception as e:
    print(f"⚠️ Failed to load or process dataset: {e}")
