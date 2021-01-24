# -*- coding: utf-8 -*-
"""
Created on Wed Dec  2 22:51:23 2020

@author: ikhla
"""
#import of the libraries, pandas for the import and the lecture of the dataset in the excel file,
#numpy for mathematics uses and for arrays and finally time for better lecture during the test of the code
import numpy as np
import pandas as pd
import time

#we will use infinity value so we create it at the beginning
INF = np.inf

#creation of the Floyd Warshall algorithm with the Map of the game entered in parameter
#were we want to return the shortest path with all the rooms
def Floyd_Warshall_Algo(Map):
    #number of nodes in the Grap
    V = Map.shape[0]
    #we initialize the matrix with infinity value
    M = np.full((V,V), INF)
    
    # For each cell in M, we put a 0 if it is on the left downward diagonal
    # And the weight value if there is a link between the two vertices
    for i in range(V):
        for j in range(V):
            if i == j : M[i,j] = 0
            elif Map[i,j] == '∞' : continue
            elif M[i,j] > Map[i,j] and Map[i,j] != 0 : 
                M[i,j] = Map[i,j]
    
    # We are computing the shortest path from each node to the others
    for k in range(V):
        for i in range(V):
            for j in range(V):
                M[i,j] = min(M[i,j], M[i,k] + M[k,j])
    return M
 
#creation of the graph with an adjacency matrix created in an excel file
def link_rooms_dataframe(excel_path):
    dataframe = pd.read_excel(excel_path)
    dataframe.rename(columns= {'Unnamed: 0' : 'Room'}, inplace=True)
    dataframe.index = dataframe.iloc[:,0]
    dataframe.drop('Room', axis=1, inplace=True)

    #the graph takes for values for each vertex the values of the dataframe
    Graph = dataframe.values
    #we apply the Floyd Warshall Algorithm on our graph and we store the result in a variable
    Floyd_result = Floyd_Warshall_Algo(Graph)
    #we store the result in a dataframe with the rooms' names and their link values
    final_dataframe = pd.DataFrame(data = Floyd_result, index = dataframe.index, 
                        columns = dataframe.columns)
    return final_dataframe
    
#calculation of the time taken to travel from a room to another  
def time_to_travel(excel_crewmate, excel_impostor):
    #we store in 2 different dataframes the time it takes to travel between 2 rooms for an impostor and a crewmate
    df = link_rooms_dataframe(excel_crewmate)
    df2 = link_rooms_dataframe(excel_impostor)
    
    print('Where did the murder take place ?')
    roommurder = str(input())
    print()
    print('In which room are you actually ?')
    actualroom = str(input())
    print()
    
    #depending the murder room and the actual player room, 
    #we display the time it would have taken for an impostor and a crewmate to travel between those 2 rooms
    timetravel = df.loc[roommurder,actualroom]
    timetravel2 = df2.loc[roommurder,actualroom]
    print('This would have taken you {} seconds for you to travel from {} to {} if you were truelly a crewmate'.format(timetravel, roommurder, actualroom))
    print('For an impostor, going from {} to {} would take aproximatively {} seconds'.format(roommurder, actualroom, timetravel2))
    print()

#display the interval of time for each pair of room where the traveler is an impostor    
def room_impostor(excel_impostor):
    df = link_rooms_dataframe(excel_impostor)
    print()
    
    print('We want to display the interval of time to travel between each pair of rooms for an impostor. From which room do you want to start ?')
    roomstart = str(input())
    print()
    #depending on what we enter for the room, we display the time it takes for an impostor to travel between this room and all the other ones
    for i in df.columns:
        timetotravel = df.loc[roomstart,i]
        print('{} to {} : {} seconds'.format(roomstart, i, timetotravel))        

    
if __name__ == '__main__':
    time_to_travel('Step-3-weight-between-rooms-crewmate.xlsx', 'Step-3-weight-between-rooms-impostor.xlsx')
    time.sleep(2)
    room_impostor('Step-3-weight-between-rooms-impostor.xlsx')
    time.sleep(2)
    
    #we want to display the adjacency matrix of the links between rooms for a crewmate and for a impostor
    dataframe_c = link_rooms_dataframe('Step-3-weight-between-rooms-crewmate.xlsx')
    print('\n\tFor the crewmates,')
    print('\n\tHere is the matrix on which we have the minimum time to go',
          'from a room to another :', end='\n\n')
    print(dataframe_c.to_string())
    
    dataframe_i = link_rooms_dataframe('Step-3-weight-between-rooms-impostor.xlsx')
    print('\n\tFor the impostors,')
    print('\n\tHere is the matrix on which we have the minimum time to go',
          'from a room to another :', end='\n\n')
    print(dataframe_i.to_string())