import pandas as pd
import numpy as np
import os
from efficient_apriori import apriori

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
    test = [1,2,3,4,5,6,7,8,9,10,11,12,13,14]
    for i in range(0,len(test)):
        if test[i]<5:
            test.pop(i)
    print(test)

def add_time_difference(file_path:str):
    file_names = os.listdir(file_path)
    for file_name in file_names:
        df = pd.read_csv(file_path + file_name)
    return

def concate_profiled_record(file_path:str, save_path:str):
    file_names = os.listdir(file_path)
    i = 0
    DF = pd.DataFrame(columns = ["address", "source", "transaction_count", "transaction_per_day", "time_interval_mean(min)", "time_interval_median(min)", "time_interval_std(min)", "from_cate", "to_cate", "from_title", "to_title", "send_count", "receive_count", "send_value_mean(eth)", "receive_value_mean(eth)", "value_dict(eth)", "average_gas", "first_date", "app_sequence"])
    for file_name in file_names:
        df = pd.read_csv(file_path+file_name)
        DF = pd.concat([DF, df])
        print(f"processed: { file_name }")
    DF.to_csv(save_path)
    print("========================================")
    print(f"concated {len(file_names)} files.")
    return

if __name__ == '__main__':
    concate_profiled_record("./transaction/profiled/sum/", "./transaction/profiled/sum.csv")
    # test()
    # get_address_list("./transaction/contract_tx_csv/axie_infinity.csv", "./transaction/contract_tx_list/axie_infinity.txt")
    # add_time_difference("./transaction/CryptokittySiringAuction_labeled/")