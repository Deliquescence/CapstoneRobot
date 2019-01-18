import picarserver
from time import sleep

server = picarserver.getServer()
server.start()
print('Server started')
sleep(60*60*24)