import picar_server
from time import sleep

server = picar_server.getServer()
server.start()
print('Server started')
sleep(60*60*24)
