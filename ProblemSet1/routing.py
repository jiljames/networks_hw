# File: routing.py

"""
This module defines a routing table for the ARPANET routing assignment.
Your job in this assignment is to implement the RoutingTable class so
its methods implement the functionality described in the comments.
"""

class RoutingTable:

    """
    This class implements a routing table, which keeps track of
    two data values for each destination node discovered so far:
    (1) the hop count between this node and the destination, and
    (2) the name of the first node along the minimal path.
    """

    def __init__(self, name):
        """
        Creates a new routing table with a single entry indicating
        that this node can reach itself in zero hops.
        """
        # You complete this implementation
        self.name = name
        self.localtime = 0
        self.timerule = 7
        self.updatetimes = {}
        self.bad_destination = {}
        self.mydict = {name : (name, 0)} # Format is {name : (pathheader, numhops)} 

    def getNodeNames(self):
        """
        Returns an alphabetized list of the known destination nodes.
        """
        # You complete this implementation
        return sorted([node for node in self.mydict])

    def getHopCount(self, destination):
        """
        Returns the hop count from this node to the destination node.
        """
        # You complete this implementation
        if self.name == "HARV" and self.localtime > 20: # FOR PART 3
            return 0
        else:
            _, x = self.mydict[destination]
        return x

    def getBestLink(self, destination):
        """
        Returns the name of the first node on the path to destination.
        """
        # You complete this implementation
        x, _= self.mydict[destination]
        return x

    def update(self, source, table):
        """
        Updates this routing table based on the routing message just
        received from the node whose name is given by source.  The table
        parameter is the current RoutingTable object for the source.
        
        
        My implementation relies on a bad_destination table that this class
        keeps track of to allow for the propagation of news about bad nodes.
        First, we simply remove any bad neighbors from mydict. Then if source
        used to route to a destination but doesn't anymore, we list the 
        destination in our bad_destination table and wait a full timerule
        before we are willing to list it in mydict. After the timerule we
        remove it from bad destinations and will list it in mydict if we hear
        from a source with a path to that destination. 
        """


        # Update local times to show source just communicated.
        self.updatetimes[source] = self.localtime

        # If a node has served one timerule in bad_destination, remove it.
        for node in self.bad_destination.copy():
            if self.bad_destination[node] < self.localtime - self.timerule:
                del self.bad_destination[node] 
        #If a neighbor hasn't communicated in a while, add it to bad_neighbors:
        bad_neighbors = []
        for node in self.updatetimes:
            if self.updatetimes[node] < self.localtime - self.timerule:
                bad_neighbors.append(node)
        # If a node that used to be a path header no longer routes to dest node, add dest node to bad_destination.
        for node in self.getNodeNames():
            if self.getBestLink(node) == table.name and node not in table.mydict:
                self.bad_destination[node] = self.localtime
        # Delete all nodes with destinations or path headers in bad_neighbors or bad_destination.
        for node in self.getNodeNames():
            if node in bad_neighbors or self.getBestLink(node) in bad_neighbors:
                del self.mydict[node]
            elif node in self.bad_destination or self.getBestLink(node) in self.bad_destination:
                del self.mydict[node]
        
        # Update mytable according to table I recieve
        for node in table.getNodeNames():
            #Don't add any nodes in bad_destination.
            good_node = node not in self.bad_destination and table.getBestLink(node) not in self.bad_destination
            #Don't create a loop.
            no_loops = table.getBestLink(node) != self.name
            if good_node and no_loops:
                new_hops = table.getHopCount(node)
                if node in self.getNodeNames():
                    current_hops = self.getHopCount(node)
                    if new_hops + 1 < current_hops:
                        self.mydict[node] = (source, new_hops+1)
                else:
                        self.mydict[node] = (source, new_hops + 1)       
        self.localtime += 1
        
        