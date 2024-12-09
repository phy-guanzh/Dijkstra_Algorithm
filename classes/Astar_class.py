import pandas as pd
import numpy as np
import math


class Astar:

    @staticmethod
    def _input(df: pd.DataFrame, df_h: pd.DataFrame,  start_point: str) -> tuple[dict, list, dict, dict]:
        '''
        provide the necessary initial variables for further calculations
        output: Ys, S, P, Pre
        '''
        
        if not start_point:
            print("Error: Invalid start_point detected! Double check the name or use -h for more information.")
            exit(1)
        
        #add the index of rows
        df = df.sort_index(axis=0)
        inf = np.inf
        
        #define variables
        Ys = {item: inf for item in df.columns} #distance from start point to point 'item'
        Ys[start_point] = 0
        S = [start_point] # define a set S which contains all visited points
        H = Astar._input_h(df_h, start_point)

        P = {item: [] for item in df.columns}  # P is used to store the shortest paths
        P[start_point].append(start_point)
        Pre = {item: [] for item in df.columns}  # define dic Pre which stores the previous point before point 'item'

        return Ys, S, P, Pre, H

    @staticmethod
    def _input_h(df_h, start_point):

        city_col = 'name'
        latitude_col = 'lat'
        longitude_col = 'long'

        df = df_h

        start_coords = df[df[city_col] == start_point][[latitude_col, longitude_col]].iloc[0]

        H = {}
        for index, row in df.iterrows():
            city = row[city_col]
            if city == start_point:
                H[city] = 0
            else:
                distance = Astar._flat_distance(
                    start_coords[latitude_col], start_coords[longitude_col],
                    row[latitude_col], row[longitude_col]
                )
                H[city] = distance
        return H

    @staticmethod
    def _flat_distance(lat1, lon1, lat2, lon2):
        """
        calculate the distance
        """

        lat_km = 111
        lon_km = 111 * math.cos(math.radians((lat1 + lat2) / 2))

        delta_lat = lat1 - lat2
        delta_lon = lon1 - lon2

        return math.sqrt((delta_lat * lat_km) ** 2 + (delta_lon * lon_km) ** 2)

    @staticmethod
    def _find_sigma_s(df_path: pd.DataFrame, S: list) -> list:
        '''
        Return all possible pathes from a visited point from S to an un-visited point.
        Output: sigma_s
        '''

        # find all pairs where one is from S and the other one is not from S
        sigma_s = [
            [i, j]
            for i in S
            for j in df_path.columns
            if j not in S
               and not pd.isna(df_path.loc[i, j]) #the path should exist
        ]

        return sigma_s

    @staticmethod
    def _find_cloest_outpoints(df_path: pd.DataFrame, sig_s: list, Ys: dict, H: dict) -> tuple[list, list]:
        '''
        return a list which may contain several cloest outpoints
        output: l_cloest
        eg:[['A','D'],['B','E']]
        '''
        
        if not sig_s:
            print("No futher outter points. Exiting function.")
            return [],[]
        
        #calucate l_ij and Y_lij 
        l_tmp = [df_path.loc[i, j] for i, j in sig_s]
        f_tmp = [df_path.loc[i, j]+ H[j] for i, j in sig_s]
        Y = [Ys[i] for i, j in sig_s]
        Y_lij = list(map(lambda x, y: x + y, Y, f_tmp))
        
        #find the shortest path index from Y_lij
        index_cloest = np.where(np.array(Y_lij) == min(Y_lij))[0]
        #index_cloest = [i for i, value in enumerate(Y_lij) if value == min(Y_lij)]
        
        #store the pairs of shortest points which need to be updated.
        cloest_sets = [sig_s[i] for i in index_cloest]
        cloest_distance = [l_tmp[i] for i in index_cloest]

        return cloest_sets, cloest_distance

    @staticmethod
    def _update_Pre_Y_S(Pre: dict, Y: dict, S: list, cloest_sets: list, cloest_distance: list) -> tuple[
        list, list, list]:
        '''
        update Ys, P and S
        output: updated Ys, P, S
        '''
        
        # update dic Y
        Y.update({
            k: Y[j] + cloest_distance[i]
            for i, (j, k) in enumerate(cloest_sets)
        })
        
        # update previous point Pre
        for i, j in cloest_sets:
            Pre[j].append(i)

        # update visted points S
        for i, j in cloest_sets:
            if j not in S:
                S.append(j)

        return Pre, Y, S

    @staticmethod
    def _find_P(Pre: dict, K: str)->list:
        '''
        return the full shortest pathes based on previous point
        output: P
        '''
        
        #if Pre[K] is empty, it means K is our start_point
        if not Pre[K]:
            return [[K]]
        P = []
        
        # append previous point one by one by recalling _find_P function
        for i in Pre[K]:
            sub_paths = Astar._find_P(Pre, i)
            for path in sub_paths:
                P.append([K] + path)

        return P

    @staticmethod
    def find_shortest_path(df: pd.DataFrame, df_h: pd.DataFrame, start_point: str, end_point: str = 'all', unit: str = "h") -> list:
        '''
        find and return the shortest path(es)
        output:list
        '''

        if (end_point not in df.columns) and end_point != "all":
            print("Error: Invalid end_point detected! Double check the name or Use -h for more information.")
            exit(1)

        #call initial variable function
        Ys, S, P, Pre, H = Astar._input(df, df_h, start_point)

        # if end_point is not specified, print all paths from start point
        points_end = (
            df.columns if end_point == 'all'
            else [end_point] if isinstance(end_point, str)
            else end_point
        )
        #loop process below until all points are in visited sets S 
        while not all(col in S for col in points_end):
            #progress = len(S) / total_columns * 100
            #print(f'Progress: {progress:.2f}% ({len(S)}/{total_columns} columns processed)')
            sig_s = Astar._find_sigma_s(df, S)
            cloest_sets, cloest_distance = Astar._find_cloest_outpoints(df, sig_s, Ys, H)
            Pre, Ys, S = Astar._update_Pre_Y_S(Pre, Ys, S, cloest_sets, cloest_distance)

        print('\n')
        
        P = {i: Astar._find_P(Pre, i) for i in points_end}
        Ys = {i : Ys[i] for i in Ys if i in points_end}

        #define the output format
        output = [
            (
                f'Start Point: {start_point} \n'
                f'End Point: {item} \n'
                f'Time: {Ys[item]} h, \n'
                f'Path: {" or ".join("->".join(item2[::-1]) for item2 in P[item])} \n'
            )
            for item in points_end
        ]
        
        #print the output
        for line in output:
            print(line)

        return True



