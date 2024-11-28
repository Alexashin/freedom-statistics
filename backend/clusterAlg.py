import pandas as pd
from sklearn.cluster import KMeans
import matplotlib.pyplot as plt


def clusterAlgGetResult(data):

    df = pd.DataFrame(data)

    kmeans = KMeans(n_clusters=3, random_state=42)
    df["Кластер"] = kmeans.fit_predict(df)

    print(df)
    return kmeans