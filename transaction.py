import os
import networkx as nx
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib as mpl
from efficient_apriori import apriori
from wordcloud import WordCloud
from mpl_toolkits.mplot3d import Axes3D
import random

def tag_user(file_path:str, save_path:str):
    
    return

def add_label(file_path:str, output_path:str, database_path:str, file_name:str):
    df_file = pd.read_csv(file_path)[['blockNumber', 'timeStamp', 'from', 'to', 'value', 'contractAddress', 'gasUsed']]
    df_database = pd.read_csv(database_path)

    new_array_file = []
    array_file = df_file.values
    for line in array_file:
        if line[2] == file_name[:-4]:
            from_title = "self"
            from_category = "self"
        else:
            try:
                from_title = df_database.loc[df_database['address'] == line[2], 'title'].iloc[0]
                from_category = df_database.loc[df_database['address'] == line[2], 'category'].iloc[0]
            except:
                from_title = line[2]
                from_category = line[2]
        
        if line[3] == file_name[:-4]:
            to_title = "self"
            to_category = "self"
        else:
            try:
                to_title = df_database.loc[df_database['address'] == line[3], 'title'].iloc[0]
                to_category = df_database.loc[df_database['address'] == line[3], 'category'].iloc[0]
            except:
                to_title = line[3]
                to_category = line[3]
        
        line = np.append(line, [from_title, to_title, from_category, to_category])
        new_array_file.append(line)

    new_df_file = pd.DataFrame(np.array(new_array_file), index=None, columns=['blockNumber', 'timeStamp', 'from', 'to', 'value', 'contractAddress', 'gasUsed', 'from_title', 'to_title', 'from_category', 'to_category'])
    
    # translate timestamp to datetime and set it as index, untested
    time_stamp_list = new_df_file["timeStamp"].values.tolist()
    time_list = [pd.Timestamp(x, unit="s") for x in time_stamp_list]
    new_df_file["Datetime"] = np.array(time_list)
    new_df_file = new_df_file.set_index('Datetime')
    
    new_df_file.to_csv(output_path)
    return

def batch_add_label(input_path:str, output_path:str):
    file_names = os.listdir(input_path)
    count = 1
    total = len(file_names)
    for file_name in file_names:
        add_label(input_path+file_name, output_path+file_name[:-4]+"_labeled.csv", "./contract_db/database.csv", file_name)
        print(f"transalted: { count }/{ total }")
        count += 1
    return

def composition_graph(file_path:str, label_select:str):
    df = pd.read_csv(file_path)
    value_series = df["to" + label_select].value_counts()
    print(value_series)
    fig1, ax1 = plt.subplots()
    ax1.pie(value_series.values, labels=value_series.index, autopct='%1.1f%%', shadow=False, startangle=90)
    ax1.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.

    plt.show()
    return

def transaction_graph(file_path:str, graph_param:str = "bycount"):
    df = pd.read_csv(file_path)
    series = df['from_category'].value_counts()
    
    df_draw = pd.DataFrame({'from':np.array(["self"]).repeat(len(series)), 'to':series.index, 'value':series.values})
    print(df_draw)
    
    G = nx.DiGraph()
    G.add_weighted_edges_from(df_draw.values)

    M = G.number_of_edges()
    edge_colors = range(2, M + 2)
    edge_alphas = [(5 + i) / (M + 4) for i in range(M)]

    pos = nx.spring_layout(G, k=0.01, iterations=1000)
    values = df_draw['value'].values
    nodes = nx.draw_networkx_nodes(G, pos, alpha=1, node_size=150, node_color='skyblue')
    edges = nx.draw_networkx_edges(G, pos, alpha=1, edge_color=values, edge_cmap=plt.cm.cool, width=3)
    labels = nx.draw_networkx_labels(G, pos, alpha=1, font_size=12, font_color='brown')

    for i in range(M):
        edges[i].set_alpha(edge_alphas[i])

    pc = mpl.collections.PatchCollection(edges, cmap=plt.cm.cool)
    pc.set_array(edge_colors)
    plt.colorbar(pc)
    ax = plt.gca()
    ax.set_axis_off()
    plt.show()
    return 0

def wordcloud(file_path:str, attribute:str):
    translation_df = pd.read_csv('./contract_db/database.csv')

    def grey_color_func(word, font_size, position, orientation, random_state=None, **kwargs):
        try:
            category = translation_df.loc[translation_df['title']==word, 'category'].values[0]
        except:
            return "hsl(121, 100%%, %d%%)" % 40
        if category in ['games', 'gambling', 'collectibles']:
            return "hsl(38, 100%%, %d%%)" % 50
        elif category in ['marketplaces', 'social', 'other']:
            return "hsl(276, 100%%, %d%%)" % 50
        elif category in ['defi', 'high-risk', 'exchanges']:
            return "hsl(197, 100%%, %d%%)" % 50

    df = pd.read_csv(file_path)
    word_dict = {}
    for index, row in df.iterrows():
        try:
            app_dict = eval(row["clean_to_title"])
        except:
            continue
        for key, value in app_dict.items():
            if key in word_dict.keys():
                word_dict[key] += value
            else:
                word_dict[key] = value
    del word_dict['unknown_addr']
    del word_dict['self']

    wordcloud = WordCloud(background_color="white",width=1000, height=1000).generate_from_frequencies(word_dict)
    plt.imshow(wordcloud.recolor(color_func=grey_color_func, random_state=3))
    wordcloud.to_file(f"./wordcloud_{attribute}.png")
    plt.axis("off")
    plt.show()
    return

