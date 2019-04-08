using System;
using System.Collections.Generic;
using System.Windows;
using System.Windows.Controls;
using System.Windows.Controls.Primitives;
using System.Windows.Input;
using System.ComponentModel;
using System.Runtime.CompilerServices;
using System.Windows.Threading;
using SharpDX.XInput;
using System.IO;
using System.Threading;
using System.Windows.Media;
using Grpc.Core;
using System.Threading.Tasks;
using System.Linq;
using System.Collections;

namespace RobotClient
{
    public partial class MainWindow
    {
        public Window Register;
        public Window SaveStreamSetup;
        public Window Mirror;
        public List<PiCarConnection> deviceListMain = new List<PiCarConnection>();

        private readonly SynchronizationContext synchronizationContext;
        private DispatcherTimer _timer;

        private string _leftAxis;
        private string _rightAxis;
        private string _buttons;
        private readonly Controller _controller;
        private const int DeadzoneValue = 2500;
        private double _directionController;
        private double _throttleController;
        private Gamepad _previousState;

        //true is the default simulator style mode, false is RC mode
        private bool _controlMode;
        //true if stream saving is enabled
        private bool _saveStreamEnabled;

        // Number of image stream frames saved
        private int saved_frame_count = 0;

        private string pathName;
        private string sessionName;
        /**
         * Method that runs when the main window launches
         */
        public MainWindow()
        {
            InitializeComponent();

            //Setup sync context
            synchronizationContext = SynchronizationContext.Current;

            Title = "Welcome " + Environment.UserName;

            //Adds shortcut to open the registration window with Ctrl + R
            var newKeybind = new RoutedCommand();
            newKeybind.InputGestures.Add(new KeyGesture(Key.R, ModifierKeys.Control));
            CommandBindings.Add(new CommandBinding(newKeybind, Register_Click));

            _controlMode = true;

            _saveStreamEnabled = false;

            //Adds shortut Ctrl + S for stream saving and Ctrl + D for disabling stream saving
            var streamKeybind = new RoutedCommand();
            streamKeybind.InputGestures.Add(new KeyGesture(Key.S, ModifierKeys.Control));
            CommandBindings.Add(new CommandBinding(streamKeybind, ImageSaving_Click));

            var dStreamKeybind = new RoutedCommand();
            dStreamKeybind.InputGestures.Add(new KeyGesture(Key.D, ModifierKeys.Control));
            CommandBindings.Add(new CommandBinding(dStreamKeybind, StopSaving_Click));

            
            
            //Checks if a controller is plugged into the current OS
            _controller = new Controller(UserIndex.One);
            if (!_controller.IsConnected)
            {
                LogField.AppendText(DateTime.Now + ":\tNo controller found!\n");
            }
            else
            {
                //Uses a timer to loop a method that checks the status of the controller
                LogField.AppendText(DateTime.Now + ":\tController detected!\n");
                _timer = new DispatcherTimer { Interval = TimeSpan.FromSeconds(1 / 30) };
                _timer.Tick += _timer_Tick;
                _timer.Start();
                _directionController = 0.0;
                _throttleController = 0.0;
            }
            //sets initial connection configuration specified by .ini file
            initializeUI();
        }

