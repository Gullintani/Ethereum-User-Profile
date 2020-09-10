import pandas as pd
import numpy as np
import pyecharts.options as opts
from pyecharts.charts import Scatter, Scatter3D, WordCloud, Grid

def scatter_2d(file_path:str, html_save_path:str):
    df = pd.read_csv(file_path)[["0", "1"]]
    data = df.values
    # data.sort(key=lambda x: x[0])
    x_data = [d[0] for d in data]
    y_data = [d[1] for d in data]

    (
        Scatter(init_opts=opts.InitOpts(width="1600px", height="1000px"))
        .add_xaxis(xaxis_data=x_data)
        .add_yaxis(
            series_name="",
            y_axis=y_data,
            symbol_size=20,
            label_opts=opts.LabelOpts(is_show=False),
        )
        .set_series_opts()
        .set_global_opts(
            xaxis_opts=opts.AxisOpts(
                type_="value", splitline_opts=opts.SplitLineOpts(is_show=True)
            ),
            yaxis_opts=opts.AxisOpts(
                type_="value",
                axistick_opts=opts.AxisTickOpts(is_show=True),
                splitline_opts=opts.SplitLineOpts(is_show=True),
            ),
            tooltip_opts=opts.TooltipOpts(is_show=False),
        )
        .render(html_save_path)
    )
    return

def scatter_3d(file_path:str, attribute_list:list, html_save_path:str):

    # config
    config_xAxis3D = attribute_list[0]
    config_yAxis3D = attribute_list[1]
    config_zAxis3D = attribute_list[2]
    config_color = attribute_list[3]
    config_symbolSize = attribute_list[4]

    # data
    df = pd.read_csv(file_path)
    data = df[attribute_list].values.tolist()

    color_maximum = df[attribute_list[3]].values.max()
    size_max = df[attribute_list[4]].values.max()

    (
        Scatter3D(
            init_opts=opts.InitOpts(
                width = "1440px",
                height = "920px",
                page_title = "3D-Scatter",
                theme = "white"
                )
        )  # bg_color="black"
        .add(
            series_name=str(attribute_list),
            data=data,
            xaxis3d_opts=opts.Axis3DOpts(
                name=config_xAxis3D,
                type_="value",
                # textstyle_opts=opts.TextStyleOpts(color="#fff"),
            ),
            yaxis3d_opts=opts.Axis3DOpts(
                name=config_yAxis3D,
                type_="value",
                # textstyle_opts=opts.TextStyleOpts(color="#fff"),
            ),
            zaxis3d_opts=opts.Axis3DOpts(
                name=config_zAxis3D,
                type_="value",
                # textstyle_opts=opts.TextStyleOpts(color="#fff"),
            ),
            grid3d_opts=opts.Grid3DOpts(width=100, height=100, depth=100),
        )
        .set_global_opts(
            visualmap_opts=[
                opts.VisualMapOpts(
                    type_="color",
                    is_calculable=True,
                    dimension=3,
                    pos_top="20",
                    # max_=2,
                    # range_color=[
                    #     "#1710c0",
                    #     "#00ff0d",
                    #     "#fe0300",
                    # ],
                    max_=color_maximum/100,
                    range_color=[
                        "#1710c0",
                        "#0b9df0",
                        "#00fea8",
                        "#00ff0d",
                        "#f5f811",
                        "#f09a09",
                        "#fe0300",
                    ],
                ),
                opts.VisualMapOpts(
                    type_="size",
                    is_calculable=True,
                    dimension=4,
                    pos_bottom="20",
                    max_=size_max/100,
                    range_size=[10, 50],
                ),
            ]
        )
        .render(html_save_path)
    )

def word_cloud(file_path:str, html_save_path:str):
    df = pd.read_csv(file_path)
    # send title
    send_dict_list = df["clean_to_title"].values
    send_store_dict = {}
    for send_dict_str in send_dict_list:
        send_dict = eval(send_dict_str)
        for k, v in send_dict.items():
            if k in send_store_dict.keys():
                    send_store_dict[k] += v
            else:
                send_store_dict[k] = v
    send_data_list = []
    for key, value in send_store_dict.items():
        send_data_list.append((key, str(value)))
    
    # receive title
    receive_dict_list = df["clean_from_title"].values
    receive_store_dict = {}
    for receive_dict_str in receive_dict_list:
        receive_dict = eval(receive_dict_str)
        for k, v in receive_dict.items():
            if k in receive_store_dict.keys():
                    receive_store_dict[k] += v
            else:
                receive_store_dict[k] = v
    receive_data_list = []
    for key, value in receive_store_dict.items():
        receive_data_list.append((key, str(value)))


    send_wordcloud = (
        WordCloud(
            init_opts=opts.InitOpts(
                width = "1440px",
                height = "920px",
                page_title = "Send Wordcloud",
                theme = "white"
            )
        )
        .add(series_name="Send DApps", data_pair=send_data_list, word_size_range=[12, 66], shape='circle',textstyle_opts=())
        .set_global_opts(
            title_opts=opts.TitleOpts(
                title="Send to DApp Title Wordcloud", title_textstyle_opts=opts.TextStyleOpts(font_size=23)
            ),
            tooltip_opts=opts.TooltipOpts(is_show=True),
        )
        .render(html_save_path+"wordcloud_send.html")
    )

    receive_wordcloud = (
        WordCloud(
            init_opts=opts.InitOpts(
                width = "1440px",
                height = "920px",
                page_title = "Receive Wordcloud",
                theme = "white"
            )
        )
        .add(series_name="Send DApps", data_pair=receive_data_list, word_size_range=[6, 66], shape='circle')
        .set_global_opts(
            title_opts=opts.TitleOpts(
                title="Receive from DApp Title Wordcloud", title_textstyle_opts=opts.TextStyleOpts(font_size=23)
            ),
            tooltip_opts=opts.TooltipOpts(is_show=True),
        )
        .render(html_save_path+"wordcloud_receive.html")
    )


