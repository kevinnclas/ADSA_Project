# -*- coding: utf-8 -*-
"""
Created on Sun Dec  6 16:53:50 2020

@author: ikhla
"""
#import of the libraries, time for better lecture during the test of the code
#and pandas for the import and the lecture of the dataset in the excel file.
import time
import pandas as pd

#creation of the graph with an adjacency matrix created in an excel file
def Graph_creation():
    #reading of the file
    dataframe = pd.read_excel('Step-3-weight-between-rooms-crewmate.xlsx') 
    #renaming of the column of the romms
    dataframe.rename(columns= {'Unnamed: 0' : 'Room'}, inplace=True) 
    dataframe.index = dataframe.iloc[:,0] 
     #we just keep the values of the connexions between rooms
    dataframe.drop('Room', axis=1, inplace=True)

    Graph = dataframe.values
    #we have 13 rooms in total so V is equal to 14 columns
    V = Graph.shape[0] 
    
    for i in range(V):
        for j in range(V):
            #we want to replace all the ∞ by 0 in our new matrix
            if Graph[i,j] == '∞' : Graph[i,j] = 0 
    #we want to return the graph and the names of the rooms
    return Graph, dataframe.columns 
    
#observation of the neighbors that a vertex has
def Neighbors(G, vertex):
    neighbors = []
    for i in range(G.shape[1]):
        #if a room has a connexion value in the the column of another room, 
        #then they are neighbors and we had them to the list
        if G[vertex, i] != 0 : neighbors.append((i, G[vertex, i]))
    #we sort the list of neighbors in ascending order by their value
    neighbors = sorted(neighbors, key=lambda x: x[1])
    #we return the list of neighbors for our algorithm
    return neighbors

#Hamilton's Algorithm to find the quickest path to visit all the rooms by going through each room only once
def Hamilton(G, path, index):
    if index == G.shape[0] : return True
    #we want to get the neighbors' list of each vertex
    neighbors = Neighbors(G, path[index - 1])
    #we are looking for the neighbors of the actual room and if one neighbor is not already in the path, we add it
    for room in neighbors:
        if room[0] not in path :
            path[index] = room[0]
            if Hamilton(G, path, index + 1) == True:
                return True
            path[index] = -1      
    return False

#ask the player to select a room where to begin the tasksa and return if the path exists or not
def ChoosePath(G, Rooms, path):
    print('Choose a room number from where you want to begin the tasks !')
    print("Here is the list of the rooms to help you :")
    for i in range(14) :
        print("{} : {}".format(i, Rooms[i]))
    #selection of the player for the room where to begin the tasks
    roomchoose = int(input())
    path[0] = roomchoose
    print('You chose {}'.format(Rooms[roomchoose]))
    print()
    time.sleep(1)
    #call the algortihm to know if the path exists or not
    possible = Hamilton(G, path, 1)
    #if it exists, we show the path to follow and if not, we ask the player to enter a new room th begin with
    if possible == True:
        print("The path is possible ! Let see the path that we are going to do : \n")
        time.sleep(2)
        for i in path[:13]:
            print(Rooms[i], end = ' -> ')
        #we want the last room shown to not display an arrow after displaying it
        print(Rooms[path[13]])
    #in this following case, the plath doesn't exist
    else:
        print("Sorry, the path is not possible. Let's find another one ! \n")
        time.sleep(2)
        ChoosePath(G, Rooms, path)
        
        
if __name__ == "__main__" :
    #creation of the graph and we collect the rooms' names in a variable
    G, Rooms = Graph_creation()
    #we initiate the all path list of 14 values with -1
    path = [-1 for i in range(G.shape[0])]
    #we call the method that will display if the path wished by the player is possible or not
    ChoosePath(G, Rooms, path)