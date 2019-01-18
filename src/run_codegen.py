"""Runs protoc with the gRPC plugin to generate messages and gRPC stubs."""

from grpc_tools import protoc

import os

proto_path='protos'
python_out='RobotServer'
csharp_out='RobotClient/RobotClient'
protos='protos/picar.proto'

#Generate python code
protoc.main((
    '',
    '--proto_path='+proto_path,
    '--python_out='+python_out,
    '--grpc_python_out='+python_out,
    protos,
))

os.system('tools\protoc.exe -I' + proto_path + ' --csharp_out=' + csharp_out + ' --grpc_out=' + csharp_out + ' ' + protos + ' --plugin=protoc-gen-grpc=tools\grpc_csharp_plugin.exe')