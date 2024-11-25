import streamlit as st
import numpy as np
import pandas as pd
import math
from pathlib import Path
import matplotlib.pyplot as plt
import matplotlib.image as mpimg

# Set the title and favicon that appear in the Browser's tab bar.
st.set_page_config(
    page_title='Pathes dashboard',
    page_icon=':earth_asia:', # This is an emoji shortcode. Could be a URL too.
)

# -----------------------------------------------------------------------------
# Declare some useful functions.

@st.cache_data
def get_gdp_data():
    """Grab GDP data from a CSV file.

    This uses caching to avoid having to read the file every time. If we were
    reading from an HTTP endpoint instead of a file, it's a good idea to set
    a maximum age to the cache with the TTL argument: @st.cache_data(ttl='1d')
    """

    # Instead of a CSV on disk, you could read from an HTTP endpoint here too.
    DATA_FILENAME = Path(__file__).parent/'data/gdp_data.csv'
    raw_gdp_df = pd.read_csv(DATA_FILENAME)

    MIN_YEAR = 1960
    MAX_YEAR = 2022

    # The data above has columns like:
    # - Country Name
    # - Country Code
    # - [Stuff I don't care about]
    # - GDP for 1960
    # - GDP for 1961
    # - GDP for 1962
    # - ...
    # - GDP for 2022
    #
    # ...but I want this instead:
    # - Country Name
    # - Country Code
    # - Year
    # - GDP
    #
    # So let's pivot all those year-columns into two: Year and GDP
    gdp_df = raw_gdp_df.melt(
        ['Country Code'],
        [str(x) for x in range(MIN_YEAR, MAX_YEAR + 1)],
        'Year',
        'GDP',
    )

    # Convert years from string to integers
    gdp_df['Year'] = pd.to_numeric(gdp_df['Year'])

    return gdp_df

def check_symmtric(sorted_df):
    difference_no_nan = (sorted_df != sorted_df.transpose()) & sorted_df.notna() & sorted_df.transpose().notna()

    asymmetric_elements_no_nan = difference_no_nan[difference_no_nan].stack()

    for index in asymmetric_elements_no_nan.index:
        original_value = sorted_df.loc[index]
        transpose_value = sorted_df.T.loc[index]
        print(f"Asymmetry at {index}: Original = {original_value}, Transpose = {transpose_value}")

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

gdp_df = get_gdp_data()

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

map_image_path = "/Users/zheguan/DDA/Python/test.png"
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

check_symmtric(sorted_df)

sorted_df = sorted_df.fillna(float('inf'))
np_network = np.array(sorted_df) #transform to an array for better efficiency

#define varibales


countries = sorted([i for i in network])

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
dist = [np.inf] * n #define shortest distance
visited = [False] * n #define visit status
previous = [[] for _ in range(n)]
#previous = [-1] * n #define mother point
start_point = sorted_df.index.get_loc(start_station)
dist[start_point] = 0
end_point = sorted_df.index.get_loc(end_station)

#st.write(start_point, "end: ", end_point )

print(dist)
print(visited)
print(previous)


# here start point = 3
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

allpath = find_pathes(previous, end_point)

st.write("All Paths:")
for path in allpath:
    st.write(" -> ".join(map(str, sorted_df.columns[path])))
    st.write(" The total travel time: ", dist[end_point], "h")

min_value = gdp_df['Year'].min()
max_value = gdp_df['Year'].max()

from_year, to_year = st.slider(
    'Which years are you interested in?',
    min_value=min_value,
    max_value=max_value,
    value=[min_value, max_value])


    #gdp_df['Country Code'].unique()





''
''
''

# Filter the data
filtered_gdp_df = gdp_df[
    (gdp_df['Country Code'].isin(selected_countries))
    & (gdp_df['Year'] <= to_year)
    & (from_year <= gdp_df['Year'])
]

st.header('GDP over time', divider='gray')

''

st.line_chart(
    filtered_gdp_df,
    x='Year',
    y='GDP',
    color='Country Code',
)

''
''


first_year = gdp_df[gdp_df['Year'] == from_year]
last_year = gdp_df[gdp_df['Year'] == to_year]

st.header(f'GDP in {to_year}', divider='gray')

''

cols = st.columns(4)

for i, country in enumerate(selected_countries):
    col = cols[i % len(cols)]

    with col:
        first_gdp = first_year[first_year['Country Code'] == country]['GDP'].iat[0] / 1000000000
        last_gdp = last_year[last_year['Country Code'] == country]['GDP'].iat[0] / 1000000000

        if math.isnan(first_gdp):
            growth = 'n/a'
            delta_color = 'off'
        else:
            growth = f'{last_gdp / first_gdp:,.2f}x'
            delta_color = 'normal'

        st.metric(
            label=f'{country} GDP',
            value=f'{last_gdp:,.0f}B',
            delta=growth,
            delta_color=delta_color
        )
