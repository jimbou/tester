#!/usr/bin/python

import sys
import re
import json
names = []


with open(str(sys.argv[1])) as file:
    for line in file:
        x =line.rstrip()
        if (x.startswith("Basic Block : ")):
            x =x.replace("Basic Block : ","")
            names.append(x)
        
  
total_num =len(names)
names_set =set(names)
names_dict ={}
for name in names_set:
    names_dict[name] = names.count(name)




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

