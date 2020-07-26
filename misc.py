import pandas as pd
import numpy as np
import os
from efficient_apriori import apriori

def rename(file_path:str):
    file_names = os.listdir(file_path)
    for file_name in file_names:
        if " " in file_name:
            new_name = file_name.replace(" ", "")
            os.rename(file_path+file_name, file_path+new_name)
    print("Complete")
    return

def get_address_list(file_path:str, save_path:str):
    df = pd.read_csv(file_path)
    address_array = np.unique(df["from"].values)
    with open(save_path, 'w') as w:
        w.write(str(address_array.tolist()))
    print("changed to txt file.")
    return

def test():
    # transactions = [('eggs', 'bacon', 'soup'),
    #             ('eggs', 'bacon', 'apple'),
    #             ('soup', 'bacon', 'banana')]
    # print(type(transactions[0]))
    # itemsets, rules = apriori(transactions, min_support=0.5, min_confidence=1)
    # print(rules)  # [{eggs} -> {bacon}, {soup} -> {bacon}]
    
    print(list(range(2)))

def add_time_difference(file_path:str):
    file_names = os.listdir(file_path)
    for file_name in file_names:
        df = pd.read_csv(file_path + file_name)
    return

def concate_profiled_record(file_path:str, save_path:str):
    file_names = os.listdir(file_path)
    i = 0
    DF = pd.DataFrame(index=None, columns = ["address", "source", "transaction_count", "transaction_per_day", "time_interval_mean(min)", "time_interval_median(min)", "time_interval_std(min)", "from_cate", "to_cate", "from_title", "to_title", "send_count", "receive_count", "send_value_mean(eth)", "receive_value_mean(eth)", "value_dict(eth)", "average_gas", "first_date", "app_sequence"])
    for file_name in file_names:
        df = pd.read_csv(file_path+file_name)
        DF = pd.concat([DF, df])
        print(f"processed: { file_name }")
    DF.to_csv(save_path)
    print("========================================")
    print(f"concated {len(file_names)} files.")
    return

def move_top10(from_path, save_path, name_list):
    df = pd.read_csv(name_list)
    target_list = df["title"].values
    # print(target_list)
    file_names = os.listdir(from_path)
    index = 1
    for file_name in file_names:
        file_key_word = file_name.split("_")[1].lower()
        # print(file_key_word)
        for target in target_list:
            if file_key_word in target:
                os.system(f"cp { from_path + file_name } {save_path + file_name}")
                print(index)
                index += 1 
    return

def concate_all_cate_top_transaction(from_path, save_path):
    file_names = os.listdir(from_path)
    i = 1
    total = len(file_names)
    DF = pd.DataFrame(index=None, columns = ["blockNumber", "timeStamp", "hash", "from", "to", "value", "gas", "gasPrice", "contractAddress", "gasUsed", "isError", "category", "title"])
    for file_name in file_names:
        df = pd.read_csv(from_path+file_name)
        name_content_list = file_name.split("_")
        df.drop_duplicates("from", "first", inplace = True)
        df["category"] = name_content_list[0]
        df["title"] = "".join(name_content_list[1:-1])
        DF = pd.concat([DF, df])
        print(f"processed: { i}/{total }")
        i += 1

    DF = DF[["blockNumber","timeStamp","hash","from","to","value","gas","gasPrice","contractAddress","gasUsed","isError","category","title"]]
    DF.to_csv(save_path)
    print("========================================")
    print(f"concated {len(file_names)} files.")
    return

def concate_labeled_transaction(from_path, save_path):
    file_names = os.listdir(from_path)
    i = 1
    total = len(file_names)
    df = pd.read_csv(from_path + file_names[1])
    df.to_csv(save_path)
    for file_name in file_names[1:]:
        df = pd.read_csv(from_path+file_name)
        df.to_csv(save_path, index=False, header=False, mode='a+')
        print(f"processed: { i }/{total }")
        i += 1

    print("========================================")
    print(f"concated {len(file_names)} files.")
    return

def analysis_all_cate_top_transaction(from_path):
    df = pd.read_csv(from_path, dtype={'timeStamp':int, 'from':object, 'to':object, 'value':float, 'contractAddress':object, 'gasUsed':float,
       'from_title':object, 'to_title':object, 'from_category':object, 'to_category':object})
    print(df.dtypes)
    # df.drop_duplicates(subset="from", inplace=True)
    # print(df["category"].value_counts())
    print("=======================================")
    from_address_list = df["from"].values
    print(f"unique address: { len(np.unique(from_address_list)) }")
    print(f"total transaction: { len(from_address_list) }")
    print("=======================================")
    # to_address_list = df["to"].values
    # print(len(np.unique(to_address_list)))
    # print(len(to_address_list))
    # print(df["title"].value_counts())

    # df1 = df.iloc[:47969, :]
    # df1.to_csv("./transaction/all_cate_top10_transaction_simplified_1.csv")
    # del df1
    # df2 = df.iloc[47969:95939, :]
    # df2.to_csv("./transaction/all_cate_top10_transaction_simplified_2.csv")
    # del df2
    # df3 = df.iloc[95939:143908, :]
    # df3.to_csv("./transaction/all_cate_top10_transaction_simplified_3.csv")
    # del df3
    # df4 = df.iloc[143908:, :]
    # df4.to_csv("./transaction/all_cate_top10_transaction_simplified_4.csv")
    return

def replace_NAN_in_title_attr(file_path:str, save_path:str):
    df = pd.read_csv(file_path, dtype={'timeStamp':int, 'from':object, 'to':object, 'value':float, 'contractAddress':object, 'gasUsed':float, 'from_title':object, 'to_title':object, 'from_category':object, 'to_category':object})
    df = df.fillna("NAN")

    index = 1
    total = len(df)
    for index, row in df.iterrows():
        if row["from_title"] == "NAN":
            df.loc[index, "from_title"] = df.loc[index, "from"]
        if row["to_title"] == "NAN":
            df.loc[index, "to_title"] = df.loc[index, "to"]
        if row["from_category"] == "NAN":
            df.loc[index, "from_category"] = df.loc[index, "from"]
        if row["to_category"] == "NAN":
            df.loc[index, "to_category"] = df.loc[index, "to"]
        
        print(f"replaced NAN with address {index }/{total}")
        index += 1
    df.to_csv(save_path, index=False)
    return

if __name__ == '__main__':
    replace_NAN_in_title_attr("./transaction/experiment/experiment.csv", "./transaction/experiment/experiment_replaced_NAN.csv")
    
    # concate_labeled_transaction("./transaction/game/all_game_labeled/","./transaction/game/all_game_labeled.csv")
    # analysis_all_cate_top_transaction("./transaction/game/all_game_labeled.csv")

    # analysis_all_cate_top_transaction("./transaction/all_cate_top10_transaction_simplified_4.csv")
    # concate_all_cate_top_transaction("./transaction/all_cate_top10_transaction/", "./transaction/all_cate_top10_transaction_simplified.csv")
    # move_top10("./transaction/all_cate_top25_transaction/", "./transaction/all_cate_top5_transaction/", "./contract_db/all_cate_top5_index.csv")
    
    # rename("./contract_db/all_cate_top25/")
    # concate_profiled_record("./transaction/profiled/sum/", "./transaction/profiled/sum.csv")
    # test()
    # get_address_list("./transaction/contract_tx_csv/GodsUnchained2.csv", "./transaction/contract_tx_list/GodsUnchained2.txt")
    # add_time_difference("./transaction/CryptokittySiringAuction_labeled/")