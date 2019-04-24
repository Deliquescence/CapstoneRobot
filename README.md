
# Leader-Follower Car Project

## About

This is a continuation of [previous semester work](https://github.com/sramocki/SeniorProjectRobot) in which Students build a robotic vehicle system that implemented a leader / follower concept.
The vehicle controls and a rudimentary algorithm was developed to follow leader vehicle.
Our goal of the project is to extend the algorithm and make follower vehicle more robust vehicles.
The project should consider incorporating one or more of the following:

1. A system in place to handle the situation where the “following” vehicle(s) lose line of sight.
2. Any vehicle in the system can be the lead vehicle.
3. A system in place to handle obstructions in the “following” vehicle(s) path that do not cause loss of line of sight but could still interrupt vehicle operations.
4. Vehicles communicate directly with one another, sharing navigational data

Minimum Requirements:

1. At least two robotic vehicles (one to lead and one to follow)
2. Vehicles must not collide with each other


## Running

After the system is installed (see below), the system is operated by running `picar_driver.py` on both cars and starting the client on the windows machine.

```bash
cd ~/CapstoneRobot/src/RobotServer
python3 picar_driver.py
```

At this point the GUI can connect to the car and issue commands.


## Required Hardware

It is assumed that two [SunFounder PiCar-V](https://www.sunfounder.com/smart-video-car-kit-v2-0.html) have been assembled with Raspberry Pi model 3B+.

A windows computer (preferably laptop) is required to run the client controller.


## Client Installation

.NET framework 4.6.1 is required to run the client.

See the most recent release on GitHub for a complied version.
All that is required is to run `RobotClient.exe`.

To build manually, it is a matter of installing Visual Studio and opening the solution file in `src/RobotClient`.


## Server Installation

It is assumed that Raspbian has been installed.

Install python 3.5 and OpenCV:
```bash
sudo apt-get install python3.5 python-opencv
```

Install SunFounder dependency (python 3 version) onto the picar:
```bash
git clone --recursive -b python3 https://github.com/sunfounder/SunFounder_PiCar.git
cd SunFounder_PiCar
sudo su
./install_dependencies
exit
```

Clone this repo onto the picar:
```bash
git clone --recursive https://github.com/Deliquescence/CapstoneRobot.git
```

Change to setup directory:
`cd CapstoneRobot/src/Setup`

Utilize install scripts:
```./misc.sh```
```./install-grpc.sh```
```./install-smbus.sh```
```./install-git-lfs.sh```

## Useful Resources

[Sutton and Barto, Reinforcement learning: An Introduction](http://incompleteideas.net/book/RLbook2018.pdf)

[SunFounder PiCar Manual](https://www.sunfounder.com/learn/download/X1BWQ19SYXNwYmVycnlfUGlfU21hcnRfVmlkZW9fQ2FyX1YyLjAucGRm/dispi)

[OpenCV Aruco Documentation](https://docs.opencv.org/3.1.0/d5/dae/tutorial_aruco_detection.html)
