"""
  Library of EV3 robot functions that are useful in many different applications. For example things
  like arm_up, arm_down, driving around, or doing things with the Pixy camera.

  Add commands as needed to support the features you'd like to implement.  For organizational
  purposes try to only write methods into this library that are NOT specific to one tasks, but
  rather methods that would be useful regardless of the activity.  For example, don't make
  a connection to the remote control that sends the arm up if the ir remote control up button
  is pressed.  That's a specific input --> output task.  Maybe some other task would want to use
  the IR remote up button for something different.  Instead just make a method called arm_up that
  could be called.  That way it's a generic action that could be used in any task.
"""

import ev3dev.ev3 as ev3
import time
import math


class Snatch3r(object):

    def __init__(self):
        self.left_motor = ev3.LargeMotor(ev3.OUTPUT_B)
        self.right_motor = ev3.LargeMotor(ev3.OUTPUT_C)
        assert self.left_motor.connected
        assert self.right_motor.connected
        self.arm_motor = ev3.MediumMotor(ev3.OUTPUT_A)
        assert self.arm_motor.connected
        self.touch_sensor = ev3.TouchSensor()
        assert self.touch_sensor.connected
        self.color_sensor = ev3.ColorSensor()
        assert self.color_sensor
        self.ir_sensor = ev3.InfraredSensor()
        assert self.ir_sensor
        self.pixy = ev3.Sensor(driver_name="pixy-lego")
        assert self.pixy


    def drive_inches(self, distance, speed):
        """make the robot drive a given distane by a given speed, if the
        distance is negative, robot drive backward by the same speed."""
        assert self.left_motor.connected
        assert self.right_motor.connected

        if distance < 0:
            speed = -speed
            distance = distance * 90
        else:
            distance=distance*90
        self.left_motor.run_to_rel_pos(speed_sp=speed, position_sp=distance)
        self.right_motor.run_to_rel_pos(speed_sp=speed,position_sp=distance)
        """.run_to_rel_pos we dont need the stop action"""
        self.left_motor.wait_while(ev3.Motor.STATE_RUNNING)
        self.right_motor.wait_while(ev3.Motor.STATE_RUNNING)
        ev3.Sound.beep().wait()

    def turn_degrees(self, degree, speed):
        """make the robot turn a certain degree at give speed """
        assert self.left_motor.connected
        assert self.right_motor.connected
        self.left_motor.run_to_rel_pos(position_sp=degree*450/90, speed_sp=speed)
        self.right_motor.run_to_rel_pos(position_sp=-degree*450/90, speed_sp=speed)
        self.left_motor.wait_while(ev3.Motor.STATE_RUNNING)
        self.right_motor.wait_while(ev3.Motor.STATE_RUNNING)
        ev3.Sound.beep().wait()

    def stop(self):
        """stop the left and right motor of the robots"""
        assert self.left_motor.connected
        assert self.right_motor.connected
        self.right_motor.stop()
        self.left_motor.stop()

    def arm_calibration(self):
        """calibrate the robot arm """
        assert self.arm_motor.connected
        touch_sensor = ev3.TouchSensor()
        self.arm_motor.run_forever(speed_sp=900)
        while not touch_sensor.is_pressed:
            time.sleep(0.01)
        self.arm_motor.stop(stop_action=ev3.Motor.STOP_ACTION_BRAKE)
        ev3.Sound.beep().wait()
        self.arm_motor.run_to_rel_pos(position_sp=-5112, speed_sp=900)
        self.arm_motor.wait_while(ev3.Motor.STATE_RUNNING)
        ev3.Sound.beep().wait()
        self.arm_motor.position = 0

    def arm_up(self):
        """make the robot's arm going up"""
        assert self.arm_motor.connected
        touch_sensor = ev3.TouchSensor()
        self.arm_motor.run_forever(speed_sp=900)
        while not touch_sensor.is_pressed:
            time.sleep(0.01)
        self.arm_motor.stop(stop_action=ev3.Motor.STOP_ACTION_BRAKE)
        self.arm_motor.wait_while(ev3.Motor.STATE_RUNNING)
        ev3.Sound.beep().wait()

    def arm_down(self):
        """make the robot's arm going down"""
        assert self.arm_motor.connected
        self.arm_motor.run_to_abs_pos(position_sp=0, speed_sp=-900)
        self.arm_motor.wait_while(ev3.Motor.STATE_RUNNING)
        ev3.Sound.beep().wait()

    def shutdown(self):
        """make the robot shutdown when the ev3's backspace bottom is
        pressed. and the two led turn green"""
        btn = ev3.Button()
        while btn.backspace:
            """do we need this while loop here?"""
            self.stop()
            ev3.Leds.set_color(ev3.Leds.RIGHT, ev3.Leds.GREEN)
            ev3.Leds.set_color(ev3.Leds.LEFT, ev3.Leds.GREEN)
            ev3.Sound.speak('goodbye').wait()
            print('Goodbye')

    def go_forward(self, left_motor_speed, right_motor_speed):
        """make the robot run forward forever"""
        assert self.left_motor.connected
        assert self.right_motor.connected
        self.left_motor.run_forever(speed_sp=left_motor_speed)
        self.right_motor.run_forever(speed_sp=right_motor_speed)

    def go_back(self, left_motor_speed, right_motor_speed):
        """maek the robot run backward forever"""
        assert self.left_motor.connected
        assert self.right_motor.connected
        self.left_motor.run_forever(speed_sp=-left_motor_speed)
        self.right_motor.run_forever(speed_sp=-right_motor_speed)

    def turn_right(self, left_motor_speed, right_motor_speed):
        """make the robot turn right forever"""
        assert self.left_motor.connected
        assert self.right_motor.connected
        self.left_motor.run_forever(speed_sp=left_motor_speed)
        self.right_motor.run_forever(speed_sp=-right_motor_speed)

    def turn_left(self, left_motor_speed, right_motor_speed):
        """make the robot turn left forever"""
        assert self.left_motor.connected
        assert self.right_motor.connected
        self.left_motor.run_forever(speed_sp=-left_motor_speed)
        self.right_motor.run_forever(speed_sp=right_motor_speed)

    def  loop_forever(self):
        while True:
            time.sleep(0.01)

    def seek_beacon(self):
        forward_speed = 300
        turn_speed = 100
        beacon_seeker = ev3.BeaconSeeker(channel=1)

        while not self.touch_sensor.is_pressed:
            current_heading = beacon_seeker.heading
            current_distance = beacon_seeker.distance
            if current_distance == -128:
                print("IR Remote not found. Distance is -128")
                self.turn_right(turn_speed, -turn_speed)
            else:

                if math.fabs(current_heading) < 2:
                    if current_distance == 1:
                        self.drive_inches(3, forward_speed)
                        self.stop()
                        print("Found the beacon!")
                        return True
                    print("On the right heading. Distance: ", current_distance)
                    if current_distance > 1:
                        self.go_forward(forward_speed, forward_speed)
                        time.sleep(0.1)
                if 2 < math.fabs(current_heading) < 10:
                    if current_heading < 0:
                        self.turn_left(turn_speed, turn_speed)
                        time.sleep(0.1)
                    if current_heading > 0:
                        self.turn_right(turn_speed, turn_speed)
                        time.sleep(0.1)
                    print("Adjusting heading: ", current_heading)

                if math.fabs(current_heading) > 10:
                    self.turn_right(forward_speed, forward_speed)
                    time.sleep(0.1)
                    print("Heading is too far off to fix: ", current_heading)

            time.sleep(0.2)
        print("Abandon ship!")
        self.stop()
        return False

    def find_beacon(self):
        while True:
            found_beacon = self.seek_beacon()
            if found_beacon:
                self.arm_up()

    def play_music(self):
        ev3.Sound.play("/home/robot/csse120/assets/sounds/L.wav")

    def speak(self, string):
        ev3.Sound.speak(string)

    def dance(self, left_motor_speed, right_motor_speed):
        self.turn_left(left_motor_speed, right_motor_speed)
        self.arm_calibration()





