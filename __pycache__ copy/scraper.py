import requests
import time
import json
import pandas as pd
import numpy as np
from pandas import DataFrame

# id_dict = {"9928":"Forsage-Smartway","10144":"EASY-CLUB","8848":"MillionMoney","9801":"DoubleWay","9696":"HEX","10124":"Ethrun","9910":"Fomo5k","9756":"RED-BOX-DAPP","7747":"CryptoHands","9823":"PyraBank-Hex","8702":"Pledgecamp","8843":"Shuffle-Monster-V3","9570":"Diamond-Dividends","10004":"DeFiGroup-ch---ETH","10092":"Crypto-Life"}

def build_db(input_path:str, save_path:str):
        df = pd.read_csv(input_path)
        index_list = df['index'].values
        index_list = index_list[536:]
        scrape_dappradar(index_list, save_path)
        return

def save_as_csv_dappradar(r_text:str, save_path):
        store_list = []
        r_dict = json.loads(r_text)
        if r_dict["success"] == False:
                print("API access failed: success = false")
                return
        r_contracts = r_dict["data"]["contracts"]
        r_info = r_dict["data"]["info"]
        for contract in r_contracts:
                if r_info["author"] == "":
                        author = "NA"
                else:
                        author = r_info["author"]
                line_list = [contract["address"], r_info["id"], r_info["title"].replace(" ", "_"), r_info["category"], author, r_info["balance"], r_info["contractsCount"], r_info["rankings"]["overall"]]
                store_list.append(line_list)
        
        store_array = np.array(store_list)
        df = pd.DataFrame(store_array, index = None, columns = ['address', 'id', 'title', 'category', 'author', 'balance', 'contractsCount', 'ranking'])
        file_path = save_path + str(r_info["id"]) + "_" + r_info["title"] + ".csv"
        df.to_csv(file_path)
        return

def scrape_dappradar(index_list, save_path):
        i = 1
        length = len(index_list)
        for index in index_list:
                # randsleep = np.random.randint(low = 1, high = 5, size = 1)
                # time.sleep(randsleep)

                request_link = "https://dappradar.com/api/dapp/" + str(index)
                headers = {
                        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.116 Safari/537.36",
                        "Connection": "keep-alive",
                        "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
                        "accept-language": "en-US,en;q=0.9,ja;q=0.8,zh-CN;q=0.7,zh-TW;q=0.6,zh;q=0.5",
                        "cache-control": "no-cache",
                        "pragma": "no-cache",
                        "sec-fetch-dest": "document",
                        "sec-fetch-mode": "navigate",
                        "sec-fetch-site": "none",
                        "sec-fetch-user": "?1",
                        "upgrade-insecure-requests": "1"
                        }
                try:
                        r = requests.get(request_link, headers = headers, timeout=150).text
                except:
                        print("connection failed")
                # save_as_csv_dappradar(r, save_path)
                try:
                        save_as_csv_dappradar(r, save_path)
                except:
                        print('error')
                
                print(f"{ i }/{ length } Dapp processed.")
                i += 1
                # break
        return

def saveAsCSV(r_json, key, path):
        r_json = eval(r_json)["content"]
        # Load the lists
        stday_list = np.asarray(eval(r_json["stday_list"]))
        balance_list = np.asarray(eval(r_json["balance_list"]))
        datadau_list = np.asarray(eval(r_json["datadau_list"]))
        ethvolume_list = np.asarray(eval(r_json["ethvolume_list"]))
        exchangerangking_list = np.asarray(eval(r_json["exchangerangking_list"]))
        totalrangking_list = np.asarray(eval(r_json["totalrangking_list"]))
        txs_list = np.asarray(eval(r_json["txs_list"]))

        # Format the arrays
        Date = stday_list.reshape(len(stday_list), 1)
        Balance = balance_list.reshape(len(balance_list), 1)
        DAU = datadau_list.reshape(len(datadau_list), 1)
        ETH_Vol = ethvolume_list.reshape(len(ethvolume_list), 1)
        Exchange_Rank = exchangerangking_list.reshape(len(exchangerangking_list), 1)
        Total_Rank = totalrangking_list.reshape(len(totalrangking_list), 1)
        Txs = txs_list.reshape(len(txs_list), 1)

        # hstack the arrays together
        data_array = np.hstack([Date, Balance, DAU, ETH_Vol, Exchange_Rank, Total_Rank, Txs])

        # Turn Array into Dataframe
        df = DataFrame(data_array, index = None, columns = ['Date', 'Balance', 'DAU', 'Vol', 'Cate Rank', 'Total Rank', 'Txs'])

        # Save as CSV file
        save_file_name = id_dict[key] + '.csv'
        save_file_path = path + save_file_name
        df.to_csv(save_file_path)

def ScrapeData(dict, save_path):
        i = 1
        e = 0
        for key in dict:
                # randsleep = np.random.randint(low = 1, high = 10, size = 1)
                # time.sleep(randsleep)
                payload = {
                        'daynumber':'all',
                        'id': key,
                        'sign':'false',
                        'langue':'en'
                }

                headers = {"accept":"application/json, text/plain, */*","accept-language":"zh-CN,zh;q=0.9,en;q=0.8,ja;q=0.7","cache-control":"no-cache","content-type":"application/x-www-form-urlencoded","pragma":"no-cache","sec-fetch-mode":"cors","sec-fetch-site":"same-origin"}
                r = requests.post('https://dapptotal.com/api/view',headers = headers, data = payload).text
                try:
                        saveAsCSV(r, key, save_path)
                        print(str(i) + " file saved: " + dict[key])
                        i = i + 1
                except:
                        print("error occurred.")
                        e = e + 1
                        i = i + 1
        print(f"{i} files scrapped, {e} failed.")

if __name__ == '__main__':
        # ScrapeData(id_dict, './csv_data/tron/highrisk/')
        # ScrapeData(id_dict, './top15_data/highrisk/')
        build_db('./contract_db/eth_index.csv','./contract_db/eth/')

