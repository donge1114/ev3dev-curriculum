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
import math
import time

left_motor = ev3.LargeMotor(ev3.OUTPUT_B)
right_motor = ev3.LargeMotor(ev3.OUTPUT_C)

class Snatch3r(object):
    """Commands for the Snatch3r robot that might be useful in many different programs."""

    def __init__(self):
        self.x = 0

    def drive_inches(self, speed, time):
        left_motor.run_forever(speed_sp=speed)
        right_motor.run_forever(speed_sp=speed)
        t = time / (0.012 * speed)
        time.sleep(t)
        left_motor.stop()
        right_motor.stop(stop_action="brake")

    def turn_degrees(self, degrees_to_turn, turn_speed_sp):
        left_motor.run_to_rel_pos(speed_sp=turn_speed_sp, position_sp=-degrees_to_turn, stop_action=ev3.Motor.STOP_ACTION_BRAKE)
        right_motor.run_to_rel_pos(speed_sp=turn_speed_sp, position_sp=degrees_to_turn, stop_action=ev3.Motor.STOP_ACTION_BRAKE)

        left_motor.run_to_rel_pos.wait_while(ev3.Motor.STATE_RUNNING)
        right_motor.run_to_rel_pos.wait_while(ev3.Motor.STATE_RUNNING)