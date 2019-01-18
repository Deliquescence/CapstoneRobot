using System;
using System.Collections.Generic;
using System.Diagnostics;
using System.Linq;
using System.Net;
using System.Net.NetworkInformation;
using System.Net.Sockets;
using System.Threading.Tasks;
using System.Windows;
using System.Windows.Controls;
using Grpc.Core;
using System.ComponentModel;

namespace RobotClient
{
    public partial class Registration
    {
        private List<string[]> deviceStringList = new List<string[]>();
        private readonly MainWindow _mainWindow = (MainWindow)Application.Current.MainWindow;

        private readonly string _defaultGateway;
        private string _scanningIp;

        private readonly int _timeout = 2000;
        private int _devicesFound;

        private static readonly object LockObj = new object();
        private TimeSpan _ts;
        private readonly BackgroundWorker _backgroundWorker1 = new BackgroundWorker();


        /**
         *
         */
        private void InitializeBackgroundWorker() //initalizes the backgroundworker
        {
            _backgroundWorker1.DoWork += BackgroundWorker1_DoWorkAsync;
            
        }

        /**
         * Constructor for Registration Window
         * Checks for gateway IP and sets the output.
         */
        public Registration()
        {
            InitializeComponent();
            InitializeBackgroundWorker();


            _backgroundWorker1.WorkerSupportsCancellation = true; //Makes the backgroundworker able to recieve cancellation requests

            CancelButton.IsEnabled = false;

            //Finds default gateway IP
            DeviceList.ItemsSource = null;
            DeviceList.ItemsSource = deviceStringList.Select(array => array.FirstOrDefault());
            try
            {
                foreach (var curInterface in NetworkInterface.GetAllNetworkInterfaces())
                {
                    if (curInterface.OperationalStatus != OperationalStatus.Up) continue;
                    foreach (var gatewayOutput in curInterface.GetIPProperties()
                        .GatewayAddresses)
                    {
                        _defaultGateway = gatewayOutput.Address.ToString();
                    }
                }
            }
            catch(NetworkInformationException exception)
            {
                LogFieldReg.AppendText(DateTime.Now + ":\tDevice not connected to the internet! " + exception);
                this.Close();
            }
            
            _defaultGateway = _defaultGateway.Substring(0, _defaultGateway.Length - 1);
            LogFieldReg.AppendText("The gateway IP is " + _defaultGateway + "x\n");
            _mainWindow.LogField.AppendText(DateTime.Now + ":\tThe gateway IP is " + _defaultGateway + "x\n");

        }

        private void Window_Closing(object sender, CancelEventArgs e)
        {
            _mainWindow.Register = null;
        }

        /**
         * Function for initiating IP scan
         */
            private void ButtonScan(object sender, RoutedEventArgs e)
        {
            buttonScan.IsEnabled = false;
            Scan.IsEnabled = false;
            deviceStringList.Clear();
            DeviceList.ItemsSource = null;

            //Dummy device for testing:
            //deviceStringList.Add(new[] { "Dummy1", "DummyIP", "Default" });
            //deviceStringList.Add(new[] { "Dummy2", "DummyIP", "Default" });
            //deviceStringList.Add(new[] { "Dummy3", "DummyIP", "Default" });

            deviceStringList.Add(new[] { "Local Server", "127.0.0.1", "Default" });
            DeviceList.ItemsSource = deviceStringList.Select(array => array.FirstOrDefault());
            _ts = TimeSpan.Zero;
            _backgroundWorker1.RunWorkerAsync();
        }

        /**
         *
         */
        private async void BackgroundWorker1_DoWorkAsync(object sender, DoWorkEventArgs e)
        {
            var tasks = new List<Task>(); //sets tasks to be a new List of Tasks
            _devicesFound = 0; //sets devices found to 0
            Dispatcher.Invoke(() => //making changes to the main thread
            {
                LogFieldReg.AppendText("Starting scan\n");
                _mainWindow.LogField.AppendText(DateTime.Now + ":\tStarting scan\n");
                buttonScan.IsEnabled = false;
                CancelButton.IsEnabled = true;
                Scan.IsEnabled = false;
            }); //end of current changes to the main thread
            var stopWatch = new Stopwatch(); //wipes the stopwatch
            stopWatch.Start(); //starts the stopwatch

            for (var i = 1; i <= 255; i++) //for the entire local ip range
            {
                _scanningIp = _defaultGateway + i;
                var p = new Ping();

                var task = AsyncUpdate(p, _scanningIp); //make a task to ping and identify the current IP
                tasks.Add(task); //add it to the task list

                if (_backgroundWorker1.CancellationPending) //if a cancellation request has been sent
                {
                    Dispatcher.Invoke(() =>
                    {
                        tasks.Clear(); //wipe the task list
                        LogFieldReg.AppendText("Scan aborted \n");
                        _mainWindow.LogField.AppendText("Scan aborted\n");
                    });
                    break; //break out of the ip for loop scan
                }
            }
            await Task.WhenAll(tasks); //asyncronously wait for all the tasks to complete

            stopWatch.Stop(); //stop the stopwatch
            _ts = stopWatch.Elapsed;   //assign the time it took to a variable        

            Dispatcher.Invoke(() =>
            {
                LogFieldReg.AppendText("Finsished scan (" + _ts.TotalSeconds + " seconds)\nDetected " + _devicesFound + " devices\n");
                _mainWindow.LogField.AppendText(DateTime.Now + ":\tFinsished scan: " + _ts.TotalSeconds + " seconds\n" + DateTime.Now + "\tDetected " + _devicesFound + " devices\n");
                buttonScan.IsEnabled = true;
                CancelButton.IsEnabled = false;
                Scan.IsEnabled = true;
            });

        }

