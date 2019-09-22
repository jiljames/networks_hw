        Jillian James CSCI 396


        Change in arpanet.py:

        I didn't want to change the API, but I found an issue that 
        I think is a bug and it caused my implementation to break.
        In arpanet.py, the update method does not clear the table's
        lables before changing them. Then in the case where you go
        from having 10 entries in the table to 9, a 10th entry is still
        displayed on the last line (from when the table doesn't erase).
        So in arpanet.py I added two lines of code (147 and 148) to clear
        the tables.



        Implementation of network update method:

        My implementation relies on a bad_destination table that this class
        keeps track of to allow for the propagation of news about bad nodes.
        First, we simply remove any bad neighbors from mydict. Then if source
        used to route to a destination but doesn't anymore, we list the 
        destination in our bad_destination table and wait a full timerule
        before we are willing to list it in mydict. After the timerule we
        remove it from bad destinations and will list it in mydict if we hear
        from a source with a path to that destination.
