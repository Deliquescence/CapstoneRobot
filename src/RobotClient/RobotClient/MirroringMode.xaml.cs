using System;
using System.Collections.Generic;
using System.ComponentModel;
using System.Linq;
using System.Text;
using System.Threading;
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
        private PiCarConnection Picar;
        private Replay replay;
        private readonly MainWindow _mainWindow = (MainWindow)Application.Current.MainWindow;
        public MirroringMode(PiCarConnection picar)
        {
            Picar = picar;
            InitializeComponent();
        }

        //starts the replays for mirroring mode
        private void StartMirroring_Click(object sender, RoutedEventArgs e)
        {
            //Leader mode for backend
            SetVehicleMode(ModeRequest.Types.Mode.Lead);
            //sets mirroring true for this picar
            Picar.SetMirroring(true);
            //creates new replay after a given delay
            var inputs = Direction.ParseLog(_mainWindow.LogField.Text);
            _mainWindow.LogField.Clear(); //Clear after load
            replay = new Replay(Picar, inputs, Convert.ToInt32(Delay.Text) * 1000);
            replay.Start();
        }

        private void StopMirroring_Click(object sender, RoutedEventArgs e)
        {
            Picar.SetMirroring(false);
            replay.Stop();
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


    }
}
