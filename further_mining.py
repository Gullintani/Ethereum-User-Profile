from sklearn.cluster import KMeans
import numpy as np
import pandas as pd
def do_k_means(file_path:str, attribute_list:list, num_of_cluster:int=2, max_iter:int=300, random_state:int=0, save_path:str="./"):
    df = pd.read_csv(file_path)
    X = df[attribute_list].values
    kmeans = KMeans(n_clusters=num_of_cluster, max_iter=max_iter, random_state=random_state).fit(X)
    
    df["transaction_interval_cluster_label"] = kmeans.labels_
    print(df["transaction_interval_cluster_label"].value_counts())
    df.to_csv(save_path)
    print(kmeans.cluster_centers_)


if __name__ == '__main__':
    do_k_means("./transaction/profiled/CryptokittySiringAuction4000.csv", ["transaction_count", "transaction_per_day", "time_interval_mean(min)", "time_interval_median(min)", "time_interval_std(min)"], 3, 5000, 0, "./CryptokittySiringAuction4000_further_mined.csv")