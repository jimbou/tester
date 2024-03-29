#!/bin/bash



clang -S -emit-llvm $1.c
llvm-as $1.ll

opt -load build/skeleton/libSkeletonPass.* -skeleton < $1.bc > $1_inst.bc   2> code_ll_$1.txt #-enable-new-pm=0  add this for your pc but not for server
llc -filetype=obj  $1_inst.bc 
llvm-dis -o $1-debug.ll $1_inst.bc 
clang  -o $1 $1_inst.o  -O0  
chmod +x $1
 echo "Creation of modified  executable successfull"

objdump -d $1 > code_assembly_$1.txt
