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
    self.RemoteControl = channel.unary_unary(
        '/CapstoneRobot.PiCar/RemoteControl',
        request_serializer=picar__pb2.SetMotion.SerializeToString,
        response_deserializer=picar__pb2.Empty.FromString,
        )
    self.VideoStream = channel.unary_stream(
        '/CapstoneRobot.PiCar/VideoStream',
        request_serializer=picar__pb2.StartVideoStream.SerializeToString,
        response_deserializer=picar__pb2.ImageCapture.FromString,
        )
    self.StopStream = channel.unary_unary(
        '/CapstoneRobot.PiCar/StopStream',
        request_serializer=picar__pb2.EndVideoStream.SerializeToString,
        response_deserializer=picar__pb2.Empty.FromString,
        )

    self.FollowerStream = channel.unary_stream(
        '/SeniorProjectRobot.PiCar/FollowerStream',
        request_serializer=picar__pb2.Empty.SerializeToString,
        response_deserializer=picar__pb2.FollowerData.FromString,
        )
    self.StopFollowerStream = channel.unary_unary(
        '/SeniorProjectRobot.PiCar/StopFollowerStream',
        request_serializer=picar__pb2.Empty.SerializeToString,
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

  def RemoteControl(self, request, context):
    """Receive control data from desktop application
    """
    context.set_code(grpc.StatusCode.UNIMPLEMENTED)
    context.set_details('Method not implemented!')
    raise NotImplementedError('Method not implemented!')

  def VideoStream(self, request, context):
    """Begin video streaming
    """
    context.set_code(grpc.StatusCode.UNIMPLEMENTED)
    context.set_details('Method not implemented!')
    raise NotImplementedError('Method not implemented!')

  def StopStream(self, request, context):
    """End video streaming
    """
    context.set_code(grpc.StatusCode.UNIMPLEMENTED)
    context.set_details('Method not implemented!')
    raise NotImplementedError('Method not implemented!')


  def FollowerStream(self, request, context):
    """Start follower stream
    """
    context.set_code(grpc.StatusCode.UNIMPLEMENTED)
    context.set_details('Method not implemented!')
    raise NotImplementedError('Method not implemented!')

  def StopFollowerStream(self, request, context):
    """End follower stream
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
      'RemoteControl': grpc.unary_unary_rpc_method_handler(
          servicer.RemoteControl,
          request_deserializer=picar__pb2.SetMotion.FromString,
          response_serializer=picar__pb2.Empty.SerializeToString,
      ),
      'VideoStream': grpc.unary_stream_rpc_method_handler(
          servicer.VideoStream,
          request_deserializer=picar__pb2.StartVideoStream.FromString,
          response_serializer=picar__pb2.ImageCapture.SerializeToString,
      ),
      'StopStream': grpc.unary_unary_rpc_method_handler(
          servicer.StopStream,
          request_deserializer=picar__pb2.EndVideoStream.FromString,
          response_serializer=picar__pb2.Empty.SerializeToString,
      ),
      'FollowerStream': grpc.unary_stream_rpc_method_handler(
          servicer.FollowerStream,
          request_deserializer=picar__pb2.Empty.FromString,
          response_serializer=picar__pb2.FollowerData.SerializeToString,
      ),
      'StopFollowerStream': grpc.unary_unary_rpc_method_handler(
          servicer.StopFollowerStream,
          request_deserializer=picar__pb2.Empty.FromString,
          response_serializer=picar__pb2.Empty.SerializeToString,
      ),
  }
  generic_handler = grpc.method_handlers_generic_handler(
      'CapstoneRobot.PiCar', rpc_method_handlers)
  server.add_generic_rpc_handlers((generic_handler,))
