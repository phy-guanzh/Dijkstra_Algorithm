import streamlit as st
import numpy as np
import pandas as pd
import math
from pathlib import Path
from datetime import datetime
import time
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import requests
import os

from selenium import webdriver
from bs4 import BeautifulSoup

# Set the title and favicon that appear in the Browser's tab bar.
st.set_page_config(
    page_title='Pathes dashboard',
    page_icon=':earth_asia:', # This is an emoji shortcode. Could be a URL too.
)

# -----------------------------------------------------------------------------
# Declare some useful functions.

@st.cache_data

def check_symmtric(sorted_df):
    difference_no_nan = (sorted_df != sorted_df.transpose()) & sorted_df.notna() & sorted_df.transpose().notna()

    asymmetric_elements_no_nan = difference_no_nan[difference_no_nan].stack()

    for index in asymmetric_elements_no_nan.index:
        original_value = sorted_df.loc[index]
        transpose_value = sorted_df.T.loc[index]
        print(f"Asymmetry at {index}: Original = {original_value}, Transpose = {transpose_value}")
        return False

    return True

def find_pathes(previous, end_point):
    if not previous[end_point]:
        return [[end_point]]
    pathes = []
    for i in previous[end_point]:
        #tmp_path.append(i)
        sub_path = find_pathes(previous, i)
        print(sub_path,i)
        for sub in sub_path:
            pathes.append(sub + [end_point])
    return pathes


def calc_dis_path(n, start_point, end_point):
    dist = [np.inf] * n  # define shortest distance
    visited = [False] * n  # define visit status
    previous = [[] for _ in range(n)]
    dist[start_point] = 0

    for _ in range(n):  # loop for every points we did not visit
        u = -1
        min_distance = inf

        for i in range(n):
            if not visited[i] and dist[i] < min_distance:
                min_distance = dist[i]
                u = i
        if u == -1:
            break

        for j in range(n):
            if visited[j] == False and np_network[u][j] != inf:
                new_distance = dist[u] + np_network[u][j]  # where dist[u] is min_distance
                print(u, j, new_distance, dist[u], np_network[u][j])
                if new_distance < dist[j]:
                    dist[j] = new_distance
                    print("here we update: distance j ", j, " with ", new_distance)
                    previous[j] = [u]
                elif new_distance == dist[j]:
                    previous[j].append(u)
        visited[u] = True

    return previous, dist


def find_lowest_price1(city_pair="EDI-LHR", start_date=datetime.today().strftime('%Y-%m-%d')):
    origin, destination = city_pair.split("-")

    driver = webdriver.Chrome()

    driver.get(f"https://www.kayak.com/flights/{origin}-{destination}/{start_date}?ucs=8liajb&sort=price_a")

    time.sleep(20)

    content = driver.page_source

    soup = BeautifulSoup(content, 'html.parser')

    prices = []
    for div in soup.findAll('div', attrs={'class': 'f8F1-price-text'}):
        price_text = div.text.strip()  # 提取价格文本
        if price_text.startswith('$'):
            price = int(price_text[1:])  # 去掉 "$" 并转换为整数
            prices.append(price)
    driver.quit()
    if prices:
        min_price = min(prices)
        st.write(f"The minimum price of {city_pair} on {start_date} is: ${min_price}")
        return min_price
    else:
        st.write(f"No prices found for {city_pair} on {start_date}")
        return None



def find_lowest_price(city_pair="EDI-LHR", start_date=datetime.today().strftime('%Y-%m-%d')):
    origin, destination = city_pair.split("-")
    url = f"https://www.kayak.com/flights/{origin}-{destination}/{start_date}?ucs=8liajb&sort=price_a"

    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
    }
    response = requests.get(url, headers=headers)

    # 检查是否抓取成功
    if response.status_code != 200:
        st.write(f"Failed to retrieve data for {city_pair} on {start_date}")
        return None

    soup = BeautifulSoup(response.content, 'html.parser')
    prices = []
    for div in soup.findAll('div', attrs={'class': 'f8F1-price-text'}):
        price_text = div.text.strip()
        if price_text.startswith('$'):
            price = int(price_text[1:])
            prices.append(price)

    if prices:
        min_price = min(prices)
        st.write(f"The minimum price of {city_pair} on {start_date} is: ${min_price}")
        return min_price
    else:
        st.write(f"No prices found for {city_pair} on {start_date}")
        return None


# -----------------------------------------------------------------------------
# Draw the actual page

