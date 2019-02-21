
sudo rm /usr/local/lib/python2.7/dist-packages/SunFounder_PiCar-1.0.1-py2.7.egg/picar/config
sudo rm /usr/local/lib/python3.5/dist-packages/SunFounder_PiCar-1.0.1-py3.5.egg/picar/config
sudo rm /usr/local/lib/python3.6/site-packages/SunFounder_PiCar-1.0.1-py3.6.egg/picar/config
rm ~/CapstoneRobot/src/RobotServer/config

sudo ln ~/SunFounder_PiCar/picar/config /usr/local/lib/python2.7/dist-packages/SunFounder_PiCar-1.0.1-py2.7.egg/picar/config
sudo ln ~/SunFounder_PiCar/picar/config /usr/local/lib/python3.5/dist-packages/SunFounder_PiCar-1.0.1-py3.5.egg/picar/config
sudo ln ~/SunFounder_PiCar/picar/config /usr/local/lib/python3.6/site-packages/SunFounder_PiCar-1.0.1-py3.6.egg/picar/config
ln ~/SunFounder_PiCar/picar/config ~/CapstoneRobot/src/RobotServer/config

vim ~/SunFounder_PiCar/picar/config
