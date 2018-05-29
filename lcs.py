#!/usr/bin/env python
from docx import Document
import argparse, os, time, sys

# size of the checking window
WIN_SIZE = 250

# used to checks similarity in two lcs(not currently used)
MIN_SIMILARITY = 0.9

# maximum length of addition or deletion
MAX_ERR_LENTH = 4

# minimum length of lcs string
# if found string is longer than this value, declare it as
# hairpin string and print it
MIN_LCS_LENTH = 50

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


def findHairpin(gene):
    genelen = len(gene)
    print("gene length: "+str(genelen))
    start = time.time()
    maxout = None
    for i in range(genelen-WIN_SIZE*2):
        out = lcs(gene[i:i+WIN_SIZE], gene[i+WIN_SIZE:i+WIN_SIZE*2])
        percent = str(i * 100 / genelen) + "%"
        sys.stdout.write("calculating:" + percent + "               \r")
        sys.stdout.flush()
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


# to allow insertion and deletion while removing string with too big gaps, 
# decrement dist[][] a little bit when common string is not continuing
def lcs(str1, str2):
    retdic = {
        'length' : 0,
        'found' : False 
        }
    len1 = len(str1)
    len2 = len(str2)
    index = [[0 for x in range(len2)] for y in range(len1)]
    dist = [[0 for x in range(len2)] for y in range(len1)]
    for i in range(len1):
        for j in range(len2): 
            # TODO: mark best lcs and apply more DP for sliding window
            if j is 0:
                dist[i][j] = max(0, dist[i-1][j])
            else: 
                # if dist[][] gets value from insertion or deletion, decrement its value by 1
                # if str1[i] and str2[j] matches, restore decremented value
                length1 = verify(dist[i-1][j] - 1)
                length2 = veryfy(dist[i][j-1] - 1)
                if str1[i] is str2[j]:
                    matchLength = (dist[i-1][j-1] + MIN_LCS_LENTH) 
                    # round up matchLength to multiple of 100
                    matchLength = matchLength + (MIN_LCS_LENTH - matchLength % MIN_LCS_LENTH) % MIN_LCS_LENTH
                else:
                    # in this case, both of the checking string is from 1 index behind,
                    # so decrement two times since its two times the difference 
                    # from single insertion or deletion
                    matchLength = verify(dist[i-1][j-1] - 1)
                    matchLength = verify(matchLength - 1)

                dist[i][j] = max(length1, length2, matchLength)
    retdic['length']=dist[len1-1][len2-1] / MIN_LCS_LENTH
    if retdic['length'] > MIN_LCS_LENTH:
        retdic['found'] = True
    return retdic


def verify(length):



def levdist(str1, str2):
    len1 = len(str1)
    len2 = len(str2)
    dist = [[0 for x in range(len2)] for y in range(len1)]
    for i in range(len1)
        for j in range(len2):
            if min(i, j) is 0:
                dist[i][j] = max(i,j)
            else:
                charmismatch = 0 if str1[i] is str2[j] else 1
                dist[i][j] = min(dist[i-1][j] + 1, dist[i][j-1] + 1, dist[i-1][j-1] + charmismatch)
    return dist[len1-1][len2-1]


if __name__ == "__main__":
    main()


