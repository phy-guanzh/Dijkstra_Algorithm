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
from classes.streamlit_class import *

from selenium import webdriver
from bs4 import BeautifulSoup

inf = np.inf


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

@st.cache_data
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

@st.cache_data
def calc_dis_path(n, start_point, end_point,np_network):
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

@st.cache_data
def find_lowest_price(city_pair="EDI-LHR", start_date=datetime.today().strftime('%Y-%m-%d')):
    origin, destination = city_pair.split("-")

    driver = webdriver.Chrome()

    driver.get(f"https://www.kayak.com/flights/{origin}-{destination}/{start_date}?ucs=8liajb&sort=price_a")

    time.sleep(20)

    content = driver.page_source

    soup = BeautifulSoup(content, 'html.parser')

    prices = []
    for div in soup.findAll('div', attrs={'class': 'f8F1-price-text'}):
        price_text = div.text.strip()  
        if price_text.startswith('$'):
            price = int(price_text[1:])  
            prices.append(price)
    driver.quit()
    if prices:
        min_price = min(prices)
        st.write(f"The minimum price of {city_pair} on {start_date} is: ${min_price}")
        return min_price
    else:
        st.write(f"No prices found for {city_pair} on {start_date}")
        return None


