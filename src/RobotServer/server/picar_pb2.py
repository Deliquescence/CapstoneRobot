# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: picar.proto

import sys
_b=sys.version_info[0]<3 and (lambda x:x) or (lambda x:x.encode('latin1'))
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from google.protobuf import reflection as _reflection
from google.protobuf import symbol_database as _symbol_database
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()




DESCRIPTOR = _descriptor.FileDescriptor(
  name='picar.proto',
  package='CapstoneRobot',
  syntax='proto3',
  serialized_options=_b('\252\002\013RobotClient'),
  serialized_pb=_b('\n\x0bpicar.proto\x12\rCapstoneRobot\"\x1f\n\x0cModelVersion\x12\x0f\n\x07version\x18\x01 \x01(\x05\"!\n\x0eSwitchModelAck\x12\x0f\n\x07success\x18\x01 \x01(\x08\"\x07\n\x05\x45mpty\"!\n\x0e\x43onnectRequest\x12\x0f\n\x07message\x18\x01 \x01(\t\"E\n\nConnectAck\x12\x0f\n\x07success\x18\x01 \x01(\x08\x12&\n\x07version\x18\x02 \x01(\x0b\x32\x15.CapstoneRobot.SemVer\"5\n\x06SemVer\x12\r\n\x05major\x18\x01 \x01(\r\x12\r\n\x05minor\x18\x02 \x01(\r\x12\r\n\x05patch\x18\x03 \x01(\r\"d\n\x0bModeRequest\x12-\n\x04mode\x18\x01 \x01(\x0e\x32\x1f.CapstoneRobot.ModeRequest.Mode\"&\n\x04Mode\x12\x08\n\x04IDLE\x10\x00\x12\x08\n\x04LEAD\x10\x01\x12\n\n\x06\x46OLLOW\x10\x02\"\x1a\n\x07ModeAck\x12\x0f\n\x07success\x18\x01 \x01(\x08\"0\n\tSetMotion\x12\x10\n\x08throttle\x18\x01 \x01(\x01\x12\x11\n\tdirection\x18\x02 \x01(\x01\"\"\n\x0eStartStreaming\x12\x10\n\x08\x64\x65\x63orate\x18\x01 \x01(\x08\"\x0f\n\rStopStreaming\"E\n\nStreamData\x12\r\n\x05image\x18\x01 \x01(\x0c\x12(\n\x06\x61\x63tion\x18\x02 \x01(\x0b\x32\x18.CapstoneRobot.SetMotion2\xc7\x03\n\x05PiCar\x12O\n\x11ReceiveConnection\x12\x1d.CapstoneRobot.ConnectRequest\x1a\x19.CapstoneRobot.ConnectAck\"\x00\x12\x42\n\nSwitchMode\x12\x1a.CapstoneRobot.ModeRequest\x1a\x16.CapstoneRobot.ModeAck\"\x00\x12\x43\n\rRemoteControl\x12\x18.CapstoneRobot.SetMotion\x1a\x14.CapstoneRobot.Empty\"\x00(\x01\x12K\n\x0bStartStream\x12\x1d.CapstoneRobot.StartStreaming\x1a\x19.CapstoneRobot.StreamData\"\x00\x30\x01\x12\x42\n\nStopStream\x12\x1c.CapstoneRobot.StopStreaming\x1a\x14.CapstoneRobot.Empty\"\x00\x12S\n\x13SwitchFollowerModel\x12\x1b.CapstoneRobot.ModelVersion\x1a\x1d.CapstoneRobot.SwitchModelAck\"\x00\x42\x0e\xaa\x02\x0bRobotClientb\x06proto3')
)



_MODEREQUEST_MODE = _descriptor.EnumDescriptor(
  name='Mode',
  full_name='CapstoneRobot.ModeRequest.Mode',
  filename=None,
  file=DESCRIPTOR,
  values=[
    _descriptor.EnumValueDescriptor(
      name='IDLE', index=0, number=0,
      serialized_options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='LEAD', index=1, number=1,
      serialized_options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='FOLLOW', index=2, number=2,
      serialized_options=None,
      type=None),
  ],
  containing_type=None,
  serialized_options=None,
  serialized_start=330,
  serialized_end=368,
)
_sym_db.RegisterEnumDescriptor(_MODEREQUEST_MODE)


