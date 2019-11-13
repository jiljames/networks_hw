# File: TCPSimulator.py

"""
This module implements the starter version of the TCP simulator assignment.
"""

# Implementation notes for Problem Set 5
# --------------------------------------
# For Problem 1, you will need to add more state information to both the
# TCPClient and TCPServer classes to keep track of which bytes have been
# acknowledged.  You will also need to implement a new TCPEvent subclass
# called TimeoutEvent that implements the response to a packet timeout.
# Sending a packet should also post a TimeoutEvent for a later time.
# If the packet has been acknowledged, the TimeoutEvent handler can simply
# ignore it.  If not, the TimeoutEvent handler should resend the packet.
#
# Problem 2 requires relatively little code beyond Problem 1, assuming
# that you have coded Problem 1 correctly (bugs in Problem 1 are likely
# to manifest themselves here when there are multiple pipelined messages).
# The priority queue strategy means that you don't need to use any
# Python primitives for parallelism such as timeouts and threads.
#
# Problem 3 means that you need to have the client keep track of the
# number of unacknowledged packets and to pay attention to the receive
# window in the acknowledgments that come in from the server.

from packet import TCPPacket
from pqueue import PriorityQueue
from checksum import checksum16
import random

# Constants
MAX_PACKET_DATA = 4
TRANSMISSION_DELAY = 5
ROUND_TRIP_TIME = 2 * TRANSMISSION_DELAY
TIMEOUT = 2 * ROUND_TRIP_TIME
RECIEVE_WINDOW = 5
LOST_PACKET_PROBABILITY = 0.25

EVENT_TRACE = False           # Set this flag to enable event tracing



def TCPSimulator():
    """
    This function implements the test program for the assignment.
    It begins by creating the client and server objects and then
    executes an event loop driven by a priority queue for which
    the priority value is time.
    """
    eventQueue = PriorityQueue()
    client = TCPClient()
    server = TCPServer()
    client.server = server
    server.client = client
    client.queueRequestMessage(eventQueue, 0)
    while not eventQueue.isEmpty():
        e,t = eventQueue.dequeueWithPriority()
        if EVENT_TRACE:
            print(str(e) + " at time " + str(t))
        e.dispatch(eventQueue, t)


class TCPClient:
    """
    This class implements the client side of the simulation, which breaks
    up messages into small packets and then sends them to the server.
    """

    def __init__(self):
        """Initializes the client structure."""
        self.name = "Client"

    def requestMessage(self, eventQueue, t):
        """Initiates transmission of a message requested from the user."""
        msg = input("Enter a message: ")
        if (len(msg) != 0):
            print("Client sends \"" + msg + "\"")
            self.msgBytes = msg.encode("UTF-8")
            self.seq = 0
            self.ack = 0
            self.serverRecieveWindow = 1    # Don't know window so initially set to 1
            self.waitingForAck = {}         # Store which packets haven't been ACK'd
            self.sendNextPacket(eventQueue, t)

    def sendNextPacket(self, eventQueue, t):
        """Sends the next packet in the message."""
        nBytes = min(MAX_PACKET_DATA, len(self.msgBytes) - self.seq)
        data = self.msgBytes[self.seq:self.seq + nBytes]
        p = TCPPacket(seq=self.seq, ack=self.ack, ACK=True, data=data)
        if self.seq + nBytes == len(self.msgBytes):
            p.FIN = True
        e = ReceivePacketEvent(self.server, p)
        #With some probability, lose the packet
        if random.random() > LOST_PACKET_PROBABILITY:
            eventQueue.enqueue(e, t + TRANSMISSION_DELAY)
        #Queue the timeout event
        timeout = TimeoutEvent(self, p)
        self.waitingForAck[checksum16(p.toBytes())] = p
        eventQueue.enqueue(timeout, t + 4 * TRANSMISSION_DELAY)
        self.seq += nBytes
        self.ack = self.seq + 1
        #If we aren't finished and serverRecieveWindow allows it, send next bytes
        if not p.FIN and len(self.waitingForAck) < self.serverRecieveWindow:
            self.sendNextPacket(eventQueue, t)

    def receivePacket(self, p, eventQueue, t):
        """Handles receipt of the acknowledgment packet."""
        self.serverRecieveWindow = p.window
        if ~p.checksum in self.waitingForAck:
            del self.waitingForAck[~p.checksum]
        if p.FIN:
            self.queueRequestMessage(eventQueue, t + TIMEOUT)
        # Recieving packets starts a call to sendNextPacket
        # only if message unfinished and not waiting for ACKs
        if not p.FIN and len(self.waitingForAck) == 0:
            self.sendNextPacket(eventQueue, t)

    def queueRequestMessage(self, eventQueue, t):
        """Enqueues a RequestMessageEvent at time t."""
        e = RequestMessageEvent(self)
        eventQueue.enqueue(e, t)
    
    def timeout(self, p, eventQueue, t):
        e = ReceivePacketEvent(self.server, p)
        eventQueue.enqueue(e, t + TRANSMISSION_DELAY)
        timeout = TimeoutEvent(self, p)
        self.waitingForAck[checksum16(p.toBytes())] = p
        eventQueue.enqueue(timeout, t + 4 * TRANSMISSION_DELAY)