        //sets up initia configuration for connection and log using specified .ini file
        private async void initializeUI()
        {
            ArrayList carInfoArray = new ArrayList();

            var file_path = $"{Environment.GetFolderPath(Environment.SpecialFolder.MyDocuments)}\\picar\\gui_config.ini";
            if (!File.Exists(file_path)) {
                return;
            }

            //gets text from specified .ini file
            try {
                string[] lines = File.ReadAllLines(file_path);

                string selectedIP;
                string selectedName;
                string[] ipNameAndMode;
                
                string mode;
                string path;
                string session;

                string[] path_and_session;
                for (int i = 0; i < lines.Length; i++)
                {
                    if (lines[i] == "(*connect)")
                    {
                        while (lines[i + 1] != "(connect*)")
                        {
                            ipNameAndMode = lines[i + 1].Split(',');
                            selectedIP = ipNameAndMode[0];
                            selectedName = ipNameAndMode[1];
                            mode = ipNameAndMode[2];
                            carInfoArray.Add(ipNameAndMode);
                            await IPConnect(selectedIP, selectedName);
                            i = i + 1;
                        }
                    }
                    
                    if (lines[i] == "(*stream)")
                    {
                        while (lines[i + 1] != "(stream*)")
                        {
                            path_and_session = lines[i + 1].Split(',');
                            path = path_and_session[0];
                            session = path_and_session[1];
                            setPathName(path);
                            setSessionName(session);
                            i = i + 1;
                        }
                    }

                    if (lines[i] == "(*log)")
                    {
                        while (lines[i + 1] != "(log*)")
                        {
                            LogField.AppendText(lines[i + 1] + "\n");
                            i = i + 1;
                        }
                    }
                }
            }
            catch (Exception e)
            {
                LogField.AppendText($"{DateTime.Now}:\tError when initializing configuration: {e.Message}\n");
            }
            DeviceListMn.ItemsSource = null;
            DeviceListMn.ItemsSource = deviceListMain;

            //initializes mode for each connection in .ini
            foreach (string[] m in carInfoArray)
            {
                initializeMode(m[1], m[2]);
            }
        }

        //automatically sets mode of cars based on .ini file
        private void initializeMode(string name, string mode)
        {
            foreach(PiCarConnection car in deviceListMain)
            {
                if(name == car.Name)
                {
                    if(mode=="lead")
                    {
                        SetVehicleMode(car, ModeRequest.Types.Mode.Lead);
                    }
                    if(mode == "follow")
                    {
                        SetVehicleMode(car, ModeRequest.Types.Mode.Follow);
                    }
                    if (mode == "idle")
                    {
                        SetVehicleMode(car, ModeRequest.Types.Mode.Idle);
                    }
                }
            }
        }

        //tries to connect to cars specified in .ini file
        private async Task IPConnect(string selectedIP, string selectedName)
        {

            //Handle the dummy connection
            if (selectedIP == "DummyIP")
            {
                var dummyConnection = new DummyConnection(selectedName, selectedIP);
                deviceListMain.Add(dummyConnection);
                LogField.AppendText(DateTime.Now + ":\t" + "Added " + selectedName + " for testing\n");
                //LogFieldReg.AppendText("Added " + selectedName + " for testing\n");
            }

            else if (!CheckIfValidIP(selectedIP))
            {
                //LogFieldReg.AppendText("Invalid IP used, try again!\n");
                LogField.AppendText(DateTime.Now + ":\tInvalid IP used, try again!\n");
            }

            else
            {
                PiCarConnection newConnection = null;
                var canConnect = false;
                try
                {
                    newConnection = new PiCarConnection(selectedName, selectedIP);
                    var connectResponse = newConnection.RequestConnect();
                    Console.Write(connectResponse.Item2);
                    //LogFieldReg.AppendText(connectResponse.Item2);
                    LogField.AppendText(DateTime.Now + ":\t" + connectResponse.Item2);
                    canConnect = connectResponse.Item1;
                }
                catch (RpcException rpcE)
                {
                    LogField.AppendText(DateTime.Now + ":\tRPC error: " + rpcE.Message + "\n");
                }
                catch (Exception exception)
                {
                    LogField.AppendText(DateTime.Now + ":\tError! " + exception + "\n");
                }

                if (canConnect)
                {
                    LogField.AppendText(DateTime.Now + ":\t" + "Connected to " + selectedName + " with IP: " + selectedIP + "\n");
                    //LogFieldReg.AppendText("Connected to " + selectedName + " with IP: " + selectedIP + "\n");
                    deviceListMain.Add(newConnection);
                }
                else
                {
                    LogField.AppendText(DateTime.Now + ":\t" + "Failed to connect to " + selectedName + " with IP: " + selectedIP + "\n");
                    //LogFieldReg.AppendText("Failed to connect to " + selectedName + " with IP: " + selectedIP + "\n");
                }
            }
        }

        private static bool CheckIfValidIP(string localIP)
        {
            if (string.IsNullOrWhiteSpace(localIP))
                return false;

            var temp = localIP.Split('.');
            return temp.Length == 4 && temp.All(r => byte.TryParse(r, out var tempForParsing));
        }

