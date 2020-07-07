import os
import numpy as np
import pandas as pd
from sklearn import preprocessing
from game import Game

class Platform_data:
    def __init__(self, path:str):
        self.name = path[:-4]
        self.df = pd.read_csv(path)[['Balance', 'DAU', 'Vol', 'Txs', 'Name']]

    def normalize(self):
        df_data = self.df[['Balance', 'DAU', 'Vol', 'Txs']]
        df_name = self.df['Name']
        x = df_data.values
        min_max_scaler = preprocessing.MinMaxScaler()
        try:
            x_scaled = min_max_scaler.fit_transform(x)
        except:
            print("Normalization Failed...")
        df_std = pd.DataFrame(x_scaled, index = None, columns = ['Balance', 'DAU', 'Vol', 'Txs'])
        df_std = pd.concat([df_std, df_name], axis=1)
        self.df_std = df_std

    def get_trend_pattern(self, dataframe, columns, x_unit:str='day'):
        if x_unit == 'month':
            dataframe = dataframe.resample('M').sum()
        if x_unit == 'week':
            dataframe = dataframe.resample('w').sum()

        x = range(0, dataframe.shape[0])
        for attr in columns:
            y = dataframe[attr].values
            peak = y.max()
            slop = (y[0]-y[-1])/dataframe.shape[0]
            var = np.var(y)
        return [peak, var, slop]

def concate(file_path:str, save_path:str):
    files = os.listdir(file_path)
    i = 0
    e = 0
    DF = pd.DataFrame(columns = ['Balance', 'DAU', 'Vol', 'Txs', 'Name'])

    for filename in files:
        try:
            temp = Game(file_path + filename)
            df = temp.df_w[['Balance', 'DAU', 'Vol', 'Txs']]
            df['Name'] = filename[:-4]
            DF = pd.concat([DF, df])
            print("Files Collected:", filename)
            i += 1
        except:
            print("Concate failed.")
            e += 1
    DF.to_csv(save_path)
    print("========================================")
    print(f"concated {i} files. {e} failed.")
    return

# This is a bad way to fix Class design flaw
def normal_concate_normalize(file_path:str, save_path:str):
    files = os.listdir(file_path)
    i = 0
    e = 0
    DF = pd.DataFrame(columns = ['Balance', 'DAU', 'Vol', 'Txs', 'Name'])

    for filename in files:
        try:
            temp = pd.read_csv(file_path + filename)
            df = temp[['Balance', 'DAU', 'Vol', 'Txs']]
            df['Name'] = filename[4:-8]
            DF = pd.concat([DF, df])
            print("Files Collected:", filename)
            i += 1
        except:
            print("Concate failed.")
            e += 1
    DF.to_csv(save_path)
    print("========================================")
    print(f"concated {i} files. {e} failed.")
    temp = Platform_data(save_path)
    temp.normalize()
    temp.df_std.to_csv(save_path[:-7]+"std.csv")
    print("========================================")
    print("normalization done.")
    return

def concate_all(platform_list:list, cate_list:list):
    for platform in platform_list:
        for cate in cate_list:
            path = './csv_data/' + platform + '/' + cate + '/'
            save_path = './temp/' + platform + '_' + cate + '_raw.csv'
            concate(path, save_path)

def print_trend_feature(attr_list:list, path:str):
    '''
    The sequence is auc, peak, var, slop
    '''
    temp = Platform_data(path)
    temp.normalize()
    for attr in attr_list:
        feature = temp.get_trend_pattern(temp.df_std, [attr])
        feature.append(np.mean(temp.df_std.values))
        print(f"{attr}: {feature}")
        print("========================================")
    return

def eliminate_zero(path:str, save_path:str):
    df = pd.read_csv(path)
    length = df.shape[0]
    df_new = df.loc[df['DAU']+df['Txs']!=0]
    new_length = df_new.shape[0]
    df_new.to_csv(save_path)
    print(f"Original: {length}. After eliminate zero: {new_length}")

def dappradar_concator(file_path:str, save_path:str):
    files = os.listdir(file_path)
    DF = pd.DataFrame(index = None, columns = ['address', 'id', 'title', 'category', 'author', 'balance', 'contractsCount', 'ranking'])
    for filename in files:
        try:
            temp = pd.read_csv(file_path + filename)
            DF = pd.concat([DF, temp])
            print("Files Collected:", filename)
        except:
            print("Concate failed.")
    DF.to_csv(save_path)
    return

if __name__ == '__main__':
    # platform_list =['eth']
    # cate_list = ['game', 'gamble', 'highrisk', 'exchange']
    # concate_all(platform_list, cate_list)
    # normal_concate_normalize('./temp/', './eth_all_raw.csv')
    # eliminate_zero('./eth_all_std.csv', './eth_all_std_nozero.csv')
    dappradar_concator("./contract_db/eth/", "./contract_db/database.csv")