from view import *
from controller import *


controller=Controller()
view=View(controller)

exit=False

while not exit:
    exit=view.get_events()