        //methods for getting and setting directory name, 
        //session prefix and ability to save to disk for stream saving
        public void setPathName(string Pname)
        {
            pathName = Pname;
        }

        public void setSessionName(string Sname)
        {
            sessionName = Sname;
        }

        public void setSaveEnabled(bool b)
        {
            _saveStreamEnabled = b;
            if (b)
            {
                writeStreamCsvHeader();
            }
        }

        public string getPathName()
        {
            return pathName;
        }

        public string getSessionName()
        {
            return sessionName;
        }

        public bool getSaveEnabled()
        {
            return _saveStreamEnabled;
        }


        /**
         * Update method which gets called by PiCarConnection when sending image frames and car actions.
         */
        public void HandleStream(byte[] imageBytes, SetMotion action)
        {
            if (imageBytes == null) { return; }

            var save_dir_path = getPathName();
            var session_prefix = getSessionName();
            bool save_to_disk = getSaveEnabled();

            //Convert bytes to ImageSource type for GUI
            var imgSource = (ImageSource)new ImageSourceConverter().ConvertFrom(imageBytes);

            // Update the GUI
            try
            {
                synchronizationContext.Post(o => StreamImage.Source = (ImageSource)o, imgSource);
            }
            catch (Exception e)
            {
                LogField.AppendText($"{DateTime.Now}: Error updating the GUI with image received from car: {e}\n");
                var picar = (PiCarConnection)DeviceListMn.SelectedItem;
                if (picar == null)
                    return;
                DisconnectCar();
            }

            if (save_to_disk)
            {
                try
                {
                    var csv_path = $"{save_dir_path}\\{session_prefix}.csv";
                    var image_file_name = $"{session_prefix}_{saved_frame_count.ToString("D5")}.jpg";

                    saved_frame_count += 1;
                    using (var fileStream = new FileStream($"{save_dir_path}\\train\\{image_file_name}", FileMode.Create))
                    {
                        //Console.WriteLine($"Writing image of length {imageBytes.Length}");
                        fileStream.Write(imageBytes, 0, imageBytes.Length);
                        fileStream.Flush();
                    }

                    using (var streamWriter = new StreamWriter(csv_path, true))
                    {
                        streamWriter.WriteLineAsync($"train/{image_file_name},{action.Throttle},{action.Direction}");
                    }
                }
                catch (IOException e)
                {
                    LogField.AppendText($"{DateTime.Now}:\tError writing stream data to disk: {e.Message}\n");
                }
            }

        }

        public void writeStreamCsvHeader()
        {
            var save_dir_path = getPathName();
            var session_prefix = getSessionName();
            var csv_path = $"{save_dir_path}\\{session_prefix}.csv";

            if (!File.Exists(csv_path)) {
                try {

                    using ( var streamWriter = new StreamWriter(csv_path, true) ) {
                        streamWriter.WriteLineAsync($"image_file,throttle,direction");
                    }
                }
                catch ( IOException e ) {
                    LogField.AppendText($"{DateTime.Now}:\tError opening csv: {e.Message}\n");
                }
            }
        }

        /**
         * Clear the image that was displayed by the stream
         */
        public void clearStreamImage()
        {
            try
            {
                synchronizationContext.Post(o => StreamImage.Source = (ImageSource)o, null);
            }
            catch (Exception e)
            {
                LogField.AppendText($"{DateTime.Now}:\tError clearing stream image: {e}\n");
            }
        }

        /**
         * Timer method that calls the method that checks the controller status
         */
        private void _timer_Tick(object sender, EventArgs e)
        {
            try
            {
                ControllerMovement();
            }
            catch (Exception exception)
            {
                Console.WriteLine(exception);
                LogField.AppendText(DateTime.Now + ":\tController disconnected\n");
                _timer.Stop();
            }

        }