if __name__ == '__main__':
    num_attr_list = ["transaction_count", "transaction_per_day", "time_interval_mean(min)", "time_interval_median(min)", "time_interval_std(min)", "send_count", "receive_count", "send_value_mean(eth)", "receive_value_mean(eth)", "average_gas"]
    time_attr_list = ["transaction_count", "transaction_per_day", "time_interval_mean(min)", "time_interval_median(min)", "time_interval_std(min)"]
    new_columns_list = ["self_count", "nan_count", "defi_count", "exchanges_count", "other_count", "gambling_count", "games_count", "marketplaces_count", "social_count", "high-risk_count", "collectibles_count", "self_value", "nan_value", "defi_value", "exchanges_value", "other_value", "gambling_value", "games_value", "marketplaces_value", "social_value", "high-risk_value", "collectibles_value"]
    
    # 19w address data
    attr_list = ["time_interval_std(min)", "time_interval_std(min)", "transaction_count", "transaction_count", "receive_value_mean(eth)"]
    scatter_3d("./transaction/19w/19w_profiled/clean_user_all.csv", attr_list, "./html_output/19w/" + "-".join(attr_list) + ".html")

    # scatter_2d("./ml_data/processed_sum_pca_2.csv", "./html_output/pca2_1.html")

    # Top 25 contract transaction info
    # scatter_3d("./transaction/profiled/all_cate_top25_transaction_profiled.csv", ["transaction_count", "time_interval_mean(min)", "time_interval_median(min)", "time_interval_std(min)", "send_value_mean(eth)"], "./html_output/scatter_top25_DApp_contract1.html")
    # scatter_3d("./transaction/profiled/all_cate_top25_transaction_profiled.csv", ["send_count", "receive_count", "transaction_per_day", "time_interval_std(min)", "send_value_mean(eth)"], "./html_output/scatter_DApp_contract2.html")

    # All contract transaction info
    # scatter_3d("./contract_db/contract_transaction_profiled.csv", ["send_count", "receive_count", "transaction_per_day", "time_interval_std(min)", "send_value_mean(eth)"], "./html_output/scatter_DApp_contract2.html")
    
    # scatter_3d("./ml_data/processed_sum_pca_3.csv", ["0", "1", "2", "1", "1"], "./html_output/pca3_1.html")
    # scatter_3d("./ml_data/labeled_1_sum.csv", ["send_count", "receive_count", "transaction_count", "cluster_label", "send_value_mean(eth)"], "./html_output/scatter_sum_std_6.html")
    # scatter_3d("./ml_data/labeled_1_sum.csv", ["send_count", "receive_count", "transaction_count", "cluster_label", "send_value_mean(eth)"], "./html_output/scatter_sum_std_4.html")
    # scatter_3d("./ml_data/processed_sum_std.csv", ["games_value", "gambling_value", "exchanges_value", "transaction_count", "send_value_mean(eth)"], "./html_output/scatter_sum_std_4.html")
    # scatter_3d("./further_mined_sum.csv", ["send_count", "receive_count", "transaction_count", "transaction_interval_cluster_label", "time_interval_std(min)"], "./html_output/time_interval_cluster_result_2.html")
    # scatter_3d("./further_mined_sum_std.csv", ["send_count", "receive_count", "transaction_count", "time_interval_median(min)", "send_value_mean(eth)"], "./html_output/time_interval_cluster_result_3.html")
    # scatter_3d("./transaction/profiled/top10000.csv", ["send_count", "receive_count", "transaction_count", "time_interval_median(min)", "send_value_mean(eth)"], "./html_output/scatter_top10000.html")
    word_cloud("./temp_utility.csv", "./html_output/utility/")