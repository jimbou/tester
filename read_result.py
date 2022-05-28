#!/usr/bin/python

import sys
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


