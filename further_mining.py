from sklearn.cluster import KMeans
from sklearn.neighbors import KNeighborsClassifier
from sklearn.preprocessing import MinMaxScaler
from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import KernelPCA
import numpy as np
import pandas as pd
def do_k_means(file_path:str, attribute_list:list, num_of_cluster:int=2, max_iter:int=300, random_state:int=0, save_path:str="./"):
    df = pd.read_csv(file_path)
    X = df[attribute_list].values

    kmeans = KMeans(n_clusters=num_of_cluster, max_iter=max_iter, random_state=random_state).fit(X)

    df["cluster_label"] = kmeans.labels_
    print(df["cluster_label"].value_counts())
    df.to_csv(save_path)
    print(kmeans.cluster_centers_)

def do_knn():
    return

def cluster_preprocessing(file_path:str, save_path:str, pca_component:int):
    # category_list = ['self', 'nan', 'defi', 'exchanges', 'other', 'gambling', 'games', 'marketplaces', 'social', 'high-risk', 'collectibles']
    num_attr_list = ["transaction_count", "transaction_per_day", "time_interval_mean(min)", "time_interval_median(min)", "time_interval_std(min)", "send_count", "receive_count", "send_value_mean(eth)", "receive_value_mean(eth)", "average_gas"]
    new_columns_list = ["self_count", "nan_count", "defi_count", "exchanges_count", "other_count", "gambling_count", "games_count", "marketplaces_count", "social_count", "high-risk_count", "collectibles_count", "self_value", "nan_value", "defi_value", "exchanges_value", "other_value", "gambling_value", "games_value", "marketplaces_value", "social_value", "high-risk_value", "collectibles_value"]
    df = pd.read_csv(file_path)
    for attribute in new_columns_list:
        df[attribute] = 0
    total_row = len(df)
    for index, row in df.iterrows():
        to_cate_dict = eval(row["to_cate"])
        value_dict = eval(row["value_dict(eth)"])
        for key, value in to_cate_dict.items():
            df.loc[index, key+"_count"] = value
        for key, value in value_dict.items():
            df.loc[index, key+"_value"] = value
        print(f"{ index }/{ total_row } processed")
    df = df.drop(["Unnamed: 0"], axis=1)
    df.to_csv(save_path)
    
    X = df[num_attr_list + new_columns_list].values
    scaler = MinMaxScaler()
    scaler.fit(X)
    X_nor = scaler.transform(X)
    df_nor = pd.DataFrame(X_nor, index=None, columns= num_attr_list + new_columns_list)
    df_nor.to_csv(save_path[:-4]+"_nor.csv")

    scaler = StandardScaler()
    scaler.fit(X)
    X_std = scaler.transform(X)
    df_std = pd.DataFrame(X_std, index=None, columns= num_attr_list + new_columns_list)
    df_std.to_csv(save_path[:-4]+"_std.csv")

    transformer = KernelPCA(n_components=pca_component, kernel='poly') #“linear” | “poly” | “rbf” | “sigmoid” | “cosine” | “precomputed”
    X_pca = transformer.fit_transform(X)
    df_pca = pd.DataFrame(X_pca, index=None, columns= list(range(pca_component)))
    df_pca.to_csv(save_path[:-4]+f"_pca_{ pca_component }.csv")


    print("===================================================================================")
    print(f"processed file saved to:\n { save_path },\n { save_path[:-4] }_nor.csv,\n { save_path[:-4] }_std.csv,\n { save_path[:-4] }_pca_{ pca_component }.csv")
    return

if __name__ == '__main__':
    # all_attr_list = ["address", "source", "transaction_count", "transaction_per_day", "time_interval_mean(min)", "time_interval_median(min)", "time_interval_std(min)", "from_cate", "to_cate", "from_title", "to_title", "send_count", "receive_count", "send_value_mean(eth)", "receive_value_mean(eth)", "value_dict(eth)", "average_gas", "first_date", "app_sequence"]
    num_attr_list = ["transaction_count", "transaction_per_day", "time_interval_mean(min)", "time_interval_median(min)", "time_interval_std(min)", "send_count", "receive_count", "send_value_mean(eth)", "receive_value_mean(eth)", "average_gas"]
    time_attr_list = ["transaction_count", "transaction_per_day", "time_interval_mean(min)", "time_interval_median(min)", "time_interval_std(min)"]
    new_columns_list = ["self_count", "nan_count", "defi_count", "exchanges_count", "other_count", "gambling_count", "games_count", "marketplaces_count", "social_count", "high-risk_count", "collectibles_count", "self_value", "nan_value", "defi_value", "exchanges_value", "other_value", "gambling_value", "games_value", "marketplaces_value", "social_value", "high-risk_value", "collectibles_value"]
    
    
    # do_k_means("./ml_data/processed_sum_std.csv", new_columns_list+new_columns_list, 3, 15000, 0, "./ml_data/labeled_1_sum.csv")
    cluster_preprocessing("./transaction/profiled/sum.csv","./ml_data/processed_sum.csv", 3)