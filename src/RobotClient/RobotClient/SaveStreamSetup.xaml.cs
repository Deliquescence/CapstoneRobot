using System;
using System.Collections.Generic;
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
    /// Interaction logic for SaveStreamSetup.xaml
    /// </summary>
    public partial class SaveStreamSetup : Window
    {
        private MainWindow _mainWindow = (MainWindow)Application.Current.MainWindow;
        public SaveStreamSetup()
        {
            InitializeComponent();
            DirectoryText.Text = _mainWindow.getPathName();
            SessionText.Text = _mainWindow.getSessionName();
            
            //pressing the enter key starts the saving
            var submit = new RoutedCommand();
            submit.InputGestures.Add(new KeyGesture(Key.Enter));
            CommandBindings.Add(new CommandBinding(submit, StartSaving));
        }
        //after clicking OK the directory name and session prefix will be set for HandleStream() 
        private void StartSaving(object sender, RoutedEventArgs e)
        {
            
            //okButton.IsEnabled = false;
            _mainWindow.setPathName(DirectoryText.Text);
            _mainWindow.setSessionName(SessionText.Text);
            _mainWindow.setSaveEnabled(true);
            this.Close();
            _mainWindow.StreamSavingHeader.IsEnabled = false;
            _mainWindow.StopStreamSavingHeader.IsEnabled = true;
            _mainWindow.LogField.AppendText(DateTime.Now + ":\tStream can now be saved to a file\n");

        }

        private void Window_Closing(object sender, System.ComponentModel.CancelEventArgs e)
        {
            _mainWindow.SaveStreamSetup = null;
        }

        private void DirectoryText_TextChanged(object sender, TextChangedEventArgs e)
        {
            
        }

        private void RadioButton_Checked(object sender, RoutedEventArgs e)
        {

        }

        private void DirectoryText_TextChanged_1(object sender, TextChangedEventArgs e)
        {

        }
    }
}
