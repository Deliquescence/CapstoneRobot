This is a continuation of previous semester work in which Students build a robotic vehicle system that implemented a leader / follower concept. The vehicle controls and a rudimentary algorithm was developed to follow leader vehicle. Our goal of the project is to extend the algorithm and make follower vehicle more robust vehicles. The project should consider incorporating one or more of the following:

1. A system in place to handle the situation where the “following” vehicle(s) lose line of sight.
2. Any vehicle in the system can be the lead vehicle.
3. A system in place to handle obstructions in the “following” vehicle(s) path that do not cause loss of line of sight but could still interrupt vehicle operations.

4. Vehicles communicate directly with one another, sharing navigational data

Minimum Requirements:

1. At least two robotic vehicles (one to lead and one to follow)
2. Vehicles must not collide with each other


Installing dependencies on picar:
git clone --recursive -b python3 https://github.com/sunfounder/SunFounder_PiCar.git
cd SunFounder_PiCar
sudo su
./install_dependencies
exit

Clone the repo continaing this README onto the picar.
cd CapstoneRobot/src/Setup
./setup.bash
./misc.sh
cd ../..

The server is started by (from project root):
python3 picar_driver.py
