from sample_players import DataPlayer
from collections import defaultdict
from isolation import isolation
import random, math, copy



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