# Set the title that appears at the top of the page.
st.markdown("""
<h2 style='text-align: center; color: #4CAF50;'> 🌏 Find the Shortest Path For your Journey!</h2>
<p style='font-size:16px;'>
<div style='text-align: center; font-size: 16px;'>
🧑‍💻 <b>Author:</b>  Zhe GUAN <br>
✉️ <b>Email:</b> <a href='mailto:zg2u24@soton.ac.uk'>zg2u24@soton.ac.uk</a>
</div>
</p>
<p>
The Dijkstra Algorithm is applied to search for the shortest path between two stations in a specified network <a href='https://data.worldbank.org/'>Details</a>.
</p>
""", unsafe_allow_html=True)
# Add some spacing
''
''

inf = np.inf
map_image_path = os.path.join(os.path.dirname(__file__), "test.png")
img = mpimg.imread(map_image_path)

img_width, img_height = 53.5709, (29)*1.8
plt.figure(figsize=(10, 8))
plt.imshow(img, extent=[0, img_width, 0, img_height])
st.pyplot(plt)

city_coordinates = {
    "Edinburgh": [55.9533, -3.1883],
    "London": [51.5074, -0.1278],
    "Madrid":  [40.4168,	-3.7038],
    "Rome":  [41.9028, 12.4964],
    "Budapest":  [47.4979, 19.0402],
    "Kyiv":  [50.4501, 30.5234],
    "Istanbul":  [41.0082, 28.9784],
    "Baku":  [40.4093, 49.8671],
    "Donetsk":  [48.0159, 37.8029],
    "Moscow":  [55.7558, 37.6173],
    "Saint Petersburg":  [59.9343, 30.3351],
    "Stockholm":  [59.3293, 18.0686],
    "Hamburg":  [53.5511, 9.9937],
    "Tromsø":  [69.6496, 18.9560],
    "Murmansk":  [68.9585, 33.0827],
    "Arkhangelsk":  [64.5399, 40.5152],
    "Ulyanovsk":  [54.3142, 48.4031],
    "Bergen":  [60.3913, 5.3221],
    "Oulu":  [65.0121, 25.4651]
}

network = {
    "Edinburgh": {"London": 1, "Bergen": 2, "Hamburg": 2},
    "London": {"Edinburgh": 1, "Hamburg": 1, "Madrid": 2, "Rome": 3},
    "Madrid": {"London": 2, "Rome": 4},
    "Rome": {"Madrid": 4, "Budapest": 1, "London": 3, "Hamburg": 3, "Istanbul": 2},
    "Budapest": {"Rome": 1, "Stockholm": 3, "Istanbul": 2, "Hamburg": 2,"Kyiv": 1},
    "Kyiv": {"Budapest": 1, "Donetsk": 1, "Stockholm": 3, "Saint Petersburg":2, "Moscow": 1, "Istanbul": 2 },
    "Istanbul": {"Budapest": 2, "Baku": 3, "Rome": 2, "Kyiv": 2,"Donetsk": 2},
    "Baku": {"Istanbul": 3,"Donetsk": 2,"Ulyanovsk": 6},
    "Donetsk": {"Kyiv": 1, "Moscow": 1, "Istanbul": 2, "Baku": 2, "Ulyanovsk":2 },
    "Moscow": {"Donetsk": 1, "Ulyanovsk": 1, "Saint Petersburg": 1,"Kyiv": 1, "Arkhangelsk":3},  # Ulyanovsk 是加粗线路
    "Saint Petersburg": {"Moscow": 1, "Stockholm": 2, "Oulu": 1, "Kyiv": 2, "Arkhangelsk":2 },
    "Stockholm": {"Saint Petersburg": 2, "Hamburg": 2, "Oulu": 2, "Budapest": 3 , "Kyiv": 3},  # Oulu 是加粗线路
    "Hamburg": {"Stockholm": 2, "London": 1, "Edinburgh": 2, "Rome": 3,"Budapest": 2,  "Bergen": 2 },
    "Tromsø": {"Murmansk": 2, "Bergen":4, "Oulu": 2},
    "Murmansk": {"Tromsø": 2, "Arkhangelsk": 2, "Oulu": 4},
    "Arkhangelsk": {"Murmansk": 2, "Ulyanovsk": 4, "Moscow": 3, "Saint Petersburg": 2,"Oulu":2 },
    "Ulyanovsk": {"Arkhangelsk": 4, "Moscow": 1, "Donetsk":2,  "Baku": 6 },  # Moscow 和 Arkhangelsk 是加粗线路
    "Bergen": {"Edinburgh": 2, "Stockholm": 2, "Hamburg":2, "Tromsø": 4, "Oulu": 4},
    "Oulu": {"Stockholm": 2, "Murmansk": 4, "Tromsø":2, "Saint Petersburg":1, "Arkhangelsk":2,  "Bergen": 4 }
}

df = pd.DataFrame(network)
sorted_df = df.sort_index(axis=0).sort_index(axis=1)

