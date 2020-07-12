from sklearn.cluster import KMeans
from sklearn.preprocessing import MinMaxScaler
import numpy as np
import pandas as pd
def do_k_means(do_std:bool, file_path:str, attribute_list:list, num_of_cluster:int=2, max_iter:int=300, random_state:int=0, save_path:str="./"):
    df = pd.read_csv(file_path)
    X = df[attribute_list].values
    if do_std:
        scaler = MinMaxScaler()
        scaler.fit(X)
        X = scaler.transform(X)

    kmeans = KMeans(n_clusters=num_of_cluster, max_iter=max_iter, random_state=random_state).fit(X)

    df_std = pd.DataFrame(X, index=None, columns=["transaction_count", "transaction_per_day", "time_interval_mean(min)", "time_interval_median(min)", "time_interval_std(min)", "send_count", "receive_count", "send_value_mean(eth)", "receive_value_mean(eth)", "average_gas"])
    df_std.to_csv(save_path[:-4]+"_td.csv")

    df["transaction_interval_cluster_label"] = kmeans.labels_
    print(df["transaction_interval_cluster_label"].value_counts())
    df.to_csv(save_path)
    print(kmeans.cluster_centers_)

def encode_category(file_path:str, save_path:str):
    
    return

if __name__ == '__main__':
    # all_attr_list = ["address", "source", "transaction_count", "transaction_per_day", "time_interval_mean(min)", "time_interval_median(min)", "time_interval_std(min)", "from_cate", "to_cate", "from_title", "to_title", "send_count", "receive_count", "send_value_mean(eth)", "receive_value_mean(eth)", "value_dict(eth)", "average_gas", "first_date", "app_sequence"]
    num_attr_list = ["transaction_count", "transaction_per_day", "time_interval_mean(min)", "time_interval_median(min)", "time_interval_std(min)", "send_count", "receive_count", "send_value_mean(eth)", "receive_value_mean(eth)", "average_gas"]
    time_attr_list = ["transaction_count", "transaction_per_day", "time_interval_mean(min)", "time_interval_median(min)", "time_interval_std(min)"]
    do_k_means(True, "./transaction/profiled/sum.csv", num_attr_list, 3, 15000, 0, "./further_mined_sum.csv")