import argparse
from classes.Astar_class import *

def Astar_main():

    print(f'**Welcome to Astar* Algorithm tool**')
    parser = argparse.ArgumentParser(description='inputs can be: map path, start_point and end point')

    parser.add_argument('-f', '--file_path', default='data/network.csv', help='the csv map path')
    parser.add_argument('-w', '--heuristic', default='data/heuristic.csv', help='Requires a heuristic data path')
    parser.add_argument('-s', '--start_point', help='the start point in the map')
    parser.add_argument('-e','--end_point', default='all', help = 'the end point in the map. Default: all')
    parser.add_argument('-u', '--unit', default='h', help='the unit of cost. Default: time h')

    args = parser.parse_args()
    file_path = args.file_path
    heuristic = args.heuristic
    start_point = args.start_point
    end_point = args.end_point
    unit = args.unit

    try:
        df = pd.read_csv(file_path, index_col=0)
        df_h = pd.read_csv(heuristic)
        print("Map below will be processed: \n",df.sort_index(axis=0).head())
        print("Provided a heuristic data: \n", df_h.sort_index(axis=0).head())
    except pd.errors.ParserError:
        df = pd.read_excel(file_path, index_col=0)
        df_h = pd.read_csv(heuristic)
        print("Map loaded as Excel:\n", df.sort_index(axis=0).head())
        print("Provided a heuristic data: \n", df_h.sort_index(axis=0).head())
    except FileNotFoundError:
        print(f'Map {file_path} Not Found.')
        exit(1)
    except Exception as e:
        print(f"Error loading map: {e}")
        exit(1)

    Astar.find_shortest_path(df, df_h, start_point, end_point, unit)

if __name__ == '__main__':
    Astar_main()


