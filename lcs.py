#!/usr/bin/env python
from docx import Document
import argparse, os

parser = argparse.ArgumentParser(description="usage: [-t] [-f] <filepath> ")
parser.add_argument("-t", dest="txtInput", default=False, action="store_true")
parser.add_argument("-f", dest="filePath", default="./src/seq_short.docx", type=str)

args = parser.parse_args()

def main():
    inputType = args.filePath[args.filePath.rfind('.'):]
    
    if args.txtInput:
        if inputType != ".txt":
            print("input file must be txt")
            os._exit(0)
        with open(args.filePath) as text:
            gene = text.readlines()[-1]
    else:
        if inputType != ".docx":
            print("input file must be docx")
            os._exit(0)
        gene = Document(args.filePath).paragraphs[-1].text

    #TODO do something with gene
    print(gene)





if __name__ == "__main__":
    main()


