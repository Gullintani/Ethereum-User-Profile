import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from numpy import trapz
from sklearn import preprocessing
from mpl_toolkits.mplot3d import Axes3D

class Game:
    def __init__(self, filepath:str):
        self.name = filepath[16:-4]
        self.df = pd.read_csv(filepath)[['Date', 'Balance', 'DAU', 'Vol', 'Cate Rank', 'Total Rank', 'Txs']]
        self.df['Date'] = pd.to_datetime(self.df['Date'])
        self.index = self.df['Date']
        self.df = self.df.set_index('Date')
        self.df_w = self.df.resample('w').sum()
        self.df_m = self.df.resample('m').sum()

    def normalize(self):
        df_data = self.df[['Balance', 'DAU', 'Vol', 'Txs']]
        x = df_data.values
        min_max_scaler = preprocessing.MinMaxScaler()
        try:
            x_scaled = min_max_scaler.fit_transform(x)
        except:
            print("Normalization Failed...")
        df_std = pd.DataFrame(x_scaled, index = None, columns = ['Balance', 'DAU', 'Vol', 'Txs'])
        df_std = pd.concat([self.index, df_std], axis = 1)
        self.df_std = df_std.set_index('Date')

    def draw(self, type:str, dataframe, columns:list, x_unit:str='day'):
        if x_unit == 'month':
            dataframe = dataframe.resample('M').sum()
        if x_unit == 'week':
            dataframe = dataframe.resample('w').sum()

        ax = plt.gca()
        ax.set_title(self.name + " " + x_unit)
        i = 0
        for i in range(0, len(columns)):
            dataframe.plot(kind=type, y=columns[i], ax=ax, color=plt.cm.Set1(i))
        plt.show()
        return 0

    def get_trend_pattern(self, dataframe, columns, x_unit:str='day'):
        if x_unit == 'month':
            dataframe = dataframe.resample('M').sum()
        if x_unit == 'week':
            dataframe = dataframe.resample('w').sum()

        x = range(0, dataframe.shape[0])
        for attr in columns:
            y = dataframe[attr].values
            auc = trapz(y, x, dx=1)
            argmax = np.argmax(y)
            # peak = y.max()
            slop = (y[-2]-y[-0])/dataframe.shape[0]
            var = np.var(y)
        return [auc, argmax/dataframe.shape[0], var, slop]
    
    def get_avg_data(self):
        avg_dau = np.mean(self.df_std.DAU.values)
        avg_balance = np.mean(self.df_std.Balance.values)
        avg_txs_num = np.mean(self.df_std.Txs.values)
        avg_txs_vol = np.mean(self.df_std.Vol.values)
        
        return [avg_dau, avg_balance, avg_txs_num, avg_txs_vol]

def get_all_trend_pattern(path:str="./csv_data/eth/game/", save_path:str="./", std:int = 0):
    '''
    The sequence is auc, argmax, var, slop
    '''
    files = os.listdir(path)
    features = []
    i = 0
    e = 0
    for filename in files:
        try:
            temp = Game(path + filename)
            temp.normalize()
            if(std==1):
                feature_list = temp.get_trend_pattern(temp.df_std, ['DAU'], 'week')
            else:
                feature_list = temp.get_trend_pattern(temp.df, ['DAU'], 'week')
            feature_list.append(filename[:-4])
            features.append(feature_list)
            print(f"feature is added: ", filename[:-4])
            i += 1
        except:
            print("Error Happened.")
            e += 1
    np.save(save_path, features)
    print("========================================")
    print(f"selected feature from {i} files. {e} failed. is_std?={std}")

def get_all_average_data(path:str="./csv_data/eth/game/", save_path:str="./"):
    '''
    The sequence is avg_dau, avg_balance, avg_txs_num, avg_txs_vol
    '''
    files = os.listdir(path)
    avg_attr = []
    i = 0
    e = 0
    for filename in files:
        try:
            temp = Game(path + filename)
            temp.normalize()
            temp_list = temp.get_avg_data()
            temp_list.append(temp.name)
            avg_attr.append(temp_list)
            print(f"avg data added: ", temp.name)
            i += 1
        except: 
            print("Error Happened.")
            e += 1
    np.save(save_path, avg_attr)
    print("========================================")
    print(f"selected avg data from {i} files. {e} failed.")
    return

def get_sum_data(file_path:str):
    files = os.listdir(file_path)
    data_list = []
    for filename in files:
        df = pd.read_csv(file_path + filename)
        df = df[['Balance', 'DAU', 'Vol', 'Total Rank', 'Txs']]
        data_list.append([file_path[13:-1], filename[:-4], df['Balance'].sum(), df['Balance'].mean(), df['DAU'].sum(), df['DAU'].mean(), df['Vol'].sum(), df['Vol'].mean(), df['Total Rank'].sum(), df['Total Rank'].mean(), df['Txs'].sum(), df['Txs'].mean()])
    
    np_list = np.array(data_list)
    df = pd.DataFrame(np_list, index = None, columns = ['Type', 'Name', 'Balance_sum', 'Balance_mean', 'DAU_sum', 'DAU_mean', 'Vol_sum', 'Vol_mean', 'Total_rank_sum', 'Total_rank_mean', 'Txs_sum', 'Txs_mean'])
    df.to_csv('./top15_data/highrisk.csv')
    return

if __name__ == '__main__':
    get_sum_data("./top15_data/highrisk/")

    # test = Game('./csv_data/eth/game/PickFlix.csv')
    # test.normalize()
    # print(test.df_m)
    # feature = test.get_trend_pattern(test.df_std,['DAU'],'day')
    # print(feature)
    # test.draw('line', test.df_std, ['DAU'], 'day')
    # auc, argmax_location, var, slop

    # get_all_trend_pattern("./csv_data/tron/highrisk/", "./tron_trend_highrisk.npy", 1)
    # get_all_average_data("./csv_data/eth/highrisk/", "./avg_data/eth/eth_avg_highrisk")
