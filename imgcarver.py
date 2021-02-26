#!/bin/python3

import sys
import binascii as bs
import os
import time

from progress import Progress

tags = {"jpg": "ffd8ffe0", 
        "png": "89504e47",
        "gif": "47494638"}

def checkMatch(dataStr, tag, matchCtr):
    for c in dataStr:
        if(matchCtr == len(currentHead)-1):
            break

        if(c == currentHead[matchCtr]):
            matchCtr = matchCtr + 1 # Case 1 : One byte matches

        elif(c != currentHead[matchCtr]):
            matchCtr = 0  # Case 2 : One byte does not match

    return matchCtr


if __name__ == "__main__":
    matches =  {}
    for t in tags:
        matches[t] = []

    filename = sys.argv[1]

    print("Opening "+filename)
    
    bSize = os.stat(filename).st_size
    for t in tags:
        p = Progress("Finding "+str(t))
        p.progress(0, bSize)
        currentHead = tags[t]
        blockCtr = 0
        with open(filename, 'rb') as infile:
            while True:
                data = infile.read(16)
                blockCtr = blockCtr + 1
                if not data:
                    break  # end of file
                
                dataStr = bs.hexlify(data).decode('utf-8')
                matchCtr = 0
                #print(dataStr)
                p.progress(blockCtr*16,bSize)
                
                matchCtr = checkMatch(dataStr, currentHead, matchCtr)
                if(matchCtr == len(currentHead)-1):
                    matches[t].append(blockCtr)
                    matchCtr = 0
            p.progress(bSize, bSize)

    time.sleep(2)
    print("xxxx END xxxx")

    for m in matches:
        print(str(m)+":"+str(matches[m]))
