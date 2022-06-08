#!/usr/bin/python

import json
import sys
import re
import pandas as pd

with open(str(sys.argv[1])) as f:
    my_dict = json.load(f)
opcodes =[]
for key, value in my_dict.items():
    for item in value :
        
        #x = re.split('/\s{1,}|,|\t{1,}/g', item)
        x = re.split(r"\s+|,", item)
        opcodes.clear()
        for i in range(min(4,len(x))):
            opcodes.append(x[i])
        print(opcodes ,"\n")  


df = pd.read_csv('opcodes.csv')
df =df.drop(df.columns[5], axis=1)
df.dropna(subset=['name'], inplace=True)
df =df.reset_index(drop=True)
#print(df.to_string()) 

