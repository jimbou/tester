#!/bin/bash

rm -r build
mkdir build
cd build
cmake ..
make
cd ..

#clang -S -emit-llvm -Xclang -disable-O0-optnone $1.c
#llvm-as $1.ll
#opt -load build/skeleton/libSkeletonPass.* -skeleton < $1.bc > $1_inst.bc  2> $1_code2.txt
#clang -emit-llvm -c $1.c
#llvm-dis $1.bc
#rm $1.bc


clang -o rapl_read rapl_read.c
chmod +x rapl_read  
#here we have compiled a script that reads  rapl energy




clang -S -emit-llvm $1.c # -static -m64
llvm-as $1.ll
 #here we have cretaed the original bc file unmodified by pass
 echo "Creation of unmodified bc successfull"

llc -filetype=obj  $1.bc 
gcc  -o $1_unchanged $1.o  -O0  
chmod +x $1_unchanged
#here we have created an unmodified executable
 echo "Creation of unmodified executable successfull"

./rapl_read >$1_unchanged_energy.txt  #read energy value then run unmodified code then read energy again
./$1_unchanged > dontcare.txt
./rapl_read >>$1_unchanged_energy.txt
#we run the unmodified executable


opt -load build/skeleton/libSkeletonPass.* -skeleton < $1.bc > $1_inst.bc  2> code_ll_$1.txt  

 echo "Applying of the llvm pass successfull"

llc -filetype=obj  $1_inst.bc 
gcc  -o $1 $1_inst.o  -O0  
chmod +x $1
 echo "Creation of modified  executable successfull"

objdump -d $1 > code_assembly_$1.txt
./$1 > run_results_$1.txt



#python3 read_result.py run_results_$1.txt code_ll_$1.txt code_assembly_$1.txt cleaned_code_$1.txt $1_dict.json $1_unchanged_energy.txt $1_energy_dict.json >final_dict_$1.txt
 echo "Run of python script successfull"
  echo "Results in final_dict_$1.txt"
