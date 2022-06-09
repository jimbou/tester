#!/usr/bin/python

import json
import sys
import re
import pandas as pd


regs =['%eax' , "%ebx" ,"%ecx", "%edx", "%cs", "%ds", "%es", "%fs", "%gs", "%ss","%esi", "%edi" , "%ebp", "%eip" ,"%esp", "%ax", "%bx", "%cx" , "%dx" ,"%ah" ,"%al" ,"%bh" ,"%bl" , "%ch" ,"%dh" ,"%dl" ,"%rax", "%rcx" ,"%rdx" ,"%rbx" ,"%rsp" ,"%rbp" ,"%rsi" ,"%rdi" ,"%sp" ,"%bp" ,"%si" ,"%di" ,"%spl" ,"%bpl" ,"%sil" ,"%dil" , "%ss" ,"%cs" ,"%ds" ,"%es" ,"%fs" ,"%gs" ,"%eflags" ,"%eip"  ]

df = pd.read_csv('opcodes.csv')
df =df.drop(df.columns[5], axis=1)
df.dropna(subset=['name'], inplace=True)
df =df.reset_index(drop=True)

with open(str(sys.argv[1])) as f:
    my_dict = json.load(f)
opcodes =[]
tmp =0
weights = {}
for key, value in my_dict.items():
    weights[key] =0
    for item in value :
        
        #x = re.split('/\s{1,}|,|\t{1,}/g', item)
        x = re.split(r"\s+|,", item)
        opcodes.clear()
        tmp =min(4,len(x))
        for i in range(tmp):
            opcodes.append(x[i])
        if (tmp == 4):
            arg1 = opcodes[1]
            arg2 = opcodes[2]
            arg3 = opcodes[3]
        elif (tmp == 3):
            arg1 = opcodes[1]
            arg2 = opcodes[2]
            arg3 = ""
        elif (tmp == 2):
            arg1 = opcodes[1]
            arg2 = ""
            arg3 = ""
        else:
            arg1 = ""
            arg2 = ""
            arg3 = ""


        print (opcodes,"\n")
        print (x[0]," ", arg1," ",arg2," ",arg3," ","\n")

        if arg1 in regs:
            arg1 ="r"
        elif ('(' in arg1 ) and (')' in arg1 ):
            arg1 ="m"
        elif arg1.startswith('%'):
            arg1 ="m"
        elif arg1.startswith("$0x"):
            arg1 ="I"
        elif arg1 == "%cl":
            arg1 ="cl"
        else :
            arg1 =""

        if arg2 in regs:
            arg2 ="r"
        elif ('(' in arg2 ) and (')' in arg2 ):
            arg2 ="m"
        elif arg2.startswith('%'):
            arg2 ="m"
        elif arg2.startswith("$0x"):
            arg2 ="I"
        elif arg2 == "%cl":
            arg2 ="cl"
        else :
            arg2 =""
        
        if arg3 in regs:
            arg3 ="r"
        elif ('(' in arg3 ) and (')' in arg3 ):
            arg3 ="m"
        elif arg3.startswith('%'):
            arg3 ="m"
        elif arg3.startswith("$0x"):
            arg3 ="I"
        elif arg3 == "%cl":
            arg3 ="cl"
        else :
            arg3 =""

        print (opcodes,"\n")
        print (x[0]," ", arg1," ",arg2," ",arg3," ","\n")

        


        #print(opcodes ,"\n")  



#print(df.to_string()) 

