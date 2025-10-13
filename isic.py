import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

try:
    # Load the dataset from the CSV file
    df = pd.read_csv("2.csv")
    print(f"✅ Dataset loaded from 2.csv")

    # Group by ISIC4 and sum TotalEmp
    isic_employment = df.groupby('ISIC4')['TotalEmp'].sum().reset_index()

    # Create a bar chart
    plt.figure(figsize=(12, 7))
    sns.barplot(x='TotalEmp', y='ISIC4', data=isic_employment.sort_values('TotalEmp', ascending=False))
    plt.title('Total Employment by ISIC4 Category')
    plt.xlabel('Total Employment')
    plt.ylabel('ISIC4 Category')
    plt.grid(True)
    plt.tight_layout()

    plt.show()
except Exception as e:
    print(f"⚠️ Failed to load or process dataset: {e}")
