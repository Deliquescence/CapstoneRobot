using System;
using System.Collections.Generic;
using System.Threading.Tasks;
using System.Windows.Media.Imaging;
using System.Windows;
using Grpc.Core;
using System.Windows.Media;

namespace RobotClient
{
    public class PiCarConnection
    {
        //TODO figure this out
        public const double SPEED_AT_MAX_THROTTLE = 1.0;

        private class PiCarClient
        {
            private readonly PiCar.PiCarClient _client;

            private readonly MainWindow _mainWindow = (MainWindow)Application.Current.MainWindow;

            public PiCarClient(PiCar.PiCarClient client)
            {
                _client = client;
            }

            //Request a connection to the PiCar server. Return success
            public bool RequestConnect()
            {
                try
                {
                    //Attempt connection to PiCar server
                    var request = new ConnectRequest {Message = "Desktop App"};
                    var ack = _client.ReceiveConnection(request);

                    return ack.Success;
                }
                catch (RpcException e)
                {
                    Console.Write("RPC failed " + e);
                    throw;
                }
            }

            //Set the mode of the PiCar, return success
            public bool SetMode(ModeRequest.Types.Mode mode)
            {
                try
                {
                    var request = new ModeRequest {Mode = mode};
                    var ack = _client.SwitchMode(request);

                    return ack.Success;
                }
                catch (RpcException e)
                {
                    Console.Write("RPC failed " + e);
                    throw;
                }
            }

            //Send a signal to the PiCar telling it how to move its wheels
            public void SetMotion(double throttle, double direction)
            {
                try
                {
                    //Send a control signal to the PiCar
                    var request = new SetMotion {Throttle = throttle, Direction = direction};
                    _client.RemoteControl(request);
                }
                catch (RpcException e)
                {
                    Console.Write("RPC failed " + e);
                    throw;
                }
            }

            //Start getting the video stream
            public async Task StartStream()
            {
                try
                {
                    StartStreaming request = new StartStreaming();

                    using (var call = _client.StartStream(request))
                    {
                        var responseStream = call.ResponseStream;

                        while (await responseStream.MoveNext())
                        {
                            var imageBytes = responseStream.Current.Image.ToByteArray();
                            var carAction = responseStream.Current.Action;

                            //Call update UI
                            _mainWindow.HandleStream(imageBytes, carAction);
                        }
                    }
                }
                catch (RpcException e)
                {
                    Console.Write("RPC failed " + e);
                    throw;
                }
            }

            //Stop the video stream
            public void StopStream()
            {
                try
                {
                    //Send a control signal to the PiCar
                    var request = new StopStreaming();
                    _client.StopStream(request);
                }
                catch (RpcException e)
                {
                    Console.Write("RPC failed " + e);
                    throw;
                }
            }
        }

        private Channel _channel;
        private PiCarClient _client;
        public string Name;
        public string ipAddress;
        public ModeRequest.Types.Mode Mode;
        private bool currentlyMirroring;

        public PiCarConnection()
        {
            Name = "Default";
            ipAddress = "127.0.0.1";
            Mode = ModeRequest.Types.Mode.Idle;
            currentlyMirroring = false;
        }

        public PiCarConnection(string name, string ipAddress)
        {
            this.Name = name;
            this.ipAddress = ipAddress;
            _channel = new Channel(ipAddress + ":50051", ChannelCredentials.Insecure);
            _client = new PiCarClient(new PiCar.PiCarClient(_channel));
            Mode = ModeRequest.Types.Mode.Idle; //Start in Idle mode
            currentlyMirroring = false;
        }

        //getter and setter to find out if the picar is mirroring
        public void SetMirroring(bool b)
        {
            currentlyMirroring = b;
        }
        public bool isMirroring()
        {
            return currentlyMirroring;
        }

        public virtual bool RequestConnect()
        {
            return _client.RequestConnect();
        }

        public virtual void SetMode(ModeRequest.Types.Mode mode)
        {
            var success = _client.SetMode(mode);
            //Change local mode if successful
            if (success)
                Mode = mode;
        }

        public virtual void SetMotion(double throttle, double direction)
        {
            _client.SetMotion(throttle, direction);
        }

        public virtual Task StartStream()
        {
            return _client.StartStream();
        }

        public virtual void StopStream()
        {
            _client.StopStream(); //End the video stream
        }

        public override string ToString()
        {
            return Name;
        }

        public async Task Shutdown()
        {
            await _channel.ShutdownAsync();
        }
    }

    public class DummyConnection : PiCarConnection
    {
        public DummyConnection(string name, string ipAddress)
        {
            Name = name;
            this.ipAddress = ipAddress;
            Mode = ModeRequest.Types.Mode.Idle;
        }

        public override bool RequestConnect()
        {
            return true;
        }

        public override void SetMode(ModeRequest.Types.Mode mode)
        {
            Mode = mode;
        }

        public override void SetMotion(double throttle, double direction){}

        public override Task StartStream() { return null;  }

        public override void StopStream() { }
    }
}
