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
    dc = DataContainer()
    white_level = 95
    black_level = 5
    mqtt_client = com.MqttClient(robot)
    mqtt_client.connect_to_pc()
    robot.loop_forever()
    while True:
        if stop(robot, ev3.ColorSensor.COLOR_YELLOW) is True:
            print("Auto start")
            auto(robot, white_level, black_level)
        if robot.ir_sensor.proximity == 4:
            print('Start to go')
            while not stop(robot, ev3.ColorSensor.COLOR_BLUE) is True:
                robot.go_forward(300, 300)


def auto(robot, white_level, black_level):
    while not stop(robot, ev3.ColorSensor.COLOR_RED) is True:
        if robot.color_sensor.reflected_light_intensity < white_level:
            robot.go_back(300, 300)
        else:
            robot.turn_right(100, 100)


def stop(robot, color):
    color_sensor = ev3.ColorSensor()
    while True:
        current_color = color_sensor.color
        time.sleep(0.01)
        if current_color == color:
            robot.stop()
            break
    robot.stop()
# ----------------------------------------------------------------------
# Calls  main  to start the ball rolling.
# ----------------------------------------------------------------------
main()