class TCPServer:
    """
    This class implements the server side of the simulation, which
    receives packets from the client side.
    """

    def __init__(self):
        self.name = "Server"
        self.resetForNextMessage()

    def receivePacket(self, p, eventQueue, t):
        """
        Handles packets sent from the server and sends an acknowledgment
        back in return.  This version assumes that the sequence numbers
        appear in the correct order.
        """
        def checkAllReceived():
            # Sorts self.recieved
            self.received.sort()
            correctAck = MAX_PACKET_DATA
            # Check if packets are missing
            for ack, _ in self.received:
                if ack > correctAck:
                    return False
                correctAck += MAX_PACKET_DATA
            return True

        self.seq = p.ack
        self.ack = p.seq + len(p.data)
        self.received.append((self.ack, p.data))
        if p.FIN:
            self.receivedFIN = True
        
        reply = TCPPacket(seq=self.seq, ack=self.ack, ACK=True,
                            checksum = ~checksum16(p.toBytes()), window = RECIEVE_WINDOW)

        #If all packets are present, message complete.
        if self.receivedFIN and checkAllReceived():
            self.received.sort()
            for _, data in self.received:
                self.msgBytes.extend(data)
            reply.FIN = True
            print("Server receives \"" + self.msgBytes.decode("UTF-8") + "\"")
            self.resetForNextMessage()
        e = ReceivePacketEvent(self.client, reply)
        eventQueue.enqueue(e, t + TRANSMISSION_DELAY)

    def resetForNextMessage(self):
        """Initializes the data structures for holding the message."""
        self.msgBytes = bytearray()
        self.ack = 0
        self.received = []
        self.receivedFIN = False



class TCPEvent:
    """
    This abstract class is the base class of all events that can be
    entered into the event queue in the simulation.  Every TCPEvent subclass
    must define a dispatch method that implements that event.
    """

    def __init__(self):
        """Each subclass should call this __init__ method."""

    def dispatch(self, eventQueue, t):
        raise Error("dispatch must be implemented in the subclasses")


class RequestMessageEvent(TCPEvent):
    """
    This TCPEvent subclass triggers a message transfer by asking
    the user for a line of text and then sending that text as a
    TCP message to the server.
    """

    def __init__(self, client):
        """Creates a RequestMessageEvent for the client process."""
        TCPEvent.__init__(self)
        self.client = client

    def __str__(self):
        return "RequestMessage(client)"

    def dispatch(self, eventQueue, t):
        self.client.requestMessage(eventQueue, t)


class ReceivePacketEvent(TCPEvent):
    """
    This TCPEvent subclass is called on each packet.
    """

    def __init__(self, handler, packet):
        """
        Creates a new ReceivePacket event.  The handler parameter is
        either the client or the server.  The packet parameter is the
        TCPPacket object.
        """
        TCPEvent.__init__(self)
        self.handler = handler
        self.packet = packet

    def __str__(self):
        return self.handler.name+ " ReceivePacket(" + str(self.packet) + ")"

    def dispatch(self, eventQueue, t):
        self.handler.receivePacket(self.packet, eventQueue, t)


class TimeoutEvent(TCPEvent):
    """
    This TCPEvent implements the response to a packet timeout.
    """

    def __init__(self, handler, packet):
        TCPEvent.__init__(self)
        self.handler = handler
        self.packet = packet

    def __str__(self):
        return "Timeout("+str(self.packet) + ")"
    
    def dispatch(self, eventQueue, t):
        #If a packet never got an ACK back -- handle timeout and resend.
        if checksum16(self.packet.toBytes()) in self.handler.waitingForAck:
            self.handler.timeout(self.packet, eventQueue, t)




# Startup code

if __name__ == "__main__":
    TCPSimulator()
