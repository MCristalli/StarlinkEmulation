#!/bin/bash

set -e

echo -e "\nSplitting up dish partitions:"
python3 ../external-tools/starlink-tools/parts-extractor/parts-extractor.py $1 ../dish-partitions


echo -e "\nRemoving ECC from Linux A partition:"
python3 ../external-tools/starlink-tools/unecc/unecc.py ../dish-partitions/linux_a ../dish-partitions/linux_a_unecc

mkdir -p ../dish-partitions/linux_a_unecc_extract

echo -e "\nExtracting kernel image:"
dumpimage -T flat_dt -p 0 -o ../dish-partitions/linux_a_unecc_extract/kernel.lzma ../dish-partitions/linux_a_unecc

echo -e "\nExtracting ramdisk"
dumpimage -T flat_dt -p 28 -o ../dish-partitions/linux_a_unecc_extract/ramdisk.lzma ../dish-partitions/linux_a_unecc

#extract dtb

echo -e "\nUnpacking ramdisk:"
unlzma ../dish-partitions/linux_a_unecc_extract/ramdisk.lzma

mkdir -p ../rootfs
cd ../rootfs
cpio -idv < ../dish-partitions/linux_a_unecc_extract/ramdisk
cd ../setup-emulation

echo -e "\nUnpacking runtime:"
dd if=../dish-partitions/sx_a of=../dish-partitions/sx_a_stripped bs=1024 skip=4

mkdir -p ../dish-partitions/sx_a_extract
python3 ../external-tools/romfsck2/romfsck2.py -p -x ../dish-partitions/sx_a_extract ../dish-partitions/sx_a_stripped
cd ../dish-partitions/sx_a_extract
unlzma < runtime.tar.lz | tar x
cp -a . ../../rootfs/sx/local/runtime/
cd ../../setup-emulation

echo -e "\nUnpacking version info:"
dd if=../dish-partitions/version_a of=../dish-partitions/version_a_stripped bs=1024 skip=4

mkdir -p ../dish-partitions/version_a_extract
python3 ../external-tools/romfsck2/romfsck2.py -p -x ../dish-partitions/version_a_extract ../dish-partitions/version_a_stripped


echo -e "\nDone!"
