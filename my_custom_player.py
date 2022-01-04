
from sample_players import DataPlayer
#from monte_carlo_tree_search import MCTS
import random, math, copy, sys
#from mcts_node import Node

class CustomPlayer(DataPlayer):

    def get_action(self, state):
        if state.ply_count < 2:
            self.queue.put(random.choice(state.actions()))
        else:
            self.queue.put(self.monte_carlo_tree_search(state))

    def monte_carlo_tree_search(self, state):
        mcts = MCTS()
        rootnode = Node(state)
        epoch = 5
        while epoch >=0:
            epoch-=1
            if rootnode.state.terminal_test():
                return random.choice(state.actions())
            child = mcts.selection(rootnode)
            reward = mcts.simulation(child.state)
            mcts.backpropagation(child, reward)
        indx = rootnode.childs.index(mcts.best_child_node(rootnode))
        acts= rootnode.childs_action[indx]
        return acts




class MCTS:
    """ 
    Class for Monte Carlo Tree Search.
    
    This class inherits from the Node class in mcts_node.py"""
    
    def __init__(self):
        pass
    
    
    def selection(self, node):
        while not node.state.terminal_test():
            if not len(node.childs_action) == len(node.state.actions()):
                return self.expand(node)
            node = self.best_child_node(node)
        return node


    def simulation(self, state):
        initials = copy.deepcopy(state)
        while not state.terminal_test():
            action = random.choice(state.actions())
            state = state.result(action)
        if state._has_liberties(initials.player()):
            reward=-1
        else:
            reward=1
        return reward


    def backpropagation(self, node, reward):
        while node != None:
            node.reward += reward
            node.visit += 1
            node = node.parent
            reward *= -1

            
    def expand(self, node):
        for action in node.state.actions():
            if action not in node.childs_action:
                not_tried_state = node.state.result(action)
                node.addchild(not_tried_state, action)
                node_chids=node.childs[-1]
                return node_chids


    def best_child_node(self, node):

        best_childs_list = []
        highest_score = float("-inf")
        for child in node.childs:
            score = child.reward / child.visit + 1 * (math.sqrt(2.0 * math.log(node.visit) / child.visit))
            if score > highest_score:
                best_childs_list=[child]
                highest_score=score 
            elif score == highest_score:
                best_childs_list.append(child)

        random_best_child = random.choice(best_childs_list)
        return random_best_child




class Node():
    def __init__(self, state, parent=None):
        self.state = state
        self.parent = parent
        self.visit = 1
        self.reward = 0
        self.childs = []
        self.childs_action = []


    def addchild(self, state, action):
        child = Node(state, self)
        self.childs.append(child)
        self.childs_action.append(action)
