import os
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from urllib.request import urlopen
from dotenv import load_dotenv

# %matplotlib inline

load_dotenv()

data_url = os.getenv("DATA_URL")

print("DATA_URL")
print(data_url)
print("DATA_URL")

column_names = ['sepal_length', 'sepal_width', 'petal_length', 'petal_width', 'class']

try:
    if data_url:
        df = pd.read_csv(data_url, header=None, names=column_names)
        print(f"✅ Dataset loaded from URL: {data_url}")
    else:
        df = pd.read_csv('iris.csv', header=None, names=column_names)
        print("⚙️ Using default iris dataset")
except Exception as e:
    print(f"⚠️ Failed to load dataset: {e}")
    column_names = ['sepal_length', 'sepal_width', 'petal_length', 'petal_width', 'class']
    df = pd.read_csv('iris.csv', header=None, names=column_names)

if df.shape[1] < 5:
    df.columns = ['sepal_length', 'sepal_width', 'petal_length', 'petal_width', 'class']

plt.figure(figsize=(10, 6))
sns.scatterplot(x='sepal_length', y='sepal_width', hue='class', data=df)
plt.title('Sepal Length vs. Sepal Width')
plt.xlabel('Sepal Length')
plt.ylabel('Sepal Width')
plt.grid(True)
plt.show()

plt.figure(figsize=(10, 6))
sns.scatterplot(x='petal_length', y='petal_width', hue='class', data=df)
plt.title('Petal Length vs. Petal Width')
plt.xlabel('Petal Length')
plt.ylabel('Petal Width')
plt.grid(True)
plt.show()
