#!/bin/bash

echo -e "Extracting .proto files from ../rootfs/sx/local/runtime/bin/user_terminal_frontend:\n"


../external-tools/pbtk/extractors/from_binary.py ../rootfs/sx/local/runtime/bin/user_terminal_frontend grpc_extracts/

echo -e "Replacing descriptor.proto ...\n"
#the original extractor.proto file extracted from the user_terminal_frontend does not seem to work with protoc
wget https://raw.githubusercontent.com/protocolbuffers/protobuf/refs/heads/main/src/google/protobuf/descriptor.proto
mv descriptor.proto grpc_extracts/google/protobuf/descriptor.proto

echo -e "Turning the .proto files into python scripts:\n"

mkdir grpc_python

find ./grpc_extracts/ -name "*.proto" | xargs python3 -m grpc_tools.protoc -I=grpc_extracts --python_out=grpc_python --grpc_python_out=grpc_python