        private void ModeChanger_Click(object sender, RoutedEventArgs e)
        {
            if (_controlMode)
            {
                _controlMode = false;
                DefaultHeader.IsEnabled = true;
                AlternativeHeader.IsEnabled = false;
                LogField.AppendText(DateTime.Now + ":\tUsing RC control mode\n");
            }
            else
            {
                _controlMode = true;
                DefaultHeader.IsEnabled = false;
                AlternativeHeader.IsEnabled = true;
                LogField.AppendText(DateTime.Now + ":\tUsing simulator control mode\n");
            }
            LogField.ScrollToEnd();
        }
        //opens up window for user to specify directory they want to save file to
        //and allows them to specify the session prefix name
        private void ImageSaving_Click(object sender, RoutedEventArgs e)
        {
            if (SaveStreamSetup == null)
            {
                SaveStreamSetup = new SaveStreamSetup();
                SaveStreamSetup.Show();
            }
            else if (SaveStreamSetup != null)
            {
                SaveStreamSetup.Focus();
            }

            LogField.ScrollToEnd();
        }
        //stops the stream from being saved
        private void StopSaving_Click(object sender, RoutedEventArgs e)
        {
            StreamSavingHeader.IsEnabled = true;
            StopStreamSavingHeader.IsEnabled = false;
            if (_saveStreamEnabled == true)
            {
                LogField.AppendText(DateTime.Now + ":\tStream will no longer be saved to a file\n");
                LogField.ScrollToEnd();
            }
            _saveStreamEnabled = false;
        }

        /**
         * Method that opens the registration window
         */
        private void Register_Click(object sender, RoutedEventArgs e)
        {
            if (Register == null)
            {
                Register = new Registration();
                Register.Show();
            }
            else
            {
                Register.Focus();
            }
        }

        //opens up window that sets up mirroring mode





        /**
         * Method that handles exporting data written to the log, and outputs a text file with timestamps
         */
        private void ExportLog_Click(object sender, RoutedEventArgs e)
        {
            try
            {
                //TODO Make the Log Export to the Application Path and Work a Time Stamp into Log Export's file Name
                var documentsLocation = Environment.GetFolderPath(Environment.SpecialFolder.MyDocuments);
                var filename = "Log " + DateTime.Now.ToString("dddd, dd MMMM yyyy") + ".txt";
                File.WriteAllText(Path.Combine(documentsLocation, filename), LogField.Text);
            }
            catch (IOException exception)
            {
                MessageBox.Show("Problem exporting log data " + exception.ToString(), "Error!");
            }
        }

        /**
         * Method that handles importing data written from a locally saved log file, and outputs it into the current log field.
         */
        private void ImportData_Click(object sender, RoutedEventArgs e)
        {
            try
            {
                var fileName = Environment.GetFolderPath(Environment.SpecialFolder.MyDocuments);
                fileName += "\\robotlog.txt";

                LogField.Text = File.ReadAllText(fileName);
                var res = Direction.ParseLog(LogField.Text);
            }
            catch (IOException exception)
            {
                MessageBox.Show("Problem importing log data " + exception.ToString(), "Error!");
            }

        }

        /**
         * Method that handles the simulator style input for variable speed and direction
         */
        private void ControllerMovement()
        {
            //var picar = (PiCarConnection)DeviceListMn.SelectedItem;
            //if (picar == null || picar.Mode != ModeRequest.Types.Mode.Lead) return;
            var state = _controller.GetState().Gamepad;
            //Default control settings (Simulator Mode)
            if (_controlMode)
            {
                if (state.LeftThumbX.Equals(_previousState.LeftThumbX) &&
                    state.LeftTrigger.Equals(_previousState.LeftTrigger) &&
                    state.RightTrigger.Equals(_previousState.RightTrigger))
                    return;


                //_Motor1 produces either -1.0 for left or 1.0 for right motion
                _directionController = Math.Abs((double)state.LeftThumbX) < DeadzoneValue
                    ? 0 :
                    (double)state.LeftThumbX / short.MinValue * -1;
                _directionController = Math.Round(_directionController, 3);

                /**
                 * These variables produce either 1.0 for forward motion, or -1 for backwards.
                 * If the values are both non-zero, then there will be no motion in either direction
                 */
                var forwardSpeed = Math.Round(state.RightTrigger / 255.0, 3);
                var backwardSpeed = Math.Round(state.LeftTrigger / 255.0 * -1.0, 3);

                if (forwardSpeed > 0 && backwardSpeed == 0)
                    _throttleController = forwardSpeed;
                else if (backwardSpeed < 0 && forwardSpeed == 0)
                    _throttleController = backwardSpeed;
                else
                    _throttleController = 0.0;
            }

            //Alternative control settings (RC Mode)
            else
            {
                if (state.LeftThumbY.Equals(_previousState.LeftThumbY) &&
                    state.RightThumbX.Equals(_previousState.RightThumbX))
                    return;

                _directionController = Math.Abs((double)state.RightThumbX) < DeadzoneValue
                    ? 0
                    : (double)state.RightThumbX / short.MinValue * -1;
                _directionController = Math.Round(_directionController, 3);

                _throttleController = Math.Abs((double)state.LeftThumbY) < DeadzoneValue
                    ? 0
                    : (double)state.LeftThumbY / short.MinValue * -1;

            }

            string output = Direction.EncodeDirection(DateTime.Now, _throttleController, _directionController);

            LogField.AppendText(output);
            LogField.ScrollToEnd();
            MoveVehicle(_throttleController, _directionController);
            _previousState = state;
        }

