#!/usr/bin/python

import sys
import re
import json
import pandas as pd
names = []

energy=[]

energy_value=[]
energy_elements =[]
energy_elements_tmp=[]
energies_unchanged= []
total_energy_unchanged =0 


with open(str(sys.argv[6])) as file1:   #file 5 has 2 energy values from a unchanged run of the test code 
    for line in file1:
      x =line.rstrip()
      if (x.startswith("Energy: ")):
            x =x.replace("Energy: ","")
            energies_unchanged.append( float(x))   


total_energy_unchanged = energies_unchanged[-1] -energies_unchanged[0]


with open(str(sys.argv[1])) as file:
    for line in file:
        x =line.rstrip()
        if (x.startswith("Basic Block : final")):
            pass
        elif (x.startswith("Basic Block : ")):
            x =x.replace("Basic Block : ","")
            names.append(x)
        elif(x.startswith("Energy: ")):
            x =x.replace("Energy: ","")
            energy.append(float(x)) # for every basic block we store its energy read at list energy
if energy[-1]!= energy[-2]:
    energy[-2] =energy[-1]
    energy.pop()
beg =energy[0]    
start_index =0
counter_ind =0
for item in energy:
    if item != beg :
        final = item 
        energy_spent = final - beg
        energy_value.append(energy_spent) # energy value is a list of all the differnt energy values in the order they were sampled
        
        energy_elements.append( names[start_index:(start_index+counter_ind)]) #energy elements is a  list that contains list of basic blocks who have the same energy value. 
        print("Added ", energy_elements_tmp , "in list \n")
        energy_elements_tmp.clear()
        start_index =start_index+counter_ind
        beg =final
        counter_ind=0
    counter_ind +=1

total_reads=0

for item in energy_elements:
    print (item, "\n")
    total_reads += len(item)
    print(total_reads, "\n")
energy_total =energy[-1]- energy[0] # energy total is the energy spent by the total  modified program 
print("Total  energy cost is : ", energy_total , "\n")
energy_total_rapl = energy_total - total_energy_unchanged  # energy total rapl  is the energy spent by the rapl reads (energy of modifies program - energy of unmodified program) 
print("Total clean energy cost is : ", energy_total_rapl , "\n")
print("Total  reads are : ", total_reads , "\n")
energy_rapl = energy_total_rapl / total_reads #average energy caused by each rapl read
print("Average Rapl Read energy cost is : ", energy_rapl , "\n")

     
        
  
total_num =len(names)
names_set =set(names)
names_dict ={}
energies_bb ={}
for name in names_set:
    names_dict[name] = names.count(name)
    energies_bb[name] =[]




for key, value in names_dict.items():
    print(key, ' : ', value)



names_ll =[]
funcs_ll = set()
fake_funcs = set()
bb_code =dict()
counter =0


with open(str(sys.argv[2])) as file:
    for line in file:
        x =line.rstrip()
        if (x.startswith("Basic Block name: ")):
            x =x.replace("Basic Block name: ","")
            names_ll.append(x)
    
        if (x.startswith("Of function : ")):
            x =x.replace("Of function : ","")
            funcs_ll.add(x)
print("the set is \n")
print(funcs_ll)


print(names_ll)

for bb_name in names_ll:
    bb_code[bb_name] = []




in_func = False
tmp_str =""
inside_bb = False
f = open(str(sys.argv[4]), "w")


with open(str(sys.argv[3])) as file:
    for line in file:
        x =line.rstrip()
        if (x.endswith(">:")):
            m = re.search('<(.+?)>:', x).group(0)[1:-2]
            in_func = True
            inside_bb = False
            counter = 0
            if m in funcs_ll:
                f.write("New real function : ")
                f.write(m)
                f.write("\n")

            else :
                fake_funcs.add(m)
                f.write("New fake function : ")
                f.write(m)
                f.write("\n")
            
        elif (in_func == True) and (not x) :
            in_func = False
            f.write("\n")
        elif (in_func == True)  and x : 
            
            if x[32:].endswith("<print>"):
                inside_bb =True
                counter +=1
                if counter == 1:
                    tmp_str = m
                elif counter >1:
                    tmp_str = m+str(counter-1)

                f.write("Basic Block : ")
                f.write(tmp_str)
                f.write("\n")

            elif x[32:]:
                if inside_bb and (tmp_str in bb_code):
                    bb_code[tmp_str].append(x[32:])
                f.write(x[32:])
                f.write("\n")




with open(str(sys.argv[5]), 'w') as f:
    json.dump(bb_code, f)

for key, value in bb_code.items():
    print("\n")
    print("Basic Block : ", key ,"\n")
    for item in value :
        print(item)  
f.close()



