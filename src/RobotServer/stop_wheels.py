from picar import back_wheels
import picar

picar.setup()
bw = back_wheels.Back_Wheels()
picar.setup()
bw.speed = 0

def main():
	bw.stop()

if __name__ == '__main__':
	main()

