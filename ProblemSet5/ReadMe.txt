Homework 5 - Jillian James

Files I have changed/added for this homework:
    checksum.py - checksum16 implementation for Problem 1.
    TCPSimulator.py - TCPSimulator.py icludes my changes to the simulator in all parts
    of problem 2. 

Notes:

    For problem 2 parts a and b:
        My implementation for Problem 2 has the client keep a dictionary which tracks which packets
        have not yet been acknowledged. The keys are the checksums of the packets. When a packet is 
        acknowledged I delete that (key,value) pair.

        I also have the server keep track of an array of tuples which reinitializes with every new
        message. The values in the tuple are the current ACK and the packet data. When the server
        has recieved a packet with p.FIN = True, for each packet it recieves after that, it sorts this
        array of tuples by the first value (the ACKs) and checks to see if any packets are missing. 
        If not, the message is complete.


    For problem 2 part c:
        In the TCPSimulator.py file I created the RECIEVE_WINDOW constant so that this can easily be
        changed by the user. This constant is only used by the server to initialize the recieve window 
        value--it is not used by the client. The client instead figures out the recieve window by sending
        a single packet to the server and updating serverRecieveWindow data member of client. From then on
        it sends the number of packets that the recieve window dictates.