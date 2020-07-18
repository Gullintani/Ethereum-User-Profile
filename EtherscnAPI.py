# Powered by Etherscan.io APIs
import requests, os
import pandas as pd
import numpy as np

def save_transaction_data(data_list:list, save_path:str):
    store_list = []
    for item_dict in data_list:
        store_list.append([item_dict["blockNumber"], item_dict["timeStamp"], item_dict["hash"], item_dict["from"], item_dict["to"], item_dict["value"], item_dict["gas"], item_dict["gasPrice"], item_dict["contractAddress"], item_dict["gasUsed"], item_dict["isError"]])
    df_titles = ["blockNumber", "timeStamp", "hash", "from", "to", "value", "gas", "gasPrice", "contractAddress", "gasUsed", "isError"]
    store_df = pd.DataFrame(np.array(store_list), index=None, columns=df_titles)
    store_df.to_csv(save_path)
    return

class Contract:
    def __init__(self, address:str):
        self.api_key = 'IGK5V2U9EW3ZJRCZHQUVGW3DEPXNVCB73G'
        self.address = address
    
    def r_process(self, r:str):
        r_dict = eval(r)
        if r_dict["status"] == '1':
            return r_dict["result"]
        else: 
            return r_dict["message"]

    def account(self, type:str, startblock:str='10001', endblock:str='99999999'):
        '''
        param: type
            balance: Get Ether Balance for a single Address
            txlist: Get a list of 'Normal' Transactions By Address
            txlistinternal: Get a list of 'Internal' Transactions by Address
            tokentx: Get a list of "ERC20 - Token Transfer Events" by Address
            tokennfttx: Get a list of "ERC721 - Token Transfer Events" by Address
            getminedblocks: Get list of Blocks Mined by Address
        '''
        api_link = f"https://api.etherscan.io/api?module=account&action={ type }&address={ self.address }&tag=latest"
        if type == "balance":
            api_link = api_link + f"&apikey={ self.api_key }"
            r = requests.get(api_link).text
            return self.r_process(r)
        elif type == "getminedblocks":
            api_link = api_link + f"&blocktype=blocks&apikey={ self.api_key }"
            r = requests.get(api_link).text
            return self.r_process(r)
        else:
            api_link = api_link + f"&startblock={ startblock }&endblock={ endblock }&sort=asc" + f"&apikey={ self.api_key }"
            # print(api_link)
            r = requests.get(api_link, timeout=200).text
            return self.r_process(r)
        return

    def contract(self):
        return

if __name__ == '__main__':
    # df = pd.read_csv("./etherscan_top_account.csv")
    # address_list = df["Address"].values[7500:10000] #20200712 18:00 from 0 to 2500
    # =====================================================================================
    path = "./transaction/all_cate_top25_transaction/"
    file_names = os.listdir(path)[36:]
    file_index = 1
    file_total = len(file_names)
    for file_name in file_names:
        df = pd.read_csv(path+file_name)
        name_list = file_name.split("_")
        address_list = np.unique(df["from"].values)
        index = 1
        total = len(address_list)
        for item in address_list:
            try:
                request_entity = Contract(item)
                a = request_entity.account("txlist")
                save_transaction_data(a, "./transaction/top25_user_transaction/" + name_list[0]+ "_" + name_list[1] + str(index) + ".csv")
                # save_transaction_data(a, f"./transaction/game/GodsUnchained_raw/{ request_entity.address }.csv")
                # save_transaction_data(a, f"./transaction/contract_tx_csv/GodsUnchained2.csv")
                print(f"processed file:{file_index}/{ file_total }; in_file transaction:{ index }/{ total }")
                index += 1
            except:
                print(f"failed:{file_index}/{ file_total }; in_file transaction:{ index }/{ total }\nat{path+file_name}")
                index += 1
                continue
        file_index += 1
    # =====================================================================================
    # address_list= ["0x06012c8cf97BEaD5deAe237070F9587f8E7A266d"]
    # index = 1
    # total = len(address_list)
    # for item in address_list:
    #     # try:
    #     request_entity = Contract(item)
    #     a = request_entity.account("txlist")
    #     save_transaction_data(a, f"./{ request_entity.address }.csv")
    #         # save_transaction_data(a, f"./contract_db/contract_transaction/{ request_entity.address }.csv")
    #         # save_transaction_data(a, f"./transaction/game/GodsUnchained_raw/{ request_entity.address }.csv")
    #         # save_transaction_data(a, f"./transaction/contract_tx_csv/GodsUnchained2.csv")
    #     # except:
    #     #     print("failed")
    #     #     index += 1
    #     #     continue
    #     # print(f"processed { index }/{ total }")
    #     index += 1
    
    
    # request_entity = Contract("0xC7af99Fe5513eB6710e6D5f44F9989dA40F27F26")
    # a = request_entity.account("txlist")
    # save_transaction_data(a, f"./transaction/{ request_entity.address }.csv")