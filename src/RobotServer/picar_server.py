"""Server run on each PiCar to listen to desktop application commands"""

from concurrent import futures
from time import sleep

import grpc
import cv2

import picar_pb2
import picar_pb2_grpc


class PiCarServicer(picar_pb2_grpc.PiCarServicer):
    """Provides methods that implement functionality of PiCar server."""

    def __init__(self, driver):
        self.driver = driver
        self.streaming = False

    def ReceiveConnection(self, request, context):
        """Handshake between PiCar and desktop application"""
        print('Received connection request from %s' % request.message)
        # Send a ConnectAck message showing success
        return picar_pb2.ConnectAck(success=True)

    def SwitchMode(self, request, context):
        """Changes the operating mode of the PiCar"""
        if self.driver.mode != request.mode:
            # If the request is for a different mode, send a success ack
            print('Switching mode from %s to %s' % (
                self.driver.mode, request.mode))
            self.driver.mode = request.mode
            return picar_pb2.ModeAck(success=True)
        else:
            # If the request is for the mode already in, send a failure ack
            print(
                    'Request received for mode %s, but already in that mode!' % request.mode)
            return picar_pb2.ModeAck(success=False)

    def RemoteControl(self, request, context):
        """Receive control data from desktop application"""
        # Clamp the input throttle and direction to [-1, 1]
        throttle = max(-1, min(request.throttle, 1))
        direction = max(-1, min(request.direction, 1))
        print('Setting wheels to %f throttle and %f steering' % (
            throttle, direction))
        self.driver.set_throttle_and_dir(throttle, direction)
        return picar_pb2.Empty()

    def VideoStream(self, request, context):
        """Send back images captured from webcam, encoded as jpeg"""
        self.streaming = True
        print('Starting video stream')

        while self.streaming:
            image = cv2.resize(self.driver.frame, (320, 240))
            _, b = cv2.imencode('.jpg', image)
            b = b.tobytes()

            message = picar_pb2.ImageCapture(
                image=b)  # Create message with image
            yield message  # Send it
            sleep(1 / 24)  # 24Hz refresh rate

    def StopStream(self, request, context):
        """Stop the sending of a video stream"""
        self.streaming = False
        print('Stopping video stream')
        return picar_pb2.Empty()

    def FollowerStream(self, request, context):
        """Send video feed and follower actions.

        If we are not a follower, the stream is empty."""

        # Empty the follower queue and start streaming
        self.driver.start_follower_streaming()
        print 'Starting follower stream'
        while self.driver.is_follower_streaming():
            follower_data = self.driver.follower_queue.get()
            image = cv2.resize(follower_data.frame, (320, 240))
            _, b = cv2.imencode('.jpg', image)
            b = b.tobytes()

            image_message = picar_pb2.ImageCapture(image=b)
            action = picar_pb2.SetMotion(throttle=follower_data.throttle,
                                         direction=follower_data.direction)
            message = picar_pb2.FollowerData(image=image_message,
                                             action=action)
            yield message

    def StopFollowerStream(self, request, context):
        """Stop the sending of the follower stream"""

        self.driver.stop_follower_streaming()
        print('Stopping follower stream')
        return picar_pb2.Empty()


def getServer(driver):
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    picar_pb2_grpc.add_PiCarServicer_to_server(
        PiCarServicer(driver), server)
    server.add_insecure_port('[::]:50051')
    return server