_MODELVERSION = _descriptor.Descriptor(
  name='ModelVersion',
  full_name='CapstoneRobot.ModelVersion',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='version', full_name='CapstoneRobot.ModelVersion.version', index=0,
      number=1, type=5, cpp_type=1, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=30,
  serialized_end=61,
)


_SWITCHMODELACK = _descriptor.Descriptor(
  name='SwitchModelAck',
  full_name='CapstoneRobot.SwitchModelAck',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='success', full_name='CapstoneRobot.SwitchModelAck.success', index=0,
      number=1, type=8, cpp_type=7, label=1,
      has_default_value=False, default_value=False,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=63,
  serialized_end=96,
)


_EMPTY = _descriptor.Descriptor(
  name='Empty',
  full_name='CapstoneRobot.Empty',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=98,
  serialized_end=105,
)


_CONNECTREQUEST = _descriptor.Descriptor(
  name='ConnectRequest',
  full_name='CapstoneRobot.ConnectRequest',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='message', full_name='CapstoneRobot.ConnectRequest.message', index=0,
      number=1, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=107,
  serialized_end=140,
)


_CONNECTACK = _descriptor.Descriptor(
  name='ConnectAck',
  full_name='CapstoneRobot.ConnectAck',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='success', full_name='CapstoneRobot.ConnectAck.success', index=0,
      number=1, type=8, cpp_type=7, label=1,
      has_default_value=False, default_value=False,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='version', full_name='CapstoneRobot.ConnectAck.version', index=1,
      number=2, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=142,
  serialized_end=211,
)


_SEMVER = _descriptor.Descriptor(
  name='SemVer',
  full_name='CapstoneRobot.SemVer',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='major', full_name='CapstoneRobot.SemVer.major', index=0,
      number=1, type=13, cpp_type=3, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='minor', full_name='CapstoneRobot.SemVer.minor', index=1,
      number=2, type=13, cpp_type=3, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='patch', full_name='CapstoneRobot.SemVer.patch', index=2,
      number=3, type=13, cpp_type=3, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=213,
  serialized_end=266,
)


_MODEREQUEST = _descriptor.Descriptor(
  name='ModeRequest',
  full_name='CapstoneRobot.ModeRequest',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='mode', full_name='CapstoneRobot.ModeRequest.mode', index=0,
      number=1, type=14, cpp_type=8, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
    _MODEREQUEST_MODE,
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=268,
  serialized_end=368,
)


_MODEACK = _descriptor.Descriptor(
  name='ModeAck',
  full_name='CapstoneRobot.ModeAck',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='success', full_name='CapstoneRobot.ModeAck.success', index=0,
      number=1, type=8, cpp_type=7, label=1,
      has_default_value=False, default_value=False,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=370,
  serialized_end=396,
)


_SETMOTION = _descriptor.Descriptor(
  name='SetMotion',
  full_name='CapstoneRobot.SetMotion',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='throttle', full_name='CapstoneRobot.SetMotion.throttle', index=0,
      number=1, type=1, cpp_type=5, label=1,
      has_default_value=False, default_value=float(0),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='direction', full_name='CapstoneRobot.SetMotion.direction', index=1,
      number=2, type=1, cpp_type=5, label=1,
      has_default_value=False, default_value=float(0),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=398,
  serialized_end=446,
)


_STARTSTREAMING = _descriptor.Descriptor(
  name='StartStreaming',
  full_name='CapstoneRobot.StartStreaming',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='decorate', full_name='CapstoneRobot.StartStreaming.decorate', index=0,
      number=1, type=8, cpp_type=7, label=1,
      has_default_value=False, default_value=False,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=448,
  serialized_end=482,
)


_STOPSTREAMING = _descriptor.Descriptor(
  name='StopStreaming',
  full_name='CapstoneRobot.StopStreaming',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=484,
  serialized_end=499,
)


