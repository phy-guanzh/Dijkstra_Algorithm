import argparse
from classes.Dijkstra_class import *

def Dijktra_main():

    print(f'**Welcome to Dijktra Algorithm tool**')
    parser = argparse.ArgumentParser(description='inputs can be: map path, start_point and end point')

    parser.add_argument('-f', '--file_path', default='data/network.csv', help='the csv map path')
    parser.add_argument('-s', '--start_point', help='the start point in the map')
    parser.add_argument('-e','--end_point', default='all', help = 'the end point in the map. Default: all')
    parser.add_argument('-u', '--unit', default='h', help='the unit of cost. Default: time h')

    args = parser.parse_args()
    file_path = args.file_path
    start_point = args.start_point
    end_point = args.end_point
    unit = args.unit

    try:
        df = pd.read_csv(file_path, index_col=0)
        print("Map below will be processed: \n",df.sort_index(axis=0))
    except pd.errors.ParserError:
        df = pd.read_excel(file_path, index_col=0)
        print("Map loaded as Excel:\n", df.sort_index(axis=0))
    except FileNotFoundError:
        print(f'Map {file_path} Not Found.')
        exit(1)
    except Exception as e:
        print(f"Error loading map: {e}")
        exit(1)

    Dijkstra.find_shortest_path(df, start_point, end_point, unit)

if __name__ == '__main__':
    Dijktra_main()