        /**
         *
         */
        private async Task AsyncUpdate(Ping ping, string ip)
        {
            var response = await ping.SendPingAsync(ip, _timeout); //set the response to the results of the ping

            if (response.Status == IPStatus.Success) //is a response is returned
            {
                string deviceName;
                try
                {
                    deviceName = Dns.GetHostEntry(ip).HostName; //try to get the device name
                }
                catch (SocketException eS)
                {
                    deviceName = "Unknown @ " + ip; //set to unknown @ ip if failed
                    Console.WriteLine(eS);
                }

                Dispatcher.Invoke(() =>
                {
                    deviceStringList.Add(new[] { deviceName, ip, "Default" }); //add the device to the listbox
                    DeviceList.ItemsSource = deviceStringList.Select(array => array.FirstOrDefault());
                    lock (LockObj)
                    {
                        _devicesFound++;
                    }
                });
        }
        }

        /**
         *
         */
        private void ButtonScanCancel(object sender, RoutedEventArgs e) => _backgroundWorker1.CancelAsync(); //cancel button sends cancellation request

        /**
         * Function for when the selected device changes in the registration window, which sets the IP text box
         */
        private void DeviceList_SelectionChanged(object sender, SelectionChangedEventArgs e)
        {
            if (DeviceList.SelectedItem == null)
                return;
            SelectedIpBox.IsReadOnly = true;
            var deviceString = DeviceList.SelectedItem.ToString();
            var index = deviceStringList.FindIndex(array => array[0] == deviceString);
            SelectedIpBox.Text = deviceStringList[index][1];
        }

        /**
         * Function that handles connection to the picar server, if possible and handles various cases
         */
        private void TryConnect(object sender, RoutedEventArgs e)
        {
            //Device list wasn't selected and the manual ip box was left in the default state
            if (DeviceList.SelectedItem == null && SelectedIpBox.Equals("IP Address"))
                return;

            string selectedName;
            var selectedIP = SelectedIpBox.Text;
            if (DeviceList.SelectedItem != null)
            {
                var selectedDevice = DeviceList.SelectedItem.ToString();
                var index = deviceStringList.FindIndex(array => array[0] == selectedDevice);
                if(_mainWindow.DeviceListMn.Items.Cast<PiCarConnection>().Any(item => item.Name == deviceStringList[index][0]))
                    return;

                selectedIP = deviceStringList[index][1];
                selectedName = deviceStringList[index][0];

            }
            else
            {
                var random = new Random();
                var randomNumber = random.Next(1, 256);
                selectedName = "Unknown" + randomNumber;
            }


            //Handle the dummy connection
            if (selectedIP == "DummyIP")
            {
                var dummyConnection = new DummyConnection(selectedName, selectedIP);
                _mainWindow.deviceListMain.Add(dummyConnection);
                _mainWindow.LogField.AppendText(DateTime.Now + ":\t" + "Added " + selectedName + " for testing\n");
                LogFieldReg.AppendText("Added " + selectedName + " for testing\n");
            }

            else if (!CheckIfValidIP(selectedIP))
            {
                LogFieldReg.AppendText("Invalid IP used, try again!\n");
                _mainWindow.LogField.AppendText(DateTime.Now + ":\tInvalid IP used, try again!\n");
            }

            else
            {
                PiCarConnection newConnection = null;
                var canConnect = false;
                try
                {
                    newConnection = new PiCarConnection(selectedName, selectedIP);
                    canConnect = newConnection.RequestConnect();
                }
                catch (RpcException rpcE)
                {
                    _mainWindow.LogField.AppendText(DateTime.Now + ":\tError! " + rpcE + "\n");
                }
                catch(Exception exception)
                {
                    _mainWindow.LogField.AppendText(DateTime.Now + ":\tError! " + exception + "\n");
                }

                if (canConnect)
                {
                    _mainWindow.LogField.AppendText(DateTime.Now + ":\t" + "Connected to " + selectedName + " with IP: " + selectedIP + "\n");
                    LogFieldReg.AppendText("Connected to " + selectedName + " with IP: " + selectedIP + "\n");
                    _mainWindow.deviceListMain.Add(newConnection);
                }
                else
                {
                    _mainWindow.LogField.AppendText(DateTime.Now + ":\t" + "Failed to connect to " + selectedName + " with IP: " + selectedIP + "\n");
                    LogFieldReg.AppendText("Failed to connect to " + selectedName + " with IP: " + selectedIP + "\n");
                }
            }

            _mainWindow.DeviceListMn.ItemsSource = null;
            _mainWindow.DeviceListMn.ItemsSource = _mainWindow.deviceListMain;
            _mainWindow.LogField.ScrollToEnd();
        }

        private static bool CheckIfValidIP(string localIP)
        {
            if (string.IsNullOrWhiteSpace(localIP))
                return false;

            var temp = localIP.Split('.');
            return temp.Length == 4 && temp.All(r => byte.TryParse(r, out var tempForParsing));
        }
    }
}