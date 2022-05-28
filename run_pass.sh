#!/bin/bash

rm -r build
mkdir build
cd build
cmake ..
make
cd ..

clang -S -emit-llvm -Xclang -disable-O0-optnone $1.c
opt -load build/skeleton/libSkeletonPass.* -skeleton < $1.ll > $1.bc  2> $1_code2.txt
#clang -emit-llvm -c $1.c
#opt -load build/skeleton/libSkeletonPass.* -skeleton < $1.bc > $1_inst.bc

llc -filetype=obj $1_inst.bc
gcc -o $1 $1_inst.o -O0
chmod +x $1
