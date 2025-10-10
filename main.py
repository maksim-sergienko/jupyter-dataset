import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

def create_chart():
    # Загружаем датасет
    column_names = ['sepal_length', 'sepal_width', 'petal_length', 'petal_width', 'class']
    df = pd.read_csv('iris.csv', header=None, names=column_names)

    # Настройка для отображения графиков в Jupyter
    %matplotlib inline
    plt.figure(figsize=(10, 6))

    # Создаём scatter plot
    sns.scatterplot(x='sepal_length', y='sepal_width', hue='class', data=df)
    plt.title('Sepal Length vs. Sepal Width')
    plt.xlabel('Sepal Length')
    plt.ylabel('Sepal Width')
    plt.legend()
    plt.grid(True)

    # Показываем график прямо в ноутбуке
    plt.show()

    # Опционально: сохраняем график в файл
    plt.savefig('chart.png')
    print("Chart saved as chart.png")

# Для запуска в ячейке Jupyter просто вызови функцию:
create_chart()
