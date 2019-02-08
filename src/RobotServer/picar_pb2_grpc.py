# Generated by the gRPC Python protocol compiler plugin. DO NOT EDIT!
import grpc

import picar_pb2 as picar__pb2


class PiCarStub(object):
  """Interface exported by the server
  """

  def __init__(self, channel):
    """Constructor.

    Args:
      channel: A grpc.Channel.
    """
    self.ReceiveConnection = channel.unary_unary(
        '/CapstoneRobot.PiCar/ReceiveConnection',
        request_serializer=picar__pb2.ConnectRequest.SerializeToString,
        response_deserializer=picar__pb2.ConnectAck.FromString,
        )
    self.SwitchMode = channel.unary_unary(
        '/CapstoneRobot.PiCar/SwitchMode',
        request_serializer=picar__pb2.ModeRequest.SerializeToString,
        response_deserializer=picar__pb2.ModeAck.FromString,
        )
    self.RemoteControl = channel.stream_unary(
        '/CapstoneRobot.PiCar/RemoteControl',
        request_serializer=picar__pb2.SetMotion.SerializeToString,
        response_deserializer=picar__pb2.Empty.FromString,
        )
    self.StartStream = channel.unary_stream(
        '/CapstoneRobot.PiCar/StartStream',
        request_serializer=picar__pb2.StartStreaming.SerializeToString,
        response_deserializer=picar__pb2.StreamData.FromString,
        )
    self.StopStream = channel.unary_unary(
        '/CapstoneRobot.PiCar/StopStream',
        request_serializer=picar__pb2.StopStreaming.SerializeToString,
        response_deserializer=picar__pb2.Empty.FromString,
        )


class PiCarServicer(object):
  """Interface exported by the server
  """

  def ReceiveConnection(self, request, context):
    """Handshake between PiCar and desktop application
    """
    context.set_code(grpc.StatusCode.UNIMPLEMENTED)
    context.set_details('Method not implemented!')
    raise NotImplementedError('Method not implemented!')

  def SwitchMode(self, request, context):
    """Changes the operating mode of the PiCar
    """
    context.set_code(grpc.StatusCode.UNIMPLEMENTED)
    context.set_details('Method not implemented!')
    raise NotImplementedError('Method not implemented!')

  def RemoteControl(self, request_iterator, context):
    """Receive control data from desktop application
    """
    context.set_code(grpc.StatusCode.UNIMPLEMENTED)
    context.set_details('Method not implemented!')
    raise NotImplementedError('Method not implemented!')

  def StartStream(self, request, context):
    """Begin video/action streaming
    """
    context.set_code(grpc.StatusCode.UNIMPLEMENTED)
    context.set_details('Method not implemented!')
    raise NotImplementedError('Method not implemented!')

  def StopStream(self, request, context):
    """End video/action streaming
    """
    context.set_code(grpc.StatusCode.UNIMPLEMENTED)
    context.set_details('Method not implemented!')
    raise NotImplementedError('Method not implemented!')


def add_PiCarServicer_to_server(servicer, server):
  rpc_method_handlers = {
      'ReceiveConnection': grpc.unary_unary_rpc_method_handler(
          servicer.ReceiveConnection,
          request_deserializer=picar__pb2.ConnectRequest.FromString,
          response_serializer=picar__pb2.ConnectAck.SerializeToString,
      ),
      'SwitchMode': grpc.unary_unary_rpc_method_handler(
          servicer.SwitchMode,
          request_deserializer=picar__pb2.ModeRequest.FromString,
          response_serializer=picar__pb2.ModeAck.SerializeToString,
      ),
      'RemoteControl': grpc.stream_unary_rpc_method_handler(
          servicer.RemoteControl,
          request_deserializer=picar__pb2.SetMotion.FromString,
          response_serializer=picar__pb2.Empty.SerializeToString,
      ),
      'StartStream': grpc.unary_stream_rpc_method_handler(
          servicer.StartStream,
          request_deserializer=picar__pb2.StartStreaming.FromString,
          response_serializer=picar__pb2.StreamData.SerializeToString,
      ),
      'StopStream': grpc.unary_unary_rpc_method_handler(
          servicer.StopStream,
          request_deserializer=picar__pb2.StopStreaming.FromString,
          response_serializer=picar__pb2.Empty.SerializeToString,
      ),
  }
  generic_handler = grpc.method_handlers_generic_handler(
      'CapstoneRobot.PiCar', rpc_method_handlers)
  server.add_generic_rpc_handlers((generic_handler,))
