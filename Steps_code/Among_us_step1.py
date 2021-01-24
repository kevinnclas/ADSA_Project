# -*- coding: utf-8 -*-
"""
Created on Mon Nov  9 19:46:40 2020

@author: ikhla
"""
import random
import string
import operator
import statistics
import time

N = 100

def random_pseudo():
    # create 5 randoms character to create pseudo
    return ''.join(random.choice(string.ascii_letters) for x in range(5))
  
def random_score(): 
    return random.randint(0,12)

# Recursive function to compute the height of a node
def Height(root):
    if root == None : return 0
    elif root.right == None and root.left == None:
        return 0
    else : return max(Height(root.left),Height(root.right)) + 1
    
class Player:
    def __init__(self):
        self.pseudo = random_pseudo()
        # list in which we will stock scores for compute the mean
        self.all_score = [] 
        self.score = 0
    
    def __str__(self):
        return '{} : {}'.format(self.pseudo, self.score) 

# for update score we append the new score in the score's list and
# we compute the mean of all scores in the list.
    def update_score(self):
        rand_score = random_score()
        self.all_score.append(rand_score)
        self.score = round(statistics.mean(self.all_score),2)
               
    def Reset_score(self):
        self.score = 0
        self.all_score = []
            
class Node :
    def __init__(self, data, right = None, left = None):
        self.data = data # in our case, data is a player
        self.right = right
        self.left = left
    
    # add a right child
    def ADD_r(self, data):
        N = Node(data)
        self.right = N
     
    # add a left child
    def ADD_l(self, data):
        N = Node(data)
        self.left = N
    
    # compute the balance factor of a tree
    def compute_balance(self):
        height_left = 0 if self.left == None else Height(self.left) + 1
        height_right = 0 if self.right == None else Height(self.right) + 1
        return height_left - height_right
        
    # Right rotation in a AVL Tree
    def right_rotate(self):
        tmp = self.left.right
        right_node = Node(self.data, self.right, tmp)
        self.data = self.left.data 
        self.left = self.left.left
        self.right = right_node
      
    # Left rotation in a AVL Tree
    def left_rotate(self):
        tmp = self.right.left 
        left_node = Node(self.data, tmp, self.left) 
        self.data = self.right.data
        self.right = self.right.right
        self.left = left_node

    # drop the ten last player after a round of party
    def Drop(self):
        tmp = self.right.left
        self.data = self.right.data
        self.right = self.right.right
        self.left = tmp
      
    # Functions for display a tree (from DVO)    
    def display(self):
        lines, *_ = self._display_aux()
        for line in lines:
            print(line)

    def _display_aux(self):
        """Returns list of strings, width, height, and horizontal coordinate of the root."""
        # No child.
        if self.right is None and self.left is None:
            line = '%s' % self.data
            width = len(line)
            height = 1
            middle = width // 2
            return [line], width, height, middle

        # Only left child.
        if self.right is None:
            lines, n, p, x = self.left._display_aux()
            s = '%s' % self.data
            u = len(s)
            first_line = (x + 1) * ' ' + (n - x - 1) * '_' + s
            second_line = x * ' ' + '/' + (n - x - 1 + u) * ' '
            shifted_lines = [line + u * ' ' for line in lines]
            return [first_line, second_line] + shifted_lines, n + u, p + 2, n + u // 2

        # Only right child.
        if self.left is None:
            lines, n, p, x = self.right._display_aux()
            s = '%s' % self.data
            u = len(s)
            first_line = s + x * '_' + (n - x) * ' '
            second_line = (u + x) * ' ' + '\\' + (n - x - 1) * ' '
            shifted_lines = [u * ' ' + line for line in lines]
            return [first_line, second_line] + shifted_lines, n + u, p + 2, u // 2
            # Two children.
        left, n, p, x = self.left._display_aux()
        right, m, q, y = self.right._display_aux()
        s = '%s' % self.data
        u = len(s)
        first_line = (x + 1) * ' ' + (n - x - 1) * '_' + s + y * '_' + (m - y) * ' '
        second_line = x * ' ' + '/' + (n - x - 1 + u + y) * ' ' + '\\' + (m - y - 1) * ' '
        if p < q:
            left += [n * ' '] * (q - p)
        elif q < p:
            right += [m * ' '] * (p - q)
        zipped_lines = zip(left, right)
        lines = [first_line, second_line] + [a + u * ' ' + b for a, b in zipped_lines]
        return lines, n + m + u, max(p, q) + 2, n + u // 2


# We compare the new player score with the score of players presents in
# the Tree. If the new player has a smaller score, we apply the 
# function on the left child of the current node and on the right one
# if the score is higher. We make it until the node is inserted.
def Insert_AVL(root, player):
    
    if root == None : return Node(player)
    elif root.data.score <= player.score : root.right = Insert_AVL(root.right, player)
    else : root.left = Insert_AVL(root.left, player)
    
    # Then we compute the balance factor of the current subtree and fix it
    # if it's not between -1 and 1. (AVL Tree condition) We go back up on
    # the tree until we come back to the root.
    balance = root.compute_balance()
    
    if balance < -1 : 
        if player.score >= root.right.data.score : 
            root.left_rotate()
        else :
            root.right = root.right_rotate()
            root.left_rotate()
    
    elif balance > 1:
        if player.score <= root.left.data.score : 
            root.right_rotate()
        else:
            root.left = root.left_rotate()
            root.right_rotate()
        
    return root

