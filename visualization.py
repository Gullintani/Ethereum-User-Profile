import os
import networkx as nx
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib as mpl
from mpl_toolkits.mplot3d import Axes3D
from math import pi

def transaction_graph(file_path:str):
    return

def database_visualization(file_path:str):
    df = pd.read_csv(file_path)
    print(df["category"].value_counts)
    return

def radar_graph(file_path:str):
    # Set data
    # Type,Name,Balance_sum,Balance_mean,DAU_sum,DAU_mean,Vol_sum,Vol_mean,Total_rank_sum,Total_rank_mean,Txs_sum,Txs_mean
    df = pd.read_csv(file_path)
    df = df[['Name', 'Balance_mean', 'DAU_mean', 'Vol_mean', 'Total_rank_mean', 'Txs_mean']][0:2]
    # df = pd.DataFrame({
    # 'group': ['A','B','C','D'],
    # 'Transaction': [38, 1.5, 30, 4],
    # 'Volumn': [29, 10, 9, 34],
    # 'Balance': [8, 39, 23, 24],
    # 'var4': [7, 31, 33, 14],
    # 'var5': [28, 15, 32, 14]
    # })
    
    # ------- PART 1: Create background
    # number of variable
    categories=list(df)[1:]
    N = len(categories)
    
    # What will be the angle of each axis in the plot? (we divide the plot / number of variable)
    angles = [n / float(N) * 2 * pi for n in range(N)]
    angles += angles[:1]
    
    # Initialise the spider plot
    ax = plt.subplot(111, polar=True)
    
    # If you want the first axis to be on top:
    ax.set_theta_offset(pi / 2)
    ax.set_theta_direction(-1)
    
    # Draw one axe per variable + add labels labels yet
    plt.xticks(angles[:-1], categories)
    
    # Draw ylabels
    ax.set_rlabel_position(0)
    plt.yticks([1000,2000,3000], ["1000","2000","3000"], color="grey", size=7)
    plt.ylim(0,3500)
    
    # ------- PART 2: Add plots
    # Plot each individual = each line of the data
    # I don't do a loop, because plotting more than 3 groups makes the chart unreadable
    
    # Ind1
    values=df.loc[0].drop('Name').values.flatten().tolist()
    values += values[:1]
    ax.plot(angles, values, linewidth=1, linestyle='solid', label="group A")
    ax.fill(angles, values, 'b', alpha=0.1)
    
    # Ind2
    values=df.loc[1].drop('Name').values.flatten().tolist()
    values += values[:1]
    ax.plot(angles, values, linewidth=1, linestyle='solid', label="group B")
    ax.fill(angles, values, 'r', alpha=0.1)
    
    # Add legend
    plt.legend(loc='upper right', bbox_to_anchor=(0.1, 0.1))
    plt.show()

def plot_3d_multifile(path:str, columns:list, columns_name:list):
    fig = plt.figure()
    ax = Axes3D(fig)
    
    cmap = ['spring', 'summer', 'autumn', 'winter']
    colors = ['red', 'yellow', 'blue', 'green']

    files = os.listdir(path)
    for i in range(0,len(files)):
        nparray = np.load(path + files[i])
        length = len(nparray)
        nparray = nparray[:,columns]

        cm = plt.get_cmap(cmap[i])
        col = [cm(float(i)/(26)) for i in range(length)]

        X = nparray[:,[0]].flatten()
        Y = nparray[:,[1]].flatten()
        Z = nparray[:,[2]].flatten()

        X = list(map(float, X))
        Y = list(map(float, Y))
        Z = list(map(float, Z))    

        # Plot Scatter
        #ax.scatter(X, Y, Z, c = col)
        ax.scatter(X, Y, Z, c = colors[i])
    
    # Set Legend
    # ax.legend(loc='best')
    
    # Set Axis
    ax.set_xlabel(columns_name[0])
    ax.set_ylabel(columns_name[1])
    ax.set_zlabel(columns_name[2])

    plt.title(path)
    plt.show()

def plot_3d_single(path:str, columns:list):
    df = pd.read_csv(path)
    if 'tron' in path:
        df_game = df.loc[df['Name']=='_game',['Balance', 'DAU', 'Vol', 'Txs', 'Name']]
        df_highrisk = df.loc[df['Name']=='_highrisk',['Balance', 'DAU', 'Vol', 'Txs', 'Name']]
        df_exchange = df.loc[df['Name']=='_exchange',['Balance', 'DAU', 'Vol', 'Txs', 'Name']]
        df_gamble = df.loc[df['Name']=='_gamble',['Balance', 'DAU', 'Vol', 'Txs', 'Name']]
    else:
        df_game = df.loc[df['Name']=='game',['Balance', 'DAU', 'Vol', 'Txs', 'Name']]
        df_highrisk = df.loc[df['Name']=='highrisk',['Balance', 'DAU', 'Vol', 'Txs', 'Name']]
        df_exchange = df.loc[df['Name']=='exchange',['Balance', 'DAU', 'Vol', 'Txs', 'Name']]
        df_gamble = df.loc[df['Name']=='gamble',['Balance', 'DAU', 'Vol', 'Txs', 'Name']]

    fig = plt.figure()
    ax = Axes3D(fig)

    cmap = ['spring', 'summer', 'autumn', 'winter']
    colors = ['red', 'yellow', 'blue', 'green']
    df_list = [df_game, df_highrisk, df_exchange, df_gamble]

    i = 0
    for item in df_list:
        X = item.Txs.values
        Y = item.Balance.values
        Z = item.DAU.values
        ax.scatter(X, Y, Z, c = colors[i])
        i+=1
    
    ax.set_xlabel("Txs")
    ax.set_ylabel("Balance")
    ax.set_zlabel("DAU")

    plt.title(path)
    plt.show()

if __name__ == '__main__':
    # plot_3d_multifile('./feature_data/eth/std/', [1,2,3], ['AUC', 'Peak', 'Var'])
    # plot_3d_multifile('./avg_data/eth/', [1,2,3], ['DAU', 'Balance', 'Txs'])
    # plot_3d_single('./cate_data/trone_w/tron_all_raw.csv', [])
    # transaction_graph('./transaction/cryptokitties_auction.csv')
    # radar_graph('./top15_data/game.csv')
    database_visualization("./contract_db/database.csv")