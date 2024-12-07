import pandas as pd
import numpy as np


class Dijkstra:

    @staticmethod
    def _input(df: pd.DataFrame, start_point: str) -> tuple[dict, list, dict, dict]:
        '''
        provide the necessary initial variables for further calculations
        output: Ys, S, P, Pre
        '''
        
        if not start_point:
            print("Error: Invalid start_point detected! Use -h for more information.")
            exit(1)
        
        #add the index of rows
        df = df.sort_index(axis=0)
        inf = np.inf
        
        #define variables
        Ys = {item: inf for item in df.columns}
        Ys[start_point] = 0
        S = [start_point]
        P = {item: [] for item in df.columns}  # define a path which starts from start point
        P[start_point].append(start_point)
        Pre = {item: [] for item in df.columns}  # define a path which starts from start point

        return Ys, S, P, Pre

    @staticmethod
    def _find_sigma_s(df_path: pd.DataFrame, S: list) -> list:
        '''
        Return all possible pathes from a visited point from S to an un-visited point.
        Output: sigma_s
        '''

        # find all pairs where one is from S and the other one not from S
        sigma_s = [
            [i, j]
            for i in S
            for j in df_path.columns
            if j not in S
               and not pd.isna(df_path.loc[i, j])
        ]

        return sigma_s

    @staticmethod
    def _find_cloest_outpoints(df_path: pd.DataFrame, sig_s: list, Ys: dict) -> tuple[list, list]:
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
        Y = [Ys[i] for i, j in sig_s]
        Y_lij = list(map(lambda x, y: x + y, Y, l_tmp))
        
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
            sub_paths = Dijkstra._find_P(Pre, i)
            for path in sub_paths:
                P.append([K] + path)

        return P

    @staticmethod
    def find_shortest_path(df: pd.DataFrame, start_point: str, end_point: str = 'all') -> list:
        '''
        find and return the shortest path(es)
        output:list
        '''
        
        #call initial variable function
        Ys, S, P, Pre = Dijkstra._input(df, start_point)
        
        #loop process below until all points are in visited sets S 
        while not all(col in S for col in df.columns):

            sig_s = Dijkstra._find_sigma_s(df, S)

            cloest_sets, cloest_distance = Dijkstra._find_cloest_outpoints(df, sig_s, Ys)

            Pre, Ys, S = Dijkstra._update_Pre_Y_S(Pre, Ys, S, cloest_sets, cloest_distance)

        # if end_point is not specified, print all paths from start point 
        points_end = (
            [end_point] if isinstance(end_point, str)
            else df.columns if end_point == 'all'
            else end_point
        )

        P = {i: Dijkstra._find_P(Pre, i) for i in points_end}
        Ys = {i : Ys[i] for i in Ys if i in points_end}

        #define the output format
        output = [
            (
                f'Start Point: {start_point} \n'
                f'End Point: {item} \n'
                f'Time: {Ys[item]}, \n'
                f'Path: {" or ".join("->".join(item2[::-1]) for item2 in P[item])} \n'
            )
            for item in points_end
        ]
        
        #print the output
        for line in output:
            print(line)

        return True



