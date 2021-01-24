# -*- coding: utf-8 -*-
"""
Created on Mon Nov 30 21:33:08 2020

@author: ikhla
"""
#for each player, we put who they saw during the game
Graph = {1 : [2,6],
         2 : [1,3,7],
         3 : [2,4,8],
         4 : [3,9],
         5 : [7,8],
         6 : [1,8,9],
         7 : [2,5,9],
         8 : [3,5,6],
         9 : [4,6,7]
           }

#allow us to know the degree for each node and sort it in descending order after
Node_n_degree = [(i, len(Graph[i])) for i in range(1,10)]
Node_n_degree.sort(key= lambda x : x[1], reverse=True)

#we create a list with all the nodes 
Node_color = { i : None for i in range(1,10)}
#we will only need 3 colors
Colors = ['red','green','blue']

#we want to give each player a color in function of their link between each others
for color in Colors :
    #check if every node has a color
    if None not in Node_color.values() : break
    for i in range(1,10):
        if Node_color[i] != None : continue
        available = True
        for j in Graph[i]:
            if Node_color[j] == color : 
                available = False
                break
        if available == True : Node_color[i] = color
  
print("Alert ! A body has just been discovered and it's player 0 !")
print("We know that he saw players 1, 4 and 5 so one of them must be an impostor ! \n")    
# The first impostor is 1 OR 4 OR 5 so 1 and 4 can't be a set of impostor for example
set_impostor = {1,4,5}

print("The second impostor doesn't have the color of the players that saw the first impostor (according to the Welsh-Powell's Algorithm) \n")

#we show the colors of all the players
print('Here are the colors attributed to the players : ')
for col in Colors:
    print(col, end=' : ')
    for i in Node_color : 
        if (Node_color[i]==col) : print(i,end =' ')
    print()

#we show the possibilities for the couple of impostors   
print("\nAt the end, we have those possibilites for the couple of impostors : \n")
for i in (set_impostor):
    for j in range(1,10):
        if not(i in set_impostor and j in set_impostor):
            if (Node_color[j] != Node_color[Graph[i][0]]):
                print('\t{} and {} can be the impostors.'.format(i,j))
    print()            
print("So now, let's vote !")