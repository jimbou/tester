#!/bin/bash

rm -r build
mkdir build
cd build
cmake ..
make
cd ..

clang -emit-llvm -c $1.c
opt -load build/skeleton/libSkeletonPass.* -skeleton < $1.bc > $1 

chmod +x $1
