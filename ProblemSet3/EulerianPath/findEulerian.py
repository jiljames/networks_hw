# Jillian James
# Short program to find a Eulerian path in a graph.
from graph import Graph, Arc, Node


#################################################################
#   I add some new functionality to the Arc class. Added methods
#   to keep track of a single Arc in the opposite direction 
#   to help with removing the correct arc in the presense of
#    multiple bridges between two nodes. 
#################################################################

Arc._opposite = None

def setOpposite(self, arc):
    self._opposite = arc

def getOpposite(self):
    return self._opposite

setattr(Arc, "setOpposite", setOpposite)
setattr(Arc, "getOpposite", getOpposite)



#################################################################
#   Methods that use graph.py to parse a graph file and if one 
#   exists, returns a path that crosses all arcs exactly once.
#################################################################


def findPathStart(g):
    ''' 
    2 odd degree nodes means we have a path. In this case, start is one 
    of the odd nodes. All even degree nodes means we have a path. In this
    case start is any node. Otherwise graph has no Eulerian path.
    '''
    odd = []
    for node in g.getNodes():
        if (len(node.getArcsFrom())+len(node.getArcsTo()))//2 %2 != 0:
            odd.append(node)
    if len(odd) == 2: 
        return odd[0]
    elif len(odd) == 0: 
        return node
    else:
        return None



def findPath(g, node, s, path):
    '''
    Modified BFS that removes arcs as it visits nodes
    If a node has no arcs from it, add it to the path.
    If there are no arcs from a node and no nodes in 
    the stack, return.
    '''
    if len(node.getArcsFrom()) > 0:
        arc = node.getArcsFrom()[0]
        s.append(node)
        node = arc.getFinish()
        g.removeArc(arc)
        g.removeArc(arc.getOpposite())
        return findPath(g, node, s, path)

    path.append(node)
    if len(s) > 0:
        node = s.pop(-1)
        return findPath(g, node, s, path)
    else:
        return path



def writeAsArcs(path):
    arcs = []
    first = path[0]
    for i in range(1, len(path)):
        arcs.append(str(first) + "-" + str(path[i]))
        first = path[i]
    return "A Eulerian Path: " + ", ".join(arcs)



def EulerianPath():
    """
    Reads in a graph file. Calls findPathStart. For each arc, find
    an equivalent arc in the opposite direction to assign as opposite.
    Calls findPath and returns path.
    """
    while True:
        g = Graph()
        filename = input("Enter name of graph file: ")
        if filename == "":
            return
        if filename.find(".") == -1:
            filename += ".txt"
        g.clear()
        g.load(filename)

        for arc1 in g.getArcs():
            for arc2 in g.getArcs():
                checkforward = arc1.getStart() == arc2.getFinish()
                checkbackward = arc1.getFinish() == arc2.getStart()
                if checkforward and checkbackward:
                    if arc1.getOpposite() == None and arc2.getOpposite() == None:
                        arc1.setOpposite(arc2)
                        arc2.setOpposite(arc1)

        start = findPathStart(g)
        if start == None:
            print("There is no valid Eulerian Path.")
            print()
        else:
            path = findPath(g, start, [], [])
            path.reverse()
            print(writeAsArcs(path))
            print()



if __name__ == "__main__":
    EulerianPath()