uploaded_file = st.file_uploader("Choose a CSV file to upload, otherwise default network will be used:", type="csv")
upload_settings = st.checkbox(
    "index names included",
    help="Check this box when the index names are included in your csv files :)"
)

if uploaded_file is not None:
    if upload_settings:
        data = pd.read_csv(uploaded_file, index_col=0)
    elif not upload_settings:
        data = pd.read_csv(uploaded_file)
        data = data.reset_index(drop=True)
        data = data.drop(data.columns[0], axis=1)
        data.columns = range(data.shape[1])

    st.write("Uploaded CSV Data:")
    st.dataframe(data)
    sorted_df = data.sort_index(axis=0).sort_index(axis=1)
    st.write("Check if uploaded network is bi-directional: ", check_symmtric(sorted_df))
    if check_symmtric(sorted_df) is False:
        st.write("Please double check the network uploaded which should be symmetrical :)")

sorted_df = sorted_df.fillna(float('inf'))
np_network = np.array(sorted_df) #transform to an array for better efficiency

#define varibales


countries = sorted([i for i in sorted_df.columns])

if not len(countries):
    st.warning("Select at least one country")

start_station = st.selectbox(
    'Which station would you start?',
    countries,
    index=0)

end_station = st.selectbox(
    'Which station would you end?',
    countries,
    index=1)

st.write(f'You selected the journey from **{start_station}** to **{end_station}**')

n = len(np_network)
start_point = sorted_df.index.get_loc(start_station)
end_point = sorted_df.index.get_loc(end_station)

previous, dist = calc_dis_path(n, start_point, end_point)
allpath = find_pathes(previous, end_point)
with_min_transfer_path = []
transfer_times = inf

st.write("**All Shortest Paths:**")
for i, path in enumerate(allpath):
    st.write(f"&nbsp;&nbsp;**{i}.** "+" -> ".join(map(str, sorted_df.columns[path])))
    st.write(f"&nbsp;&nbsp;The total travel time: {dist[end_point]}h")
    if len(allpath[i]) < transfer_times:
        transfer_times =  len(allpath[i])

st.write("---------------------------------------------------------------------------")

with_min_transfer_path = [i for i in allpath if transfer_times == len(i)]

transfer_times_settings = st.checkbox(
    "Prefer minimum number of transfers",
    help="Check this box when you prefer the path with the minimum number of transfers :)"
)

if transfer_times_settings:
    st.write("**BEST** Choice(s):")
    for best_path in with_min_transfer_path:
        st.write("->".join(map(str, sorted_df.columns[best_path])))

lowest_price_settings = st.checkbox(
    "Prefer lowest price with solid price",
    help="Check this box when you prefer the lowest price to travel:)                                              "
         "\n **NOTE: This function is only available for local runs as the ticket price is automatically retrieved in real-time from the KAYAK website.**"
)

airport_codes = {
    "Edinburgh": "EDI",
    "London": "LHR",
    "Madrid": "MAD",
    "Rome": "FCO",
    "Budapest": "BUD",
    "Kyiv": "KBP",
    "Istanbul": "IST",
    "Baku": "GYD",
    "Donetsk": "DOK",
    "Moscow": "SVO",
    "Saint Petersburg": "LED",
    "Stockholm": "ARN",
    "Hamburg": "HAM",
    "Tromsø": "TOS",
    "Murmansk": "MMK",
    "Arkhangelsk": "ARH",
    "Ulyanovsk": "ULV",
    "Bergen": "BGO",
    "Oulu": "OUL"
}

under_war = ["KBP", "DOK", "SVO", "LED","MMK", "ARH", "ULV"]
formatted_routes = []
total_price = 0


progress_bar = st.progress(0)
status = st.empty()
if lowest_price_settings:

    st.write("We are trying to find the lowest prices...")
    for path in allpath:
        cities = sorted_df.columns[path]
        airport_list = [airport_codes[city] for city in cities]
        st.write(f"&nbsp;&nbsp;**{i}.** " + " -> ".join(map(str, sorted_df.columns[path])))
        if any(item in airport_list for item in under_war):
            st.write("**ATTENTION:** Due to the ongoing war, some airports selected are currently unavailable in the function:(    "
                     "\n:earth_asia: **Hope for world peace!!**")
            break
        for i in range(len(airport_list) - 1):
            progress_bar.progress(i)
            formatted_routes.append(f"{airport_list[i]}-{airport_list[i + 1]}")
            total_price += find_lowest_price1(city_pair=f"{airport_list[i]}-{airport_list[i + 1]}")
            progress_bar.progress(int(100*(i+1)/(len(airport_list) - 1)))
            status.write(f" {100*(i+1)/(len(airport_list) - 1)}% complete")

        st.write("*Total prices* $",f"{total_price}")




