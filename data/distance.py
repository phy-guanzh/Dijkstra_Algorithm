import pandas as pd

# 定义城市坐标数据
city_coordinates = {
    "Edinburgh": [55.9533, -3.1883],
    "London": [51.5074, -0.1278],
    "Madrid": [40.4168, -3.7038],
    "Rome": [41.9028, 12.4964],
    "Budapest": [47.4979, 19.0402],
    "Kyiv": [50.4501, 30.5234],
    "Istanbul": [41.0082, 28.9784],
    "Baku": [40.4093, 49.8671],
    "Donetsk": [48.0159, 37.8029],
    "Moscow": [55.7558, 37.6173],
    "Saint Petersburg": [59.9343, 30.3351],
    "Stockholm": [59.3293, 18.0686],
    "Hamburg": [53.5511, 9.9937],
    "Tromsø": [69.6496, 18.9560],
    "Murmansk": [68.9585, 33.0827],
    "Arkhangelsk": [64.5399, 40.5152],
    "Ulyanovsk": [54.3142, 48.4031],
    "Bergen": [60.3913, 5.3221],
    "Oulu": [65.0121, 25.4651]
}

# 转换为 DataFrame
df = pd.DataFrame.from_dict(city_coordinates, orient='index', columns=['lat', 'long'])

# 重置索引，使城市名成为一列
df.reset_index(inplace=True)
df.rename(columns={'index': 'name'}, inplace=True)

# 将 DataFrame 保存为 CSV 文件
df.to_csv('city_coordinates.csv', index=False)

print("DataFrame successfully saved to 'city_coordinates.csv'.")

