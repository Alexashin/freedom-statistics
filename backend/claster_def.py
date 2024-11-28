import pandas as pd
from sklearn.cluster import KMeans
def clasterAlgGetResult(data):

    df = pd.DataFrame(data)

    # Кластеризация
    kmeans = KMeans(n_clusters=3, random_state=42)
    df["Кластер"] = kmeans.fit_predict(df)

    print(df)
    return (data)
