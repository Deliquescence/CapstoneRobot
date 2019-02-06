using System;
using System.Collections.Generic;
using System.ComponentModel;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using System.Windows;
using System.Windows.Controls;
using System.Windows.Data;
using System.Windows.Documents;
using System.Windows.Input;
using System.Windows.Media;
using System.Windows.Media.Imaging;
using System.Windows.Shapes;

namespace RobotClient
{
    /// <summary>
    /// Interaction logic for MirroringMode.xaml
    /// </summary>
    public partial class MirroringMode : Window
    {
        private PiCarConnection leaderPicar;
        private PiCarConnection followerPicar;
        private Replay leaderReplay;
        private Replay followerReplay;
        private readonly MainWindow _mainWindow = (MainWindow)Application.Current.MainWindow;
        public MirroringMode()
        {
            InitializeComponent();
        }

        private void SetLeader(object sender, RoutedEventArgs e)
        {
            //Get the picar from the device List
            leaderPicar = (PiCarConnection) _mainWindow.DeviceListMn.SelectedItem;
            if (leaderPicar == null) return;
            SetVehicleMode(ModeRequest.Types.Mode.Lead);
        }
        //follower must be set as leader for the backend
        private void SetAsLeader(object sender, RoutedEventArgs e)
        {
            //Get the picar from the device List
            followerPicar = (PiCarConnection)_mainWindow.DeviceListMn.SelectedItem;
            if (followerPicar == null) return;
            SetVehicleMode(ModeRequest.Types.Mode.Lead);
        }

        private void SetVehicleMode(ModeRequest.Types.Mode mode)
        {
            var picar = (PiCarConnection)_mainWindow.DeviceListMn.SelectedItem;
            try
            {
                picar.SetMode(mode);
                _mainWindow.DeviceStatus.Text = picar.Mode.ToString();
                _mainWindow.LogField.AppendText(DateTime.Now + ":\tSetting " + picar + "to " + picar.Mode.ToString() + "\n");
                _mainWindow.LogField.ScrollToEnd();
            }
            catch (Exception e)
            {
                DisconnectCar();
                Console.WriteLine(e);
            }
        }

        private void DisconnectCar()
        {
            var picar = (PiCarConnection)_mainWindow.DeviceListMn.SelectedItem;
            if (picar.GetType() == typeof(DummyConnection))
                return;

            _mainWindow.LogField.AppendText(DateTime.Now + ":\tVehicle stopped responding, disconnecting. \n");
            _mainWindow.LogField.ScrollToEnd();
            _mainWindow.deviceListMain.Remove(picar);
            _mainWindow.DeviceListMn.ItemsSource = null;
            _mainWindow.DeviceListMn.ItemsSource = _mainWindow.deviceListMain;
        }
        //starts the replays for mirroring mode
        private void StartMirroring_Click(object sender, RoutedEventArgs e)
        {
            var inputs = Direction.ParseLog(_mainWindow.LogField.Text);

            //Replay.StartTwoWithCatchup((PiCarConnection)_mainWindow.DeviceListMn.Items[0], (PiCarConnection)_mainWindow.DeviceListMn.Items[1], inputs, 1.0);
            Replay.StartTwoWithCatchup(leaderPicar, followerPicar, inputs, Convert.ToDouble(CatchDistance.Text));
            
            //leaderReplay = Replay.StartTwoWithCatchup(leaderPicar, followerPicar, inputs, Convert.ToDouble(CatchDistance.Text)).Item1;
            //followerReplay = Replay.StartTwoWithCatchup(leaderPicar, followerPicar, inputs, Convert.ToDouble(CatchDistance.Text)).Item2;
        }

        private void StopMirroring_Click(object sender, RoutedEventArgs e)
        {
            //leaderReplay.Stop();
            //followerReplay.Stop();
            
        }

        private void Window_Closing(object sender, CancelEventArgs e)
        {
            _mainWindow.Mirror = null;
        }
    }
}
