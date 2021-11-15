from view import *
from controller import *


control=Controller()
view=View(control)

exit=False

while not exit:
    exit=view.get_events()