regs =['%eax' , "%ebx" ,"%ecx", "%edx", "%cs", "%ds", "%es", "%fs", "%gs", "%ss","%esi", "%edi" , "%ebp", "%eip" ,"%esp", "%ax", "%bx", "%cx" , "%dx" ,"%ah" ,"%al" ,"%bh" ,"%bl" , "%ch" ,"%dh" ,"%dl" ,"%rax", "%rcx" ,"%rdx" ,"%rbx" ,"%rsp" ,"%rbp" ,"%rsi" ,"%rdi" ,"%sp" ,"%bp" ,"%si" ,"%di" ,"%spl" ,"%bpl" ,"%sil" ,"%dil" , "%ss" ,"%cs" ,"%ds" ,"%es" ,"%fs" ,"%gs" ,"%eflags" ,"%eip"  ]

df = pd.read_csv('opcodes.csv')
df =df.drop(df.columns[5], axis=1)
df.dropna(subset=['name'], inplace=True)
df =df.reset_index(drop=True)

with open(str(sys.argv[5])) as f:
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


        #print (opcodes,"\n")
        #print (x[0]," ", arg1," ",arg2," ",arg3," ","\n")

        if arg1 in regs:
            arg1 ="r"
        elif ('(' in arg1 ) and (')' in arg1 ):
            arg1 ="m"
        elif arg1.startswith('<') and arg1.endswith('>') :
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
        elif arg2.startswith('<') and arg2.endswith('>') :
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
        elif arg2.startswith('<') and arg3.endswith('>') :
            arg2 ="m"
        elif arg3.startswith("$0x"):
            arg3 ="I"
        elif arg3 == "%cl":
            arg3 ="cl"
        else :
            arg3 =""

        print (opcodes,"\n")
        print (x[0]," ", arg1," ",arg2," ",arg3," ","\n")

        
        df_temp = df.loc[df['name'] == x[0]]
        if df_temp.empty :
            df_temp = df.loc[df['name'] == x[0][:-1]]
        if df_temp.empty :
            df_temp = df.loc[df['name'] == x[0][:-2]]
        if df_temp.empty :
            df_temp = df.loc[df['name'] == x[0][:-3]]
        if df_temp.empty :
            df_temp = df.loc[df['name'] == x[0][:-4]]
        if df_temp.empty :
            print("Could not find opcode  : ", x[0] ,"\n")

        res_weight =3 
        
        if not df_temp.loc[(df_temp['op1'] == arg1) & (df_temp['op2'] == arg2) & (df_temp['op3'] == arg3)].empty :
            res_weight = df_temp.loc[(df_temp['op1'] == arg1) & (df_temp['op2'] == arg2) & (df_temp['op3'] == arg3)].iloc[0]['weight']
        elif not df_temp.loc[(df_temp['op1'] == arg1) & (df_temp['op2'] == arg2) ].empty :
            res_weight = df_temp.loc[(df_temp['op1'] == arg1) & (df_temp['op2'] == arg2) ].iloc[0]['weight']
        elif not df_temp.loc[(df_temp['op1'] == arg1) & (df_temp['op3'] == arg3) ].empty :
            res_weight = df_temp.loc[(df_temp['op1'] == arg1) & (df_temp['op3'] == arg3) ].iloc[0]['weight']
        elif not df_temp.loc[(df_temp['op3'] == arg3) & (df_temp['op2'] == arg2) ].empty :
            res_weight = df_temp.loc[(df_temp['op3'] == arg3) & (df_temp['op2'] == arg2) ].iloc[0]['weight']
        elif not df_temp.loc[df_temp['op1'] == arg1  ].empty :
            res_weight = df_temp.loc[df_temp['op1'] == arg1  ].iloc[0]['weight']
        elif not df_temp.loc[df_temp['op2'] == arg2  ].empty :
            res_weight = df_temp.loc[df_temp['op2'] == arg2  ].iloc[0]['weight']
        elif not df_temp.loc[df_temp['op3'] == arg3  ].empty :
            res_weight = df_temp.loc[df_temp['op3'] == arg3  ].iloc[0]['weight']
        elif not df_temp.empty :
            res_weight = df_temp.iloc[0]['weight']
        else :
            print (print("Could not find opcode  : ", x[0] ," ", arg1," ",arg2," ",arg3," ", "\n"))
        
        print ("the result weight is ", res_weight , "\n")
        weights[key] += float(res_weight)
        



        


        print(df_temp)
        print ("\n")
        #print(opcodes ,"\n")  


for item in weights.items():
    print(item)

for index, elem in enumerate(energy_value):
    total_weight =0
    for bb in energy_elements[index]:
        total_weight+= weights[bb]
    for bb in energy_elements[index]:
        energies_bb[bb].append((elem * weights[bb])/ total_weight)

for item in energies_bb.items():
    print(item)
    

    
with open(str(sys.argv[7]), 'w') as f:
    json.dump(energies_bb, f)


total_burnt_energy =0

for key, value in energies_bb.items():
    for i in value:
        total_burnt_energy +=i

print ("Total burnt energy is " , total_burnt_energy , energy_total , "\n")
#print(df.to_string()) 