_STREAMDATA = _descriptor.Descriptor(
  name='StreamData',
  full_name='CapstoneRobot.StreamData',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='image', full_name='CapstoneRobot.StreamData.image', index=0,
      number=1, type=12, cpp_type=9, label=1,
      has_default_value=False, default_value=_b(""),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='action', full_name='CapstoneRobot.StreamData.action', index=1,
      number=2, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=501,
  serialized_end=570,
)

_CONNECTACK.fields_by_name['version'].message_type = _SEMVER
_MODEREQUEST.fields_by_name['mode'].enum_type = _MODEREQUEST_MODE
_MODEREQUEST_MODE.containing_type = _MODEREQUEST
_STREAMDATA.fields_by_name['action'].message_type = _SETMOTION
DESCRIPTOR.message_types_by_name['ModelVersion'] = _MODELVERSION
DESCRIPTOR.message_types_by_name['SwitchModelAck'] = _SWITCHMODELACK
DESCRIPTOR.message_types_by_name['Empty'] = _EMPTY
DESCRIPTOR.message_types_by_name['ConnectRequest'] = _CONNECTREQUEST
DESCRIPTOR.message_types_by_name['ConnectAck'] = _CONNECTACK
DESCRIPTOR.message_types_by_name['SemVer'] = _SEMVER
DESCRIPTOR.message_types_by_name['ModeRequest'] = _MODEREQUEST
DESCRIPTOR.message_types_by_name['ModeAck'] = _MODEACK
DESCRIPTOR.message_types_by_name['SetMotion'] = _SETMOTION
DESCRIPTOR.message_types_by_name['StartStreaming'] = _STARTSTREAMING
DESCRIPTOR.message_types_by_name['StopStreaming'] = _STOPSTREAMING
DESCRIPTOR.message_types_by_name['StreamData'] = _STREAMDATA
_sym_db.RegisterFileDescriptor(DESCRIPTOR)

ModelVersion = _reflection.GeneratedProtocolMessageType('ModelVersion', (_message.Message,), dict(
  DESCRIPTOR = _MODELVERSION,
  __module__ = 'picar_pb2'
  # @@protoc_insertion_point(class_scope:CapstoneRobot.ModelVersion)
  ))
_sym_db.RegisterMessage(ModelVersion)

SwitchModelAck = _reflection.GeneratedProtocolMessageType('SwitchModelAck', (_message.Message,), dict(
  DESCRIPTOR = _SWITCHMODELACK,
  __module__ = 'picar_pb2'
  # @@protoc_insertion_point(class_scope:CapstoneRobot.SwitchModelAck)
  ))
_sym_db.RegisterMessage(SwitchModelAck)

Empty = _reflection.GeneratedProtocolMessageType('Empty', (_message.Message,), dict(
  DESCRIPTOR = _EMPTY,
  __module__ = 'picar_pb2'
  # @@protoc_insertion_point(class_scope:CapstoneRobot.Empty)
  ))
_sym_db.RegisterMessage(Empty)

ConnectRequest = _reflection.GeneratedProtocolMessageType('ConnectRequest', (_message.Message,), dict(
  DESCRIPTOR = _CONNECTREQUEST,
  __module__ = 'picar_pb2'
  # @@protoc_insertion_point(class_scope:CapstoneRobot.ConnectRequest)
  ))
_sym_db.RegisterMessage(ConnectRequest)

ConnectAck = _reflection.GeneratedProtocolMessageType('ConnectAck', (_message.Message,), dict(
  DESCRIPTOR = _CONNECTACK,
  __module__ = 'picar_pb2'
  # @@protoc_insertion_point(class_scope:CapstoneRobot.ConnectAck)
  ))
_sym_db.RegisterMessage(ConnectAck)

SemVer = _reflection.GeneratedProtocolMessageType('SemVer', (_message.Message,), dict(
  DESCRIPTOR = _SEMVER,
  __module__ = 'picar_pb2'
  # @@protoc_insertion_point(class_scope:CapstoneRobot.SemVer)
  ))
_sym_db.RegisterMessage(SemVer)

ModeRequest = _reflection.GeneratedProtocolMessageType('ModeRequest', (_message.Message,), dict(
  DESCRIPTOR = _MODEREQUEST,
  __module__ = 'picar_pb2'
  # @@protoc_insertion_point(class_scope:CapstoneRobot.ModeRequest)
  ))
