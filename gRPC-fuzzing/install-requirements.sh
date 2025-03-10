#!/bin/bash

apt install python3-pip git libqt5x11extras5 python3-pyqt5.qtwebengine python3-pyqt5
apt install default-jdk
apt install python3-protobuf
apt install python3-grpc

#maybe not a good idea
sudo pip install grpcio-tools  --break-system-packages

cd ../external-tools/
git clone https://github.com/marin-m/pbtk
wget https://github.com/fullstorydev/grpcurl/releases/download/v1.9.2/grpcurl_1.9.2_linux_amd64.deb
dpkg -i grpcurl_1.9.2_linux_amd64.deb

cd ../gRPC-fuzzing