# We add a new node with the player instance on right if the score is
# higher or equal than the current node and on the left if it is not.
def Insert_BST(Tree, player):
    
    current = Tree
    if player.score >= current.data.score :
        if current.right == None:
            current.ADD_r(player)
        else : Insert_BST(current.right, player)
    elif player.score <= current.data.score :
        if current.left == None:
            current.ADD_l(player)
        else : Insert_BST(current.left, player)

# Creation of the database for the tournament            
def Create_BST(list_player):
    # We sort the player by their score in ascending order
    list_player.sort(key=operator.attrgetter('score'))
    # We compute the index of the root node (the player with the best score
    # between those who will be ejected)
    root_index = int((N/10)-1)
    root = Node(list_player[root_index])
    # On root2 we will construct the avl tree, those who will continue.
    root2 = None
    for i in range(len(list_player)):
        if list_player[i] == root.data : continue #don't add the root twice
        # We add the ten last players on the left of the root.
        if i < root_index :
            if root.left == None : root.ADD_l(list_player[i])
            else: Insert_BST(root.left, list_player[i])
        else : 
            root2 = Insert_AVL(root2, list_player[i])
    # Then we add the AVL Tree on the right of the root.
    root.right = root2
    return root        

# For each player in the list, we will update the score 3 times for
# simulate 3 games.    
def Play_3_games(list_players):
    
    for player in list_players : 
        player.update_score()
        player.update_score()
        player.update_score()

# An Inorder traversal who put player of the tree in a list
def In_Order(root, ranking=[]):
    if root:
        In_Order(root.left, ranking) 
        ranking.append(root.data)
        In_Order(root.right, ranking) 
        
# A function for compose different rooms (represented by list)
# of ten players.        
def Ranking_games(root) :   
    l = []
    In_Order(root,l)
    return [l[i:i+int(N/10)] for i in range(0,len(l),int(N/10))]


# Function which compute different games until there is the ten last player    
def Play():
    Tree = Create_BST([Player() for i in range(N)])
    print('\n')
    count = 0
    print('This is the first initialization of the the tournament, everyone begin at 0, so be the best to see yourself in the top of the ranking !')
    Tree.display()
    time.sleep(4)
    counterround = 1
    while(count <= 8):
        print('This is the state of the tournament at the step {} :'.format(counterround))
        time.sleep(2)
        All_room = Ranking_games(Tree)
        for room in All_room : Play_3_games(room)
        Tree = Create_BST([player for room in All_room for player in room])
        print('\n')
        Tree.display()
        print('\n')
        Tree.Drop()
        time.sleep(2)
        print('The 10 last players are eliminated and we have our remaining players for the next round ! \n')
        time.sleep(2)
        Tree.display()
        #if Tree.right != None : Tree.right.display()
        print('\n')
        count += 1
        counterround += 1
        time.sleep(3)
    return Tree

# Function for the five last games which determine the top 10
def Final(Tree):
    L_final = []
    In_Order(Tree,L_final)
    for player in L_final :
        player.Reset_score()
        for i in range(5) : player.update_score()
    Tree = Create_BST(L_final)
    print("The tournament has reached its end ! Let's see the final ranking of our finalists ! \n")
    time.sleep(2)
    j = 0
    for i in range(10,3,-1) :
        print('At the {}th position, we have : {} with a score of {}'.format(i, L_final[j].pseudo, L_final[j].score))
        j += 1
        time.sleep(2)
    print()        
    print("Now the moment you've all been waiting for, the podium of the tournament ! \n")
    time.sleep(3)
    print('At the 3rd position, we have {} with a score of {} !'.format(L_final[7].pseudo, L_final[7].score))
    time.sleep(4)
    print('At the 2nd position, we have {} with a score of {} ! \n'.format(L_final[8].pseudo, L_final[8].score))
    time.sleep(4)
    print('And finaly, the winner of the tournament ! \n')
    time.sleep(2)
    print('With a score of {}, the winner of the Among Us tournament of the ZLAN is ...'.format(L_final[9].score))
    time.sleep(4)
    print('\t {} !!! \n'.format(L_final[9].pseudo))
    time.sleep(2)
    print('Congratulations to all ! See you next year !')

    
if __name__ == '__main__':
    print('Welcome to the Among Us tournament of the ZLAN ! \n')
    time.sleep(3)
    print('Here are some of the rules : ')
    time.sleep(2)
    print('\t - 100 players')
    time.sleep(2)
    print('\t - 10 players per room')
    time.sleep(2)
    print('\t - 3 random games for each round between the players of one room \n')
    time.sleep(3)
    print('The last 10 players will face each other during 5 random games and the final ranking will be given with our great winner ! \n')
    time.sleep(5)
    print("So let's jump into it !")
    time.sleep(2)
    
    tree = Play()
    
    print('Wow ! Congratulations on making it to the finals ! Now, you will face each other during 5 random games and the final ranking will be given ! Good luck ! \n')
    time.sleep(5)
    
    Final(tree)
    
    