        /**
         * Method that handles when one or more key is pressed down (Vehicle is moving in one or more directions)
         */
        private void Key_down(object sender, KeyEventArgs e)
        {
            //var picar = (PiCarConnection)DeviceListMn.SelectedItem;
            //if (picar == null || picar.Mode != ModeRequest.Types.Mode.Lead) return;
            if (e.IsRepeat) return;

            var directionMotor = 0.0;
            var throttleMotor = 0.0;

            string[] throttleStrings = { "Moving backwards", "In Neutral", "Moving forwards" };
            string[] directionStrings = { "and left", "", "and right" };


            if (Keyboard.IsKeyDown(Key.W) || Keyboard.IsKeyDown(Key.Up)) throttleMotor++;

            if (Keyboard.IsKeyDown(Key.S) || Keyboard.IsKeyDown(Key.Down)) throttleMotor--;

            if (Keyboard.IsKeyDown(Key.A) || Keyboard.IsKeyDown(Key.Left)) directionMotor--;

            if (Keyboard.IsKeyDown(Key.D) || Keyboard.IsKeyDown(Key.Right)) directionMotor++;

            string output = Direction.EncodeDirection(DateTime.Now, throttleMotor, directionMotor);
            LogField.AppendText(output);
            MoveVehicle(throttleMotor, directionMotor);
            LogField.ScrollToEnd();
        }

        /**
         * Method that handles when one or more key is released (Vehicle is stopping in one or more directions)
         */
        private void Key_up(object sender, KeyEventArgs e)
        {
            //var picar = (PiCarConnection)DeviceListMn.SelectedItem;
            //if (picar == null || picar.Mode != ModeRequest.Types.Mode.Lead) return;

            var directionMotor = 0.0;
            var throttleMotor = 0.0;

            if (Keyboard.IsKeyUp(Key.W) && Keyboard.IsKeyUp(Key.Up)) throttleMotor--;

            if (Keyboard.IsKeyUp(Key.S) && Keyboard.IsKeyUp(Key.Down)) throttleMotor++;

            if (Keyboard.IsKeyUp(Key.A) && Keyboard.IsKeyUp(Key.Left)) directionMotor++;

            if (Keyboard.IsKeyUp(Key.D) && Keyboard.IsKeyUp(Key.Right)) directionMotor--;

            string output = Direction.EncodeDirection(DateTime.Now, throttleMotor, directionMotor);

            LogField.AppendText(output);
            MoveVehicle(throttleMotor, directionMotor);
            LogField.ScrollToEnd();
        }

