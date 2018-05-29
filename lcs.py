#!/usr/bin/env python
from docx import Document
import argparse, os, time, sys

# size of the checking window
WIN_SIZE = 250

# used to checks similarity in two lcs(not currently used)
MIN_SIMILARITY = 0.9

# maximum length of addition or deletion
MAX_ERR_LENTH = 15

# how many character must continuously match to make it valid lcs
MIN_MATCH_LENGTH = 3

# minimum length of lcs string
# if found string is longer than this value, declare it as
# hairpin string and print it
MIN_LCS_LENTH = 50

# if valid lcs isn't found, skip iteration to speed up process
SKIP_DIST = 30

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
    i = 0
    maxlen = 0
    bestStr = ("", "")
    while i < genelen-WIN_SIZE*2:
        out = lcs(gene[i:i+WIN_SIZE], gene[i+WIN_SIZE:i+WIN_SIZE*2])
        percent = str(i * 100 / genelen) + "%"
        sys.stdout.write("calculating:" + percent + "               \r")
        sys.stdout.flush()
        if out is not None:
            if maxlen < max(out[1]-out[0], out[3]-out[2]):
                maxlen = max(out[1]-out[0], out[3]-out[2])
                bestStr = (gene[i+out[0]:i+out[1]], gene[i+WIN_SIZE+out[2]:i+WIN_SIZE+out[3]])
                i = i + 1
            else:
                print("LCS 1: " + bestStr[0])
                print("LCS 2: " + bestStr[1])
                i = i + WIN_SIZE
                maxlen = 0
                bestStr = ("","")
        else:
            i = i + SKIP_DIST
        
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

# variable for expression where max dist[][]['length'] come from:
START = 0
FROM_I = 1
FROM_J = 2
FROM_MATCH = 3
DEFAULT_DIST = {'length' : 0, 'from' : START, 'cont' : 0}
def lcs(str1, str2):
    retdic = {
        'length' : 0,
        'found' : False 
        }
    len1 = len(str1)
    len2 = len(str2)
    maxLength = 0
    bestIndex = (0,0)
    # dist contains a dictionary which consists of length and where lcs come from,
    # and how many character is continously matching
    # if string is not matching, cont variable will turn negative, and too many mismatch will
    # make the lcs start over from 0
    dist = [[DEFAULT_DIST for x in range(len2)] for y in range(len1)]
    for i in range(len1):
        for j in range(len2): 
            if j is 0:
                dist[i][j] = {'length' : max(0, dist[i-1][j]['length']), 'from' : START, 'cont' : 0}
            else: 
                # if dist[][] gets value from insertion or deletion, decrement its value by 1
                # if str1[i] and str2[j] matches, restore decremented value
                length1 = decrement(dist[i-1][j], FROM_I)
                length2 = decrement(dist[i][j-1], FROM_J)
                if str1[i] is str2[j]:
                    matchLength = {'length' : dist[i-1][j-1]['length'] + 1
                            , 'from' : FROM_MATCH
                            , 'cont' : max(0, dist[i-1][j-1]['cont']) + 1
                            }
                else:
                    # in this case, both of the checking string is from 1 index behind,
                    # so decrement two times since its two times the difference 
                    # from single insertion or deletion
                    matchLength = DEFAULT_DIST

                dist[i][j] = getBestLCS(length1, length2, matchLength)
                # because dist[][] looses its value if there's too much insertion 
                # in a row, I need to store the index to best index 
                if dist[i][j]['length'] > maxLength:
                    maxLength = dist[i][j]['length']
                    bestIndex = (i, j)

    if maxLength > MIN_LCS_LENTH:
        return LCSindex(str1, str2, dist, bestIndex)
    else:
        return None

def LCSindex(str1, str2, dist, bestIndex):
    i = bestIndex[0]
    j = bestIndex[1]
    while True:
        lcsFrom = dist[i][j]['from']
        if lcsFrom == FROM_I:
            i = i - 1
        elif lcsFrom == FROM_J:
            j = j - 1
        elif lcsFrom == FROM_MATCH:
            i = i - 1
            j = j - 1

        if dist[i][j]['from'] is START:
            break

    return(i, bestIndex[0] + 1, j, bestIndex[1] + 1)


# finds the best LCS, using cont value as tiebreaker
def getBestLCS(dict1, dict2, dict3):
    l1 = dict1['length'] * 100 + dict1['cont']
    l2 = dict2['length'] * 100 + dict2['cont']
    l3 = dict3['length'] * 100 + dict3['cont']
    maxLength = max(l1, l2, l3)
    if l1 is maxLength:
        return dict1
    elif l2 is maxLength:
        return dict2
    else:
        return dict3


def decrement(dist, src):
    retlen = dist['length']
    retcont = dist['cont']
    retsrc = START
    
    # cont value, which is number of continous character that match,
    # must be over MIN_MATCH_LENGTH to be valid lcs    
    if retcont > 0 and retcont < MIN_MATCH_LENGTH:
        return DEFAULT_DIST

    # cont will be negative if character is mismatching several times in a row,
    # and if it will be used to discard lcs that has to many insertions or deletion
    if retcont <= -MAX_ERR_LENTH:
        return DEFAULT_DIST

    retlen = retlen - 1
    retsrc = src
    retcont = min(retcont, 0) - 1
    
    return {'length' : retlen, 'from' : retsrc, 'cont' : retcont}


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