_sym_db.RegisterMessage(ModeRequest)

ModeAck = _reflection.GeneratedProtocolMessageType('ModeAck', (_message.Message,), dict(
  DESCRIPTOR = _MODEACK,
  __module__ = 'picar_pb2'
  # @@protoc_insertion_point(class_scope:CapstoneRobot.ModeAck)
  ))
_sym_db.RegisterMessage(ModeAck)

SetMotion = _reflection.GeneratedProtocolMessageType('SetMotion', (_message.Message,), dict(
  DESCRIPTOR = _SETMOTION,
  __module__ = 'picar_pb2'
  # @@protoc_insertion_point(class_scope:CapstoneRobot.SetMotion)
  ))
_sym_db.RegisterMessage(SetMotion)

StartStreaming = _reflection.GeneratedProtocolMessageType('StartStreaming', (_message.Message,), dict(
  DESCRIPTOR = _STARTSTREAMING,
  __module__ = 'picar_pb2'
  # @@protoc_insertion_point(class_scope:CapstoneRobot.StartStreaming)
  ))
_sym_db.RegisterMessage(StartStreaming)

StopStreaming = _reflection.GeneratedProtocolMessageType('StopStreaming', (_message.Message,), dict(
  DESCRIPTOR = _STOPSTREAMING,
  __module__ = 'picar_pb2'
  # @@protoc_insertion_point(class_scope:CapstoneRobot.StopStreaming)
  ))
_sym_db.RegisterMessage(StopStreaming)

StreamData = _reflection.GeneratedProtocolMessageType('StreamData', (_message.Message,), dict(
  DESCRIPTOR = _STREAMDATA,
  __module__ = 'picar_pb2'
  # @@protoc_insertion_point(class_scope:CapstoneRobot.StreamData)
  ))
_sym_db.RegisterMessage(StreamData)


DESCRIPTOR._options = None

_PICAR = _descriptor.ServiceDescriptor(
  name='PiCar',
  full_name='CapstoneRobot.PiCar',
  file=DESCRIPTOR,
  index=0,
  serialized_options=None,
  serialized_start=573,
  serialized_end=1028,
  methods=[
  _descriptor.MethodDescriptor(
    name='ReceiveConnection',
    full_name='CapstoneRobot.PiCar.ReceiveConnection',
    index=0,
    containing_service=None,
    input_type=_CONNECTREQUEST,
    output_type=_CONNECTACK,
    serialized_options=None,
  ),
  _descriptor.MethodDescriptor(
    name='SwitchMode',
    full_name='CapstoneRobot.PiCar.SwitchMode',
    index=1,
    containing_service=None,
    input_type=_MODEREQUEST,
    output_type=_MODEACK,
    serialized_options=None,
  ),
  _descriptor.MethodDescriptor(
    name='RemoteControl',
    full_name='CapstoneRobot.PiCar.RemoteControl',
    index=2,
    containing_service=None,
    input_type=_SETMOTION,
    output_type=_EMPTY,
    serialized_options=None,
  ),
  _descriptor.MethodDescriptor(
    name='StartStream',
    full_name='CapstoneRobot.PiCar.StartStream',
    index=3,
    containing_service=None,
    input_type=_STARTSTREAMING,
    output_type=_STREAMDATA,
    serialized_options=None,
  ),
  _descriptor.MethodDescriptor(
    name='StopStream',
    full_name='CapstoneRobot.PiCar.StopStream',
    index=4,
    containing_service=None,
    input_type=_STOPSTREAMING,
    output_type=_EMPTY,
    serialized_options=None,
  ),
  _descriptor.MethodDescriptor(
    name='SwitchFollowerModel',
    full_name='CapstoneRobot.PiCar.SwitchFollowerModel',
    index=5,
    containing_service=None,
    input_type=_MODELVERSION,
    output_type=_SWITCHMODELACK,
    serialized_options=None,
  ),
])
_sym_db.RegisterServiceDescriptor(_PICAR)

DESCRIPTOR.services_by_name['PiCar'] = _PICAR

# @@protoc_insertion_point(module_scope)
