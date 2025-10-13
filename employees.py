import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

def plot_employees_by_sector(language='en'):
    column_names = ['CHAPTER', 'SECTOREN', 'SECTORAR', 'NOOFEMPLOYEE', 'ACTIVITYTYPE']
    data_url = "3.csv"

    try:
        df = pd.read_csv(data_url, skiprows=1, names=column_names)
        print(f"✅ Dataset loaded from URL: {data_url}")

        if language == 'en':
            sector_column = 'SECTOREN'
            title_prefix = 'Number of Employees by Sector (English)'
            xlabel = 'Sector (English)'
        elif language == 'ar':
            sector_column = 'SECTORAR'
            title_prefix = 'Number of Employees by Sector (Arabic)'
            xlabel = 'Sector (Arabic)'
        else:
            print("⚠️ Invalid language selected. Using English by default.")
            sector_column = 'SECTOREN'
            title_prefix = 'Number of Employees by Sector (English)'
            xlabel = 'Sector (English)'

        employees_by_sector = df.groupby(sector_column)['NOOFEMPLOYEE'].sum().reset_index()

        employees_by_sector = employees_by_sector.sort_values(by='NOOFEMPLOYEE', ascending=False)

        plt.figure(figsize=(14, 8))
        sns.barplot(x=sector_column, y='NOOFEMPLOYEE', data=employees_by_sector, palette='viridis')
        plt.title(title_prefix)
        plt.xlabel(xlabel)
        plt.ylabel('Number of Employees')
        plt.xticks(rotation=90)
        plt.tight_layout()

        plt.show()
    except Exception as e:
        print(f"⚠️ Failed to load or process dataset: {e}")

if __name__ == "__main__":
    print("Select language for the chart:")
    print("1. English (en)")
    print("2. Arabic (ar)")
    choice = input("Enter your choice (1 or 2): ")

    if choice == '1':
        plot_employees_by_sector(language='en')
    elif choice == '2':
        plot_employees_by_sector(language='ar')
    else:
        print("Invalid choice. Plotting in English by default.")
        plot_employees_by_sector(language='en')
