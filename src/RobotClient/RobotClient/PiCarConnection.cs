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

        public const int CONNECTION_TIMEOUT_SECONDS = 2;

        private class PiCarClient
        {
            private readonly PiCar.PiCarClient _client;

            private readonly MainWindow _mainWindow = (MainWindow)Application.Current.MainWindow;

            private readonly AsyncClientStreamingCall<SetMotion, Empty> remoteControlCall;

            private const uint _exactMajorVersion = 1;
            private const uint _atLeastMinorVersion = 1;

            public PiCarClient(PiCar.PiCarClient client)
            {
                _client = client;
                remoteControlCall = _client.RemoteControl();
            }

            //Request a connection to the PiCar server. Return success
            public Tuple<bool, string> RequestConnect()
            {
                try
                {
                    //Attempt connection to PiCar server
                    var request = new ConnectRequest { Message = "Desktop App" };

                    var ack = _client.ReceiveConnection(request, new CallOptions(deadline: DateTime.UtcNow.AddSeconds(CONNECTION_TIMEOUT_SECONDS)));
                    var version = ack.Version;
                    string msg = null;

                    // Version ok
                    if (version.Major == _exactMajorVersion && version.Minor >= _atLeastMinorVersion)
                    {
                        msg = $"Protocol version {version.Major}.{version.Minor}.{version.Patch} ok\n";
                    } else // Version bad
                    {
                        msg = $"Expected major version {_exactMajorVersion} and minor version "
                            + $"at least {_atLeastMinorVersion}, but server returned "
                            + $"{version.Major}.{version.Minor}.{version.Patch}.\n";
                    }

                    return Tuple.Create(ack.Success, msg);
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

            //Set the model of the follower, return success
            public bool SetFollowerModel(int model)
            {
                try {
                    var request = new ModelVersion { Version = model };
                    var ack = _client.SwitchFollowerModel(request);

                    return ack.Success;
                }
                catch (RpcException e) {
                    Console.Write("RPC failed " + e);
                    throw;
                }
            }

            //Send a signal to the PiCar telling it how to move its wheels
            public void SetMotion(double throttle, double direction)
            {
                try
                {
                    // Send a control signal to the PiCar
                    var request = new SetMotion { Throttle = throttle, Direction = direction };
                    remoteControlCall.RequestStream.WriteAsync(request);
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
                    StartStreaming request = new StartStreaming { Decorate = true };

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

        public virtual Tuple<bool, string> RequestConnect()
        {
            return _client.RequestConnect();
        }

        public virtual void SetMode(ModeRequest.Types.Mode mode)
        {
            _client.SetMode(mode);
            Mode = mode;
        }

        public virtual void SetFollowerModel(int model)
        {
            _client.SetFollowerModel(model);
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

        public override Tuple<bool, string> RequestConnect()
        {
            return Tuple.Create(true, "");
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