def profile_labeled_data(file_path:str, save_path:str):
    store_list = []
    file_names = os.listdir(file_path)
    index = 1
    total = len(file_names)

    for file_name in file_names:
        try:
            df = pd.read_csv(file_path + file_name)
            # address, transaction count, transaction per day, from category, to category, from title, to title, transaction in/out, Average in value, Average out value, Average gas, First transaction, Interact DApp Sequence
            # transaction count
            transaction_count = len(df)
            
            time_stamp_list = df["timeStamp"].values.tolist()
            time_list = [pd.Timestamp(x, unit="s") for x in time_stamp_list]
            

            # transaction per day
            first_date = time_list[0]
            day_between = (time_list[-1] - time_list[0]).days

            try:
                transaction_per_day = round(transaction_count/day_between, 2)
            except:
                transaction_per_day = 0

            # category count
            df["from_category"] = df["from_category"].values.astype(str)
            from_category_dict = df["from_category"].value_counts().to_dict()

            df["to_category"] = df["to_category"].values.astype(str)
            to_category_dict = df["to_category"].value_counts().to_dict()
            
            # title count
            df["from_title"] = df["from_title"].values.astype(str)
            from_title_dict = df["from_title"].value_counts().to_dict()

            df["to_title"] = df["to_title"].values.astype(str)
            to_title_dict = df["to_title"].value_counts().to_dict()

            # transaction in/out
            try:
                send_count = from_category_dict["self"]
            except:
                send_count = 0

            try:
                receive_count = to_category_dict["self"]
            except:
                receive_count = 0

            # value
            send_value_mean = round(df.loc[df["from_title"] == "self", 'value'].values.astype(float).mean() / 1000000000000000000, 2)
            receive_value_mean = round(df.loc[df["to_title"] == "self", 'value'].values.astype(float).mean() / 1000000000000000000, 2)
            
            # average gas
            average_gas = round(df["gasUsed"].mean(), 2)

            # first transaction made
            # up there first_date

            # Interact App Sequence
            app_sequence = []
            for app in df["to_title"].values:
                app = str(app)
                if app not in app_sequence:
                    app_sequence.append(app)

            # time interval info
            timestamp_array = df["timeStamp"].values
            time_interval_list = []
            for i in range(1, len(timestamp_array)):
                time_interval_list.append(timestamp_array[i] - timestamp_array[i-1])

            IRQ = np.percentile(time_interval_list, 75) - np.percentile(time_interval_list, 25)
            lower_bound = np.percentile(time_interval_list, 25) - 1.5 * IRQ
            upper_bound = np.percentile(time_interval_list, 75) + 1.5 * IRQ

            new_list = []
            for item in time_interval_list:
                if item > lower_bound and item < upper_bound:
                    new_list.append(item/60)

            time_interval_mean = round(np.mean(new_list), 2)
            time_interval_std = round(np.std(new_list), 2)
            tiem_interval_median = round(np.median(new_list), 2)

            # transaction value by category
            receive_value_mean = df.loc[df["to_title"] == "self", 'value'].values.astype(float).mean()

            # Collected from
            to_category_value_dict = {}
            to_category_list = np.unique(df["to_category"].values)
            for category in to_category_list:
                category_value_sum = np.sum(df.loc[df["to_category"] == category, 'value'].values.astype(float))
                category_value_sum = round(category_value_sum / 1000000000000000000, 2)
                to_category_value_dict[category] = category_value_sum
            

            # Collect source
            # source = file_name.split("_")[0]
            # source = data_source

            # address, transaction count, transaction per day, from category, to category, from title, to title, transaction in/out, Average in value, Average out value Average gas, First transaction, Interact DApp Sequence
            store_list.append([file_name[:-12], transaction_count, transaction_per_day, time_interval_mean, tiem_interval_median, time_interval_std, from_category_dict, to_category_dict, from_title_dict, to_title_dict, send_count, receive_count, send_value_mean, receive_value_mean, to_category_value_dict, average_gas, first_date, app_sequence])
            print(f" { file_name } collected: { index }/ { total }")
            index += 1
        
        except:
            print("Error Happened")
        break

    store_array = np.array(store_list)
    store_df = pd.DataFrame(store_array, index = None, columns=["address", "transaction_count", "transaction_per_day", "time_interval_mean(min)", "time_interval_median(min)", "time_interval_std(min)", "from_cate", "to_cate", "from_title", "to_title", "send_count", "receive_count", "send_value_mean(eth)", "receive_value_mean(eth)", "value_dict(eth)", "average_gas", "first_date", "app_sequence"]).fillna(0)
    store_df.to_csv(save_path)
    print("================extraction done==================")
    return

