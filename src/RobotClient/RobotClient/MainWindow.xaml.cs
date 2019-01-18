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

namespace RobotClient
{
    public partial class MainWindow
    {
        public Window Register;
        public List<PiCarConnection> deviceListMain = new List<PiCarConnection>();
        public string LeaderIp { set; get; }
        public string FollowerIP { set; get; }

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

        /**
         * Method that runs when the main window launches
         */
        public MainWindow()
        {
            InitializeComponent();

            //Setup sync context
            synchronizationContext = SynchronizationContext.Current;
            
            LeaderIp = "Empty";
            Title = "Welcome " + Environment.UserName;

            //Adds shortcut to open the registration window with Ctrl + R
            var newKeybind = new RoutedCommand();
            newKeybind.InputGestures.Add(new KeyGesture(Key.R, ModifierKeys.Control));
            CommandBindings.Add(new CommandBinding(newKeybind, Register_Click));

            _controlMode = true;

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
                _timer = new DispatcherTimer { Interval = TimeSpan.FromSeconds(1/30) };
                _timer.Tick += _timer_Tick;
                _timer.Start();
                _directionController = 0.0;
                _throttleController = 0.0;
            }
        }

        /**
         * Image update method to update video stream image asynchronously
         */
        public void UpdateStream(ImageSource image)
		{
			try
			{
				synchronizationContext.Post(o =>
				{
				    StreamImage.Source = (ImageSource)o;
				}, image);
			}
			
			catch(Exception e)
			{
				Console.WriteLine("Error " + e);
                var picar = (PiCarConnection)DeviceListMn.SelectedItem;
                if (picar == null)
                    return;
                DisconnectCar();
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
            catch(IOException exception)
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
                var dlg = new Microsoft.Win32.OpenFileDialog
                {
                    DefaultExt = ".txt"
                };
                var result = dlg.ShowDialog();
                if (result != true) return;
                LogField.Text = File.ReadAllText(dlg.FileName);
            }
            catch(IOException exception)
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
                    ? 0: 
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

            string[] throttleStrings = { "Moving backwards", "In Neutral", "Moving forwards" };
            string[] directionStrings = { "and left", "", "and right" };
            int temp1 = 1;
            int temp2 = 1;
            if (_throttleController > 0)
            {
                temp1 = (int)Math.Ceiling(_throttleController) + 1;
            }
            else if (_throttleController < 0)
            {
                temp1 = (int)Math.Floor(_throttleController) + 1;
            }

            if (_directionController > 0)
            {
                temp2 = (int)Math.Ceiling(_directionController) + 1;
            }
            else if (_directionController < 0)
            {
                temp2 = (int)Math.Floor(_directionController) + 1;
            }

            LogField.AppendText(DateTime.Now + ":\t" + throttleStrings[temp1] + " " +
                                directionStrings[temp2] + "\n");
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

            LogField.AppendText(DateTime.Now + ":\t" + throttleStrings[(int)throttleMotor + 1] + " " +
                                directionStrings[(int)directionMotor + 1] + "\n");
 
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

            string[] throttleStrings = { "Now Moving backwards", "Now In Neutral", "Now Moving forwards" };
            string[] directionString = { "and left", "", "and right" };

            if (Keyboard.IsKeyUp(Key.W) && Keyboard.IsKeyUp(Key.Up)) throttleMotor--;

            if (Keyboard.IsKeyUp(Key.S) && Keyboard.IsKeyUp(Key.Down)) throttleMotor++;

            if (Keyboard.IsKeyUp(Key.A) && Keyboard.IsKeyUp(Key.Left)) directionMotor++;

            if (Keyboard.IsKeyUp(Key.D) && Keyboard.IsKeyUp(Key.Right)) directionMotor--;

            LogField.AppendText(DateTime.Now + ":\t" + throttleStrings[(int)throttleMotor + 1] + " " +
                                directionString[(int)directionMotor + 1] + "\n");
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
                UpdateStream(null);
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
                    UpdateStream(null);
                    temp.StopStream();
                    MoveVehicle(0.0, 0.0);
                    SetVehicleMode(ModeRequest.Types.Mode.Idle);
                }
                catch(Exception exception)
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
                    UpdateStream(null);
                    oldPicar.StopStream();

                }
            }
            catch(Exception exception)
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
                if (picar.Mode == ModeRequest.Types.Mode.Lead)
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
    }
}
