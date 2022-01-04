
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
