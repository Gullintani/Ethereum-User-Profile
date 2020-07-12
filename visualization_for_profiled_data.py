import pandas as pd
import numpy as np
import pyecharts.options as opts
from pyecharts.charts import Scatter3D, WordCloud, Grid

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
                    max_=color_maximum/30000,
                    range_color=[
                        "#1710c0",
                        "#00ff0d",
                        "#fe0300",
                    ],
                    # max_=color_maximum/15,
                    # range_color=[
                    #     "#1710c0",
                    #     "#0b9df0",
                    #     "#00fea8",
                    #     "#00ff0d",
                    #     "#f5f811",
                    #     "#f09a09",
                    #     "#fe0300",
                    # ],
                ),
                opts.VisualMapOpts(
                    type_="size",
                    is_calculable=True,
                    dimension=4,
                    pos_bottom="20",
                    max_=size_max/10,
                    range_size=[10, 40],
                ),
            ]
        )
        .render(html_save_path)
    )

def word_cloud(file_path:str, html_save_path:str):
    df = pd.read_csv(file_path)
    # send title
    send_dict_list = df["to_title"].values
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
    receive_dict_list = df["from_title"].values
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

    print(send_store_dict)

    send_wordcloud = (
        WordCloud(
            init_opts=opts.InitOpts(
                width = "1440px",
                height = "920px",
                page_title = "Send Wordcloud",
                theme = "white"
            )
        )
        .add(series_name="Send DApps", data_pair=send_data_list, word_size_range=[6, 66])
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
        .add(series_name="Send DApps", data_pair=receive_data_list, word_size_range=[6, 66])
        .set_global_opts(
            title_opts=opts.TitleOpts(
                title="Receive from DApp Title Wordcloud", title_textstyle_opts=opts.TextStyleOpts(font_size=23)
            ),
            tooltip_opts=opts.TooltipOpts(is_show=True),
        )
        .render(html_save_path+"wordcloud_receive.html")
    )

if __name__ == '__main__':
    # scatter_3d("./further_mined_sum.csv", ["send_count", "receive_count", "transaction_count", "transaction_interval_cluster_label", "time_interval_std(min)"], "./html_output/time_interval_cluster_result_2.html")
    scatter_3d("./further_mined_sum_std.csv", ["send_count", "receive_count", "transaction_count", "time_interval_median(min)", "send_value_mean(eth)"], "./html_output/time_interval_cluster_result_3.html")
    # word_cloud("./transaction/profiled/sum.csv", "./html_output/")