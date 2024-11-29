import os
import psycopg2
import pandas as pd
from dotenv import load_dotenv
from sklearn.preprocessing import StandardScaler
from sklearn.cluster import MiniBatchKMeans
import numpy as np

# Загрузка переменных окружения из файла .env
load_dotenv()

DB_SETTINGS = {
    'dbname': os.getenv('DB_NAME'),
    'user': os.getenv('DB_USER'),
    'password': os.getenv('DB_PASSWORD'),
    'host': os.getenv('DB_HOST'),
    'port': os.getenv('DB_PORT')
}

# Функция для подключения к базе данных
def get_connection():
    try:
        conn = psycopg2.connect(**DB_SETTINGS)
        return conn
    except Exception as e:
        print(f"Ошибка подключения к базе данных: {e}")
        return None

# Шаг 1: Извлечение данных из базы данных
def extract_data(conn):
    try:
        query = """
        SELECT 
            c.client_id,
            c.gender,
            c.age_range,
            e.category,
            e.subcategory,
            SUM(e.duration) as total_duration
        FROM client c
        JOIN epg_stat e ON c.client_id = e.client_id
        GROUP BY c.client_id, c.gender, c.age_range, e.category, e.subcategory
        """
        df = pd.read_sql(query, conn)
        return df
    except Exception as e:
        print(f"Ошибка при извлечении данных: {e}")
        return None

# Шаг 2: Предобработка данных
def preprocess_data(df):
    # Заполняем пропущенные значения
    df['category'] = df['category'].fillna('Unknown')
    df['subcategory'] = df['subcategory'].fillna('Unknown')
    df['gender'] = df['gender'].fillna('U')  # U - Unknown
    df['age_range'] = df['age_range'].fillna('Unknown')

    # Создаем уникальный идентификатор для каждой категории и подкатегории
    df['category_subcategory'] = df['category'] + ' - ' + df['subcategory']

    # Создаем сводную таблицу с пользователями и их предпочтениями
    df_pivot = df.pivot_table(
        index=['client_id', 'gender', 'age_range'],
        columns='category_subcategory',
        values='total_duration',
        aggfunc='sum',
        fill_value=0
    ).reset_index()

    # Сохраняем client_id для последующего использования
    client_ids = df_pivot['client_id']

    # Преобразуем категориальные переменные (gender, age_range) в числовые
    df_features = pd.get_dummies(df_pivot, columns=['gender', 'age_range'])

    # Масштабируем признаки, исключая 'client_id'
    features_to_scale = df_features.drop(columns=['client_id'])
    scaler = StandardScaler()
    df_scaled = scaler.fit_transform(features_to_scale)

    # Возвращаем DataFrame с 'client_id' для дальнейшего использования
    return df_scaled, client_ids, df_features

# Шаг 3: Кластеризация
def perform_clustering(df_scaled, n_clusters=5):
    minibatch_kmeans = MiniBatchKMeans(n_clusters=n_clusters, random_state=42, batch_size=1000)
    minibatch_kmeans.fit(df_scaled)
    labels = minibatch_kmeans.labels_
    return labels

# Шаг 4: Вывод результатов
def print_clusters(labels, client_ids, df_features):
    clusters = {}
    for client_id, label in zip(client_ids, labels):
        clusters.setdefault(label, []).append(client_id)

    for cluster_id, clients in clusters.items():
        print(f"\nКластер {cluster_id}: {len(clients)} пользователей")
        cluster_data = df_features[df_features['client_id'].isin(clients)]

        # Вычисляем среднее время просмотра по категориям
        category_columns = [col for col in cluster_data.columns if col not in ['client_id']]
        avg_preferences = cluster_data[category_columns].mean().sort_values(ascending=False)

        print("Наиболее популярные категории и подкатегории в этом кластере:")
        print(avg_preferences.head(5))
        print(f"Первые 10 client_id: {clients[:10]}")

def main():
    conn = get_connection()
    if not conn:
        return

    try:
        # Извлечение данных
        df = extract_data(conn)
        if df is None or df.empty:
            print("Нет данных для обработки.")
            return

        # Предобработка данных
        df_scaled, client_ids, df_features = preprocess_data(df)

        # Кластеризация
        labels = perform_clustering(df_scaled, n_clusters=5)

        # Вывод результатов
        print_clusters(labels, client_ids, df_features)

    finally:
        conn.close()
        print("Соединение с базой данных закрыто.")

if __name__ == '__main__':
    main()