        /**
         * Method that handles when the GUI buttons are held down (Vehicle is moving a single direction)
         */
        private void ButtonPress_Event(object sender, RoutedEventArgs e)
        {
            //TODO add button up event for stop command
            //var picar = (PiCarConnection)DeviceListMn.SelectedItem;
            //if (picar == null || picar.Mode != ModeRequest.Types.Mode.Lead) return;
            var button = (RepeatButton)sender;
            switch (button.Name)
            {
                case "Forward":
                    LogField.AppendText(DateTime.Now + ":\tMoving forward\n");
                    MoveVehicle(1.0, 0.0);
                    break;

                case "Backwards":
                    LogField.AppendText(DateTime.Now + ":\tMoving backwards\n");
                    MoveVehicle(-1.0, 0.0);
                    break;

                case "Left":
                    LogField.AppendText(DateTime.Now + ":\tMoving left\n");
                    MoveVehicle(0.0, -1.0);
                    break;

                case "Right":
                    LogField.AppendText(DateTime.Now + ":\tMoving right\n");
                    MoveVehicle(0.0, 1.0);
                    break;

                default:
                    Console.WriteLine("Mistakes were made");
                    break;
            }
            LogField.ScrollToEnd();
        }

        /**
         *  Method that handles when the GUI button is released (Vehicle is stopped)
         */
        private void ButtonPress_Released(object sender, RoutedEventArgs e)
        {
            //var picar = (PiCarConnection)DeviceListMn.SelectedItem;
            //if (picar == null || picar.Mode != ModeRequest.Types.Mode.Lead) return;
            LogField.AppendText(DateTime.Now + ":\tNow In Neutral\n");
            MoveVehicle(0.0, 0.0);
            LogField.ScrollToEnd();
        }

        private async void StreamToggle_Checked(object sender, RoutedEventArgs e)
        {
            var picar = (PiCarConnection)DeviceListMn.SelectedItem;
            if (picar == null) return;
            try
            {
                var streamTask = picar.StartStream();
                await streamTask;
            }
            catch (Exception exception)
            {
                DisconnectCar();
                Console.WriteLine(exception);
            }
        }

        private void StreamToggle_Unchecked(object sender, RoutedEventArgs e)
        {
            var picar = (PiCarConnection)DeviceListMn.SelectedItem;
            if (picar == null) return;
            try
            {
                clearStreamImage();
                picar.StopStream();
            }
            catch (Exception exception)
            {
                DisconnectCar();
                Console.WriteLine(exception);
            }
        }

        /**
         * Method that opens a message box with 'About' information
         */
        private void About_Click(object sender, RoutedEventArgs e)
        {
            //TODO rewrite for tutorial information/team
            MessageBox.Show(
                "Created by Team Robot Follower, of Capstone Project Class 4999 of Fall 2018 \nThe Team consists of:\nEric Ramocki and Sean Ramocki on Desktop Application Developer\nAlex Alwardt and Scott Dudley on Network/Desktop Application Developer \nChristian Nickolaou and Anton Cantoldo on Vehicle Application/Systems Developer",
                "About");
        }

        /**
         * Method that handles shutdown confirmation
         */
        private void Shutdown_Click(object sender, RoutedEventArgs e)
        {
            if (MessageBox.Show("Do you want to close this program", "Confirmation", MessageBoxButton.YesNo,
                    MessageBoxImage.Question) == MessageBoxResult.Yes)
            {

                Application.Current.Shutdown();
            }
        }

        /**
         * Method that handles shutdown confirmation
         */
        private void Window_Closing(object sender, CancelEventArgs e)
        {

            foreach (var t in DeviceListMn.Items)
            {
                try
                {
                    if (!(t is PiCarConnection temp) || temp.Mode != ModeRequest.Types.Mode.Lead) continue;
                    LogField.AppendText(DateTime.Now + ":\t" + temp.Name + " is stopping");
                    clearStreamImage();
                    temp.StopStream();
                    MoveVehicle(0.0, 0.0);
                    SetVehicleMode(ModeRequest.Types.Mode.Idle);
                }
                catch (Exception exception)
                {
                    LogField.AppendText(DateTime.Now + ":\tSomething went wrong: " + exception.ToString());
                }
            }

            Application.Current.Shutdown();
        }

