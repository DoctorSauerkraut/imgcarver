#!/bin/python3

# Image carver and extractor from memory raw images

import sys
import binascii as bs
import os
import time

from progress import Progress

headers = { "jpg": ["ff", "d8", "ff", "e1"], 
            "jfif": ["ff", "d8", "ff", "e0"],
            "jfif2": ["ff", "d8", "ff", "fe"],  
            "png": ["89", "50", "4e", "47"],
            "gif": ["47", "49", "46", "38"],
            "bmp": ["42", "4d"]
        }

trailers = {"jpg":["FF","D9"],
            "jfif":["FF","D9"],
            "jfif2":["FF","D9"],
            "png": ["ae","42","60","82"],
            "gif": ["3b"]}


if __name__ == "__main__":
    matches = {}
    counters = {}
    for h in headers:
        matches[h] = []
        counters[h] = 0

    filename = sys.argv[1]

    print("Opening "+filename)
    
    bSize = os.stat(filename).st_size
    p = Progress("Carving data")
    p.progress(0, bSize)
    infile = open(filename, "rb")

    blockCtr = 0
    extracting = False
    extFormat = None
    ctrBmp = 0
    bmp = False
    sizeBmp = ""

    while infile:
        data = infile.read(1)
        blockCtr = blockCtr + 1
        c = bs.hexlify(data).decode('utf-8') 

        if(extracting):
            fout.write(data)

            if(bmp):
                ctrBmp = ctrBmp + 1

                # Getting the size field
                if(ctrBmp >= 1 and ctrBmp <= 4):
                    sizeBmp = c + sizeBmp

                # Computing the final size
                if(ctrBmp == 4):
                    sizeBmp = int(sizeBmp, 16)

            if(bmp or c == trailers[extFormat][counters[extFormat]]):
                counters[extFormat] = counters[extFormat]+1
            else:
                counters[extFormat] = 0

            if ((bmp and ctrBmp >= 4 and ctrBmp == sizeBmp) or 
                ((not bmp) and counters[extFormat] == len(trailers[extFormat]))):
                extracting = False
                counters[extFormat] = 0
                fout = None
                bmp = False
               
        else:
            for h in headers:
                if(c == headers[h][counters[h]]):
                    counters[h] = counters[h]+1
                else:
                    counters[h] = 0

                if (counters[h] == len(headers[h])):
                    if(h == "bmp"):
                        bmp = True
                    extracting = True
                    matches[h].append(blockCtr)
                    counters[h] = 0
                    extFormat = h
                    fout = open(str(blockCtr)+"."+str(h), "wb")
                    for b in headers[h]:
                        fout.write(bytearray.fromhex(b))

        p.progress(blockCtr, bSize)                        
        if(blockCtr == bSize):
            break

    p.progress(bSize, bSize)

    time.sleep(1)
    print("xxxx END xxxx")
    
    for m in matches:
        print(str(m)+":"+str(matches[m]))
