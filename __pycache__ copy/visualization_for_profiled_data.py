import asyncio
import pyecharts.options as opts
import pandas as pd
import numpy as np
from aiohttp import TCPConnector, ClientSession
from pyecharts.charts import Scatter3D

def scatter_3d(file_path:str, html_save_path:str):
    """
    Gallery 使用 pyecharts 1.1.0
    参考地址: https://echarts.baidu.com/examples/editor.html?c=scatter3d&gl=1&theme=dark

    目前无法实现的功能:

    1、暂时无法对 Grid3D 设置 轴线和轴坐标的 style (非白色背景下有问题)
    """

    async def get_json_data(url: str) -> dict:
        async with ClientSession(connector=TCPConnector(ssl=False)) as session:
            async with session.get(url=url) as response:
                return await response.json()


    # 获取官方的数据
    data = asyncio.run(
        get_json_data(
            url="https://echarts.baidu.com/examples/data/asset/data/nutrients.json"
        )
    )


    # 列名映射
    field_indices = {
        "calcium": 3,
        "calories": 12,
        "carbohydrate": 8,
        "fat": 10,
        "fiber": 5,
        "group": 1,
        "id": 16,
        "monounsat": 14,
        "name": 0,
        "polyunsat": 15,
        "potassium": 7,
        "protein": 2,
        "saturated": 13,
        "sodium": 4,
        "sugars": 9,
        "vitaminc": 6,
        "water": 11,
    }

    # 配置 config
    config_xAxis3D = "protein"
    config_yAxis3D = "fiber"
    config_zAxis3D = "sodium"
    config_color = "fiber"
    config_symbolSize = "vitaminc"

    # 构造数据
    data = [
        [
            item[field_indices[config_xAxis3D]],
            item[field_indices[config_yAxis3D]],
            item[field_indices[config_zAxis3D]],
            item[field_indices[config_color]],
            item[field_indices[config_symbolSize]],
            index,
        ]
        for index, item in enumerate(data)
    ]

    print(data)


    (
        Scatter3D(
            init_opts=opts.InitOpts(width="1440px", height="920px")
        )  # bg_color="black"
        .add(
            series_name="",
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
                    pos_top="10",
                    max_=79 / 2,
                    range_color=[
                        "#1710c0",
                        "#0b9df0",
                        "#00fea8",
                        "#00ff0d",
                        "#f5f811",
                        "#f09a09",
                        "#fe0300",
                    ],
                )
            ]
        )
        .render(html_save_path)
    )

if __name__ == '__main__':
    scatter_3d("./transaction/profiled/CryptokittySiringAuction4000.csv", "./html_output/scatter3d.html")