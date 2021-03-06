Hairpin structure finder implemented with LCS  
  
usage: lcs.py [-h] [-f FILEPATH] [-e MAXERR] [-l MINLEN] [-m MINMATCH]  
              [-s SAVE]  
  
optional arguments:  
    -h, --help   show this help message and exit  
    -f FILEPATH  path of the file, gets seq_short on default  
    -e MAXERR    maximum changes allowed in lcs  
    -l MINLEN    minimum length of lcs(50~100 recommended)  
    -m MINMATCH  minimum length of consequtive  
    -s SAVE      store result in filepath  
  
output example:  
\>./lcs -f input/seq.txt  
gene length: 100586  
LCS 1  : TAGATGATGATGTTATACGCGTTCTTCTGGCCGCTATTGGTGGAGGATGTAGTACTCCTCTTTTTTTAATAGTGACATAGGTCATCCTAGAGGCGGATTCGGACTCGAAGTTTGTGTTTGACGGGGGAATGTTGAGTGACCAGTCC  
hairpin: CCTGGAACATGAATCACAAATGGAGAGCTAACTAATCTATATCACTTTATCTTGCTAATGCAAAGGCCAAATGCATAAGTAGTTCAAACCCGGAAAATAATCTACTTTTGG  
LCS 2  : TAGATGATGATGTTATACGCGTTCTTCTGGCCGCTATTGGTGGAGGATGGGTATAGTACTCCTCTTTAATAGTGACATATTTTGGTCATCCTAGAGGCGGATTCGGACTCGAAGTTTGGACGGGGGAATGTTGAGTGACCTGTTTAGTCC  
change : TAGATGATGATGTTATACGCGTTCTTCTGGCCGCTATTGGTGGAGGAT~~GG~~GTA~~TA~~GTACTCCTC**TTTT**TTTAATAGTGACATA~~TTTT~~GGTCATCCTAGAGGCGGATTCGGACTCGAA**GTTTGT**GTTT~~G~~GACGGGGGAATGTTGAGTGACC~~TGTTT~~AGTCCC  
  
LCS 1  : GCGCGGCGGTGCACAAGCAATTGACAACTAACCACCGTGTATTCGTTATGGCATCAGGCAGTTTAAGTCGAGACAATAGGGCTCGCAATACACAGTTTACCGCATCTTGCCCTAACTGACAAACTGTGATCGACCACTAGCCATGCCATTGCCTCTTAGACACCCGTG  
hairpin: TCGATACTGAACGAATCGATGCACACTCCCTTCCTTGAAAACGCACAATCATACAAGTGGGCACATGATGG  
LCS 2  : GCGCGGCGGTGCACAAGCAATTGACAACTAACCACCGTGTATTCGTTATGGCATCAGTTTAAGTCGAGACAATAGGGCTCTACACAGTTTGCAAACCGCATCTTGCCCTAACTGACAAACTGTGATCGACCACTAGCCATGCCATTGCCTCTTAGACACCCTG  
change : GCGCGGCGGTGCACAAGCAATTGACAACTAACCACCGTGTATTCGTTATGGCAT**CAGG**CAGTTTAAGTCGAGACAATAGGGCT**CGCA**~~C~~**A**TACACAGTTT~~GCAA~~ACCGCATCTTGCCCTAACTGACAAACTGTGATCGACCACTAGCCATGCCATTGCCTCTTAGACACCC**G**TGT  
  
LCS 1  : ACCCGGAAATGGCTGTATTTATTGAGGTATTATACTGTGATATGTTAAAAAAAAAAGGGGAGTAGGTGGATGATTTTCAAGAAGCTATGCCTAAGCGCGTGAGTACCATCGGCCAGACGCAGTCTTGGCCCAGTACCGACGAATCTACTGCAATCGCATGACAGGGCTAC  
hairpin: CATTAGAAACTACATATGAGGAGAATACCAGACGTTATTTTTTTGAACGACCACATACATAGCATACACATAATAAATTTAAAA  
LCS 2  : ACCCGGAAATGGCTGTATTTATTGAGGTATTATACAGTTGTGATATGTTAAAAAAAAAAGGGGAGTAGGTGGATGATTTTCAAGAAGCTATGCCTAAGCGCGTGAGTACCATCGGCCAGACGCAGTCTTGGCCCAGTACCGACGAATCTACTGCCCCAATCGCATGACAGGGCTAC  
change : ACCCGGAAATGGCTGTATTTATTGAGGTATTATAC~~AGT~~TGTGATATGTTAAAAAAAAAAGGGGAGTAGGTGGATGATTTTCAAGAAGCTATGCCTAAGCGCGTGAGTACCATCGGCCAGACGCAGTCTTGGCCCAGTACCGACGAATCTACTG~~CCC~~CAATCGCATGACAGGGCTACC  
  
time spent:122.67      
