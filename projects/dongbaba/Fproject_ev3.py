import mqtt_remote_method_calls as com
import robot_controller as robo
import ev3dev.ev3 as ev3
import time

COLOR_NAMES = ["None", "Black", "Blue", "Green", "Yellow", "Red", "White", "Brown"]

class DataContainer(object):

    def __init__(self):
        self.running = True

def main():
    robot = robo.Snatch3r()
    mqtt_client = com.MqttClient(robot)
    mqtt_client.connect_to_pc()
    dc = DataContainer()
    btn = ev3.Button()
    btn.on_up = handle_up_button
    btn.on_backspace = lambda state: handle_shutdown(state, dc)
    while dc.running:
        btn.process()
        time.sleep(0.01)
    print("Goodbye!")
    ev3.Sound.speak("Goodbye").wait()


    robot.loop_forever()

def handle_up_button(button_state):
    if button_state:
        print("Up button is pressed")
        ev3.Sound.speak("Autonomous control begin")

def handle_shutdown(button_state, dc):
    if button_state:
        print("back")
        dc.running = False


# ----------------------------------------------------------------------
# Calls  main  to start the ball rolling.
# ----------------------------------------------------------------------
main()
