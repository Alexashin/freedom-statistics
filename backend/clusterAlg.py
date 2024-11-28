import pandas as pd
from sklearn.cluster import KMeans
import matplotlib.pyplot as plt


def clusterAlgGetResult():
        # Данные о пользователях
    data = {
        "Тариф": [0, 1, 2],  # 0 = Эконом, 1 = Стандарт, 2 = Премиум
        "Часы просмотра": [10, 20, 15],
        "Каналы": [5, 12, 10],
        "Спорт (%)": [10, 30, 5],
        "Новости (%)": [50, 20, 15],
        "Фильмы (%)": [30, 40, 60],
        "Сериалы (%)": [10, 10, 20]
    }

    df = pd.DataFrame(data)

    # Кластеризация
    kmeans = KMeans(n_clusters=3, random_state=42)
    df["Кластер"] = kmeans.fit_predict(df)

    print(df)

    
    return kmeans;