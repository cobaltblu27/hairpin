#!/usr/bin/env python
from docx import Document
import argparse, os, time, sys

WIN_SIZE = 250
MIN_SIMILARITY = 0.9

parser = argparse.ArgumentParser(description="usage: [-t] [-f] <filepath> ")
parser.add_argument("-t", dest="txtInput", default=False, action="store_true")
parser.add_argument("-f", dest="filePath", type=str)

args = parser.parse_args()

if args.filePath is not None:
    FILE_DEST = args.filePath 
else:
    FILE_DEST = "./input/seq_short.txt" if args.txtInput else "./input/seq_short.docx"

def main():
    inputType = FILE_DEST[FILE_DEST.rfind('.'):]
    try:
        if args.txtInput:
            if inputType != ".txt":
                print("input file must be txt")
                os._exit(0)
            with open(FILE_DEST) as text:
                gene = text.readlines()[-1]
        else:
            if inputType != ".docx":
                print("input file must be docx")
                os._exit(0)
            gene = Document(FILE_DEST).paragraphs[-1].text
    except: 
        print("no such file!")
        os._exit(0)
    findHairpin(gene)


# MUST be done in linear time
def findHairpin(gene):
    genelen = len(gene)
    print("gene length: "+str(genelen))
    start = time.time()
    maxout = None
    for i in range(genelen-WIN_SIZE*2):
        out = lcs(gene[i:i+WIN_SIZE], gene[i+WIN_SIZE:i+WIN_SIZE*2])
        percent = str(i * 100 / genelen) + "%"
        sys.stdout.write("calculating:" + percent + "               \r")
        sys.stdout.flush
        if maxout is None or maxout['length'] < out['length']:
            maxout = out
            
        
    end = time.time()
    print("time spent:" + str(round(end-start, 2)))
    print(maxout)

# getstring similarity based on levenshtein distance
# similar to lcs algorithm
def strsim(str1, str2):
    similarity = levdist(str1, str2) * 1.0 / max(len(str1), len(str2))
    return 1 - similarity


def lcs(str1, str2):
    retdic = {
        'length' : 0,
        'lcs1_start' : 0,
        'lcs1_end' : 0,
        'lcs2_start' : 0,
        'lcs2_end' : 0
        }
    len1 = len(str1)
    len2 = len(str2)
    dist = [[0 for x in range(len2)] for y in range(len1)]
    for i in range(len1):
        for j in range(len2): 
            # TODO: mark best lcs and apply more DP for sliding window
            if j is 0:
                dist[i][j] = max(0, dist[i-1][j])
            else:
                charmatch = 1 if str1[i] == str2[j] else 0
                dist[i][j] = max(dist[i-1][j], dist[i][j-1], dist[i-1][j-1] + charmatch)
    retdic['length']=dist[len1-1][len2-1]
    return retdic


def levdist(str1, str2):
    len1 = len(str1)
    len2 = len(str2)
    dist = [[0 for x in range(len2)] for y in range(len1)]
    for i in range(len1):
        for j in range(len2):
            if min(i, j) is 0:
                dist[i][j] = max(i,j)
            else:
                charmismatch = 0 if str1[i] is str2[j] else 1
                dist[i][j] = min(dist[i-1][j] + 1, dist[i][j-1] + 1, dist[i-1][j-1] + charmismatch)
    return dist[len1-1][len2-1]


if __name__ == "__main__":
    main()


