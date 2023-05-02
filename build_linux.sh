#!/bin/bash
#git pull
#this version copied from upstream
#python3 pre_linux.py
set -e
TARGET=linux-x86_64
CURRDIR=$PWD
FRIDA_SRC=${FRIDA_SRC:-~/github/frida}
(cd $FRIDA_SRC/releng; python3 devkit.py frida-core $TARGET $CURRDIR/devkit/linux)
(cd devkit/linux; python3 build_linux_map.py)

mkdir -p build_linux
(cd build_linux; cmake -DCMAKE_BUILD_TYPE=Release -DCMAKE_DEPENDS_USE_COMPILER=FALSE -G "CodeBlocks - Unix Makefiles" ..; make all)
SHARED_LIB=libfrida_shared.so
result=$(sha256sum build_linux/$SHARED_LIB | awk '{print $1}')
mkdir -p builds/$TARGET
cp build_linux/$SHARED_LIB builds/$TARGET/${result}-libinterceptor.so
echo BUILD COMPLETE: builds/$TARGET/${result}-libinterceptor.so
