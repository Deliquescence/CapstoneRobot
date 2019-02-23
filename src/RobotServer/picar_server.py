"""Server run on each PiCar to listen to desktop application commands"""

from concurrent import futures

import grpc
import cv2

import picar_pb2
import picar_pb2_grpc

# Increment major version for incompatible protocol API changes
# Increment minor version for backwards-compatible protocol API additions
# Increment patch version for backwards-compatible bug fixes
MAJOR_VERSION = 1
MINOR_VERSION = 0
PATCH_VERSION = 0


class PiCarServicer(picar_pb2_grpc.PiCarServicer):
    """Provides methods that implement functionality of PiCar server."""

    def __init__(self, driver):
        self.driver = driver
        self.streaming = False

    def ReceiveConnection(self, request, context):
        """Handshake between PiCar and desktop application"""
        print('Received connection request from %s' % request.message)
        print('Switching mode to idle')
        self.driver.mode = 0
        self.driver.set_throttle_and_dir(0.0, 0.0)
        # Send a ConnectAck message showing success with supported protocol version
        version = picar_pb2.SemVer(major=MAJOR_VERSION, minor=MINOR_VERSION, patch=PATCH_VERSION)
        return picar_pb2.ConnectAck(success=True, version=version)

    def SwitchMode(self, request, context):
        """Changes the operating mode of the PiCar"""
        if self.driver.mode != request.mode:
            # If the request is for a different mode, send a success ack
            print('Switching mode from %s to %s' % (self.driver.mode, request.mode))
            self.driver.mode = request.mode
            return picar_pb2.ModeAck(success=True)
        else:
            # If the request is for the mode already in, send a failure ack
            print('Request received for mode %s, but already in that mode!' % request.mode)
            return picar_pb2.ModeAck(success=False)

    def RemoteControl(self, request_iterator, context):
        """Receive control data from desktop application"""
        for set_motion in request_iterator:
            # Clamp the input throttle and direction to [-1, 1]
            throttle = max(-1, min(set_motion.throttle, 1))
            direction = max(-1, min(set_motion.direction, 1))
            print('Setting wheels to %f throttle and %f steering' % (throttle, direction))
            self.driver.set_throttle_and_dir(throttle, direction)
        # Stop car when stream ends
        self.driver.set_throttle_and_dir(0.0, 0.0)
        return picar_pb2.Empty()

    def StartStream(self, request, context):
        """Send video feed, throttle, and direction."""

        # Empty the stream queue and start streaming
        self.driver.start_streaming()
        print('Starting follower stream')
        while self.driver.is_streaming():
            stream_data = self.driver.stream_queue.get()
            image = cv2.resize(stream_data.frame, (320, 240))
            _, b = cv2.imencode('.jpg', image)
            b = b.tobytes()

            action = picar_pb2.SetMotion(throttle=stream_data.throttle,
                                         direction=stream_data.direction)
            message = picar_pb2.StreamData(image=b,
                                           action=action)
            yield message

    def StopStream(self, request, context):
        """Stop the sending of the follower stream"""

        self.driver.stop_streaming()
        print('Stopping follower stream')
        return picar_pb2.Empty()


def getServer(driver):
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    picar_pb2_grpc.add_PiCarServicer_to_server(
        PiCarServicer(driver), server)
    server.add_insecure_port('[::]:50051')
    return server
