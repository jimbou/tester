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
clang -S -emit-llvm $1.c # -static -m64
llvm-as $1.ll
opt -load build/skeleton/libSkeletonPass.* -skeleton < $1.bc > $1_inst.bc  2> code_ll_$1.txt

llc -filetype=obj  $1_inst.bc 
echo "i am here"
gcc  -o $1 $1_inst.o  -O0  
chmod +x $1

objdump -d $1 > code_assembly_$1.txt
./$1 > run_results_$1.txt



python3 read_result.py run_results_$1.txt code_ll_$1.txt code_assembly_$1.txt cleaned_code_$1.txt $1_dict.json >final_dict_$1.txt
