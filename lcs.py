#!/usr/bin/env python
from docx import Document
import argparse, os

parser = argparse.ArgumentParser(description="usage: [-t] [-f] <filepath> ")
parser.add_argument("-t", dest="txtInput", default=False, action="store_true")
parser.add_argument("-f", dest="filePath", type=str)

args = parser.parse_args()
MIN_SIMILARITY = 0.9
if args.filePath is not None:
    FILE_DEST = args.filePath 
else:
    FILE_DEST = "./input/seq_short.txt" if args.txtInput else "./input/seq_short.docx"

def main():
    inputType = FILE_DEST[FILE_DEST.rfind('.'):]
    print(FILE_DEST) 
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


#MUST be done in linear time
def findHairpin(gene):
    genelen = len(gene)
    print(genelen)



#getstring similarity based on levenshtein distance
#its similar to lcs algorithm
def strsim(str1, str2):
    similarity = levdist(str1, str2) * 1.0 / max(len(str1), len(str2))
    return True if similarity > MIN_SIMILARITY else False

def levdist(str1, str2):
    len1 = len(str1)
    len2 = len(str2)
    dist = [[0 for x in range(len2)] for y in range(len1)]
#    for i in range(len1):
#        for j in range(len2):
            #TODO


if __name__ == "__main__":
    main()


