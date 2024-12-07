import argparse
from classes.Dijkstra_class import *

def Dijktra_main():

    print(f'Welcome Dijktra Algorithm')
    parser = argparse.ArgumentParser(description='map information, start_point and possible end_point')

    parser.add_argument('-f', '--file_path', default='data/network.csv', help='input the csv map path')
    parser.add_argument('-s', '--start_point', help='input the start point in the map')
    parser.add_argument('-e','--end_point', default='all', help = 'Input the end point in the map. Default: all')

    args = parser.parse_args()
    file_path = args.file_path
    start_point = args.start_point
    end_point = args.end_point

    try:
        df = pd.read_csv(file_path, index_col=0)
        print("Map will be processed: \n",df.sort_index(axis=0))
    except FileNotFoundError:
        print(f'Map {file_path} Not Found.')
        exit(1)
    except Exception as e:
        print(f"Error loading map: {e}")
        exit(1)

    Dijkstra.find_shortest_path(df, start_point, end_point)

if __name__ == '__main__':
    Dijktra_main()


