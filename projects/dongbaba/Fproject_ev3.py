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
    stop(robot, ev3.ColorSensor.COLOR_YELLOW)
    robot.loop_forever()


def stop(robot, color):
    color_sensor = ev3.ColorSensor()
    white_level = 30
    black_level = 10
    while True:
        current_color = color_sensor.color
        time.sleep(0.01)
        if current_color == color:
            robot.stop()
            ev3.Sound.speak('Auto start').wait()
            robot.drive_inches(-1, 300)
            while not robot.color_sensor.color == ev3.ColorSensor.COLOR_RED:
                print(robot.color_sensor.reflected_light_intensity)
                if robot.color_sensor.reflected_light_intensity < white_level:
                    robot.go_back(300, 300)
                else:
                    robot.turn_right(30, 250)
            robot.stop()
            ev3.Sound.speak('Finish')
        elif robot.touch_sensor.is_pressed:
            ev3.Sound.speak('Start to go').wait()
            while not robot.color_sensor.color == ev3.ColorSensor.COLOR_WHITE:
                robot.go_forward(300, 300)
            robot.stop()



# ----------------------------------------------------------------------
# Calls  main  to start the ball rolling.
# ----------------------------------------------------------------------
main()