        /**
         *
         */
        private void DeviceList_SelectionChanged(object sender, SelectionChangedEventArgs e)
        {
            try
            {
                //Stop the stream of the previously selected event
                foreach (PiCarConnection oldPicar in e.RemovedItems)
                {
                    oldPicar.StopStream();
                    clearStreamImage();
                }
            }
            catch (Exception exception)
            {
                //TODO Remove vehicles that throw exceptions
                LogField.AppendText(DateTime.Now + ":\tException found when removing an old streams!\n" + e + "\n");
                //TODO remove previous car
                Console.WriteLine(exception);
            }
            //Get the picar from the device List
            var picar = (PiCarConnection)DeviceListMn.SelectedItem;
            if (picar == null) return;

            StreamToggle.IsEnabled = true;
            StreamToggle.IsChecked = false;


            //Update ipBox and deviceStatus with it's info
            IpBox.Text = picar.ipAddress.ToString();
            DeviceStatus.Text = picar.Mode.ToString();
        }

        /**
         *
         */
        private void SetLeader(object sender, RoutedEventArgs e)
        {
            //Get the picar from the device List
            var picar = (PiCarConnection)DeviceListMn.SelectedItem;
            if (picar == null) return;
            SetVehicleMode(ModeRequest.Types.Mode.Lead);
        }

        /**
         *
         */
        private void SetFollower(object sender, RoutedEventArgs e)
        {
            //Get the picar from the device List
            var picar = (PiCarConnection)DeviceListMn.SelectedItem;
            if (picar == null) return;
            SetVehicleMode(ModeRequest.Types.Mode.Follow);
        }

        /**
         *
         */
        private void SetDefault(object sender, RoutedEventArgs e)
        {
            //Get the picar from the device List
            var picar = (PiCarConnection)DeviceListMn.SelectedItem;
            if (picar == null) return;
            SetVehicleMode(ModeRequest.Types.Mode.Idle);
        }

        private void MoveVehicle(double speed, double direction)
        {
            foreach (var picar in deviceListMain)
            {
                if (picar.Mode == ModeRequest.Types.Mode.Lead && !picar.isMirroring())
                {
                    try
                    {
                        picar.SetMotion(speed, direction);
                    }
                    catch (Exception e)
                    {
                        DisconnectCar();
                        Console.WriteLine(e);
                    }
                }
            }
        }

        private void SetVehicleMode(ModeRequest.Types.Mode mode)
        {
            var picar = (PiCarConnection)DeviceListMn.SelectedItem;
            SetVehicleMode(picar, mode);
        }

        private void SetVehicleMode(PiCarConnection picar, ModeRequest.Types.Mode mode)
        {
            try
            {
                picar.SetMode(mode);
                DeviceStatus.Text = picar.Mode.ToString();
                LogField.AppendText(DateTime.Now + ":\tSetting " + picar + "to " + picar.Mode.ToString() + "\n");
                LogField.ScrollToEnd();
            }
            catch (Exception e)
            {
                DisconnectCar();
                Console.WriteLine(e);
            }
        }

        private void DisconnectCar()
        {
            var picar = (PiCarConnection)DeviceListMn.SelectedItem;
            if (picar.GetType() == typeof(DummyConnection))
                return;

            LogField.AppendText(DateTime.Now + ":\tVehicle stopped responding, disconnecting. \n");
            LogField.ScrollToEnd();
            deviceListMain.Remove(picar);
            DeviceListMn.ItemsSource = null;
            DeviceListMn.ItemsSource = deviceListMain;
        }

        #region Properties

        public string LeftAxis
        {
            get => _leftAxis;
            set
            {
                if (value == _leftAxis) return;
                _leftAxis = value;
                OnPropertyChanged();
            }
        }

        public string RightAxis
        {
            get => _rightAxis;
            set
            {
                if (value == _rightAxis) return;
                _rightAxis = value;
                OnPropertyChanged();
            }
        }

        public string Buttons
        {
            get => _buttons;
            set
            {
                if (value == _buttons) return;
                _buttons = value;
                OnPropertyChanged();
            }
        }

        public event PropertyChangedEventHandler PropertyChanged;

        protected virtual void OnPropertyChanged([CallerMemberName] string propertyName = null)
        {
            var handler = PropertyChanged;
            if (handler != null) handler(this, new PropertyChangedEventArgs(propertyName));
        }

        #endregion

        private void SetMirror(object sender, RoutedEventArgs e)
        {
            var car = (PiCarConnection)DeviceListMn.SelectedItem;
            if (car == null) return;
            Mirror = new MirroringMode(car);
            Mirror.Show();
        }
    }
}