def analysis_profile(file_path:str):
    df = pd.read_csv(file_path)

    # transaction info
    # fig1, ax1 = plt.subplots()
    # ax1.set_title('transaction count')
    # ax1.boxplot(df["transaction_count"].values)

    # fig2, ax2 = plt.subplots()
    # ax2.set_title('transaction per day')
    # ax2.boxplot(df["transaction_per_day"].values)

    # fig3, ax3 = plt.subplots()
    # ax3.set_title('send value')
    # ax3.boxplot(df["send_value_mean"].values)
    
    # fig4, ax4 = plt.subplots()
    # ax4.set_title('receive value')
    # ax4.boxplot(df["receive_value_mean"].values)
    print("==========================Transaction Info==============================")
    print("Average transaction count: " + str(df["transaction_count"].values.mean()))
    print("Average send count: " + str(df["send_count"].values.mean()))
    print("Average receive count: " + str(df["receive_count"].values.mean()))
    print("Average transaction per day: " + str(df["transaction_per_day"].values.mean()))
    print("Average send value(eth): " + str(df["send_value_mean(eth)"].values.mean()))
    print("Average receive value(eth): " + str(df["receive_value_mean(eth)"].values.mean()))
    # plt.show()
    
    # DApp info
    attribute_list = ["value_dict(eth)", "from_cate", "to_cate", "from_title", "to_title"]
    for attribute in attribute_list:
        dict_list = df[attribute].values
        store_dict = {}
        for cate_dict_str in dict_list:
            cate_dict = eval(cate_dict_str)
            for k, v in cate_dict.items():
                if k in store_dict.keys():
                        store_dict[k] += v
                else:
                    store_dict[k] = v
        print(f"=========================={ attribute }==============================")
        print(store_dict)

    # First transaction date
    df_date_index = df
    df_date_index['first_date'] = pd.to_datetime(df['first_date'])
    df_date_index = df_date_index.set_index('first_date')
    year_list = ['2015', '2016', '2017', '2018', '2019', '2020']
    count_list = []
    for year in year_list:
        count_list.append(len(df_date_index[year]))
    fig1, ax1 = plt.subplots()
    ax1.pie(count_list, labels=year_list, autopct='%1.1f%%', shadow=False, startangle=90)
    ax1.axis('equal')
    ax1.set_title('created year')
    plt.show()

    return

def apply_apriori(file_path:str):
    df = pd.read_csv(file_path)
    app_sequence = []
    item_array = df["app_sequence"].values
    
    for item in item_array:
        item = eval(item)
        try:
            item.remove('self')
        except:
            pass
        try:
            item.remove('nan')
        except:
            pass
        app_sequence.append(tuple(item))
    
    itemsets, rules = apriori(app_sequence, min_support=0.05, min_confidence=0.1)
    print(rules)
    print("===================================================================")
    print(itemsets)
    return

def add_usd(file_path:str):
    price_df = pd.read_csv('./eth_price.csv', index_col="Date")
    price_df.index = pd.to_datetime(price_df.index)

    file_names = os.listdir(file_path)
    process_index=0
    total = len(file_names)
    for file_name in file_names:
        df = pd.read_csv(file_path + file_name)

        df['value(usd)'] = '0'

        # transform to eth and change index to datetime
        df['Datetime'] = pd.to_datetime(df['Datetime'])
        df = df.set_index('Datetime')
        df['value(eth)'] = df['value'].apply(lambda x: int(x)/1000000000000000000)

        for index, row in df.iterrows():
            eth_price = price_df.loc[price_df.index.date == index, 'Value'].iloc[0]
            df.loc[index, 'value(usd)'] = round(row['value(eth)'] * eth_price, 2)
        
        df.to_csv('./transaction/19w/address_usd/' + file_name)
        print(f"processed: {process_index}/{total}")
        process_index += 1

if __name__ == '__main__':
    # add_usd("./transaction/19w/address/")

    # apply_apriori("./transaction/profiled/CryptokittySiringAuction4000.csv")

    # analysis_profile("./contract_db/contract_transaction_profiled.csv")
    # analysis_profile("./transaction/profiled/top10000.csv")

    # batch_add_label("./contract_db/contract_transaction/", "./contract_db/contract_transaction_labeled/")
    # batch_add_label("./transaction/all_cate_top25_transaction/", "./transaction/all_cate_top25_transaction_labeled/")

    # profile_labeled_data("./transaction/game/CryptokittySiringAuction_labeled/", "./z_profiling_test.csv")
    # profile_labeled_data("./transaction/all_cate_top25_transaction/", "./transaction/profiled/Etheremon1200.csv", "Etheremon")
    
    # transaction_graph("./transaction/labeled/0x4da725d81911dc6b452a79eacbe8e2df7ab4ca49_labeled.csv", "bycount")
    # composition_graph("./transaction/labeled/0xf165d353abddb7cb00052d610254249fcc12a8c7_labeled.csv", "_title")
    wordcloud("./temp_finance.csv", "finance_square")