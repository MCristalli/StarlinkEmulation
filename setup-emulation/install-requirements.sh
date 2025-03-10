#!/bin/sh

sudo apt update
sudo apt-get update

sudo apt-get install -y git
sudo apt-get install -y wget
sudo apt-get install -y make

sudo apt install -y net-tools
sudo apt-get install -y flex
sudo apt-get install -y bison
sudo apt install -y bc
sudo apt-get install -y pkg-config
sudo apt-get install -y libncurses5-dev libncursesw5-dev
sudo apt install -y u-boot-tools
sudo apt install -y gcc-aarch64-linux-gnu
sudo apt-get install -y make build-essential libncurses-dev libssl-dev libelf-dev
sudo apt install -y qemu-system-arm
sudo apt-get install -y device-tree-compiler
sudo apt-get install -y bridge-utils
sudo apt-get install -y iptables

cd ..
mkdir external-tools
cd external-tools
git clone https://github.com/quarkslab/starlink-tools
git clone https://github.com/JordanMilne/romfsck2
cd ../setup-emulation
