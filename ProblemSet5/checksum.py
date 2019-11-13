

def checksum16(b):
    '''
    Computes the checksum for a packet
    '''
    def add(x, y):
        result = x + y
        # If binary rep is too long, then carry.
        if  len(bin(result)[2:]) > 16:
            return add(int(bin(result)[-16:], 2), int(bin(result)[:-16], 2))
        return result

    cs, i = 0, 1
    for i in range(1, len(b), 2):
        data = (b[i-1] << 8) | b[i]
        cs = add(cs, data)
    return cs