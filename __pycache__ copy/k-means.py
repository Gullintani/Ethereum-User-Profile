from sklearn.cluster import KMeans
import os
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from game import Game
from sklearn.manifold import TSNE

def k_means(path:str, n:int=4, rs=0):
    nparray = np.load(path)
    
    X = nparray[:,0:4]
    kmeans = KMeans(n_clusters=n, random_state=rs).fit(X)
    
    concate_tag = kmeans.labels_.reshape(len(kmeans.labels_), 1)
    tagged = np.concatenate((nparray, concate_tag),axis=1)
    df = pd.DataFrame(tagged, index = None, columns = ['auc', 'argmax', 'var', 'slop', 'name', 'cate'])
    df.to_csv(path[:-4]+'_tagged.csv')
    np.save(path[:-4]+'_tagged.npy', tagged)

    return kmeans.cluster_centers_, kmeans.labels_    

def npy_concator(path:str, save_path:str):
    files = os.listdir(path)
    a = np.zeros([1,5])
    for filename in files:
        temp = np.load(path+filename)
        a = np.concatenate((a,temp),axis=0)
    np.save(save_path, a)
    print(f"concate done. The shape of the new array is {a.shape}")
    return a

def tsne_operation(data, n_component:int):
    info = data[:,4:6]
    X = data[:, 0:4]
    tsne = TSNE(n_component, init='pca')
    result = tsne.fit_transform(X)
    result = np.concatenate((result, info),axis=1) 

    df = pd.DataFrame(result, index = None, columns = ['x', 'y', 'name', 'cate'])
    cluster_0 = df.loc[df['cate']=='0',['x','y']]
    cluster_1 = df.loc[df['cate']=='1',['x','y']]
    cluster_2 = df.loc[df['cate']=='2',['x','y']]
    
    plt.figure(figsize=(8, 8))
    colors = ['red','blue','green']
    df_list = [cluster_0, cluster_1, cluster_2]
    i = 0
    for item in df_list:
        x = item.x.values
        y = item.y.values
        plt.scatter(x, y, c = colors[i], alpha=0.2)
        i+=1
    plt.xticks([])
    plt.yticks([])
    plt.title("t-SNE visualization")
    plt.show()

def plot_result(path:str, search_path:str, assign_name_list:list=""):
    if assign_name_list == "":
        df = pd.read_csv(path)
        name_list = df.loc[df['cate']==2,['name']].values
        name_list = name_list.flatten().tolist()
    else:
        name_list = assign_name_list
    for name in name_list:
        try:
            path = search_path + name + ".csv"
            game = Game(path)
            game.normalize()

            y = game.df_std.DAU.values
            x = game.df_std.index.values
            plt.plot(x, y, label = name)
        except:
            continue
    
    plt.xlabel('x - axis')
    # Set the y axis label of the current axis.
    plt.ylabel('y - axis')
    # Set a title of the current axes.
    plt.title('test')
    # show a legend on the plot
    plt.legend()
    # Display a figure.
    plt.show()


if __name__ == '__main__':
    # concateor_save_path = './tron_trend.npy'
    # npy_concator('./temp/', concateor_save_path)
    # centers, labels = k_means(concateor_save_path, 3)
    
    # x = np.arange(len(labels))
    # plt.plot(x, labels)
    # plt.show()

    # nparray = np.load(concateor_save_path[:-4]+"_tagged.npy")
    # tsne_operation(nparray, 2)
    plot_result("./trend_data/eth/std/eth_trend_tagged.csv", "./csv_data/eth/all/", ['Etheremon', 'MegaCryptoPolis', 'win777'])
    # eth growth: ['CryptoDozer', 'HyperDragons', 'OpenSea']
    # eth inactive: ['TotalGame', 'MilFold', 'FOMO4D']
    # eth decline: ['Etheremon', 'MegaCryptoPolis', 'win777']