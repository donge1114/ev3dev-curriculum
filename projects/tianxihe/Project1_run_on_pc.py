import tkinter
from tkinter import ttk
import mqtt_remote_method_calls as com
import ev3dev.ev3 as ev3
import robot_controller as robo



def main():
    robot = robo.Snatch3r()

    """making my user input window"""
    mqtt_client=com.MqttClient()
    mqtt_client.connect_to_ev3()

    root = tkinter.Tk()
    root.title("MQTT Remote")

    main_frame = ttk.Frame(root, padding=20, relief='raised')
    main_frame.grid()

    left_speed_label = ttk.Label(main_frame, text="Left")
    left_speed_label.grid(row=0, column=0)
    left_speed_entry = ttk.Entry(main_frame, width=8)
    left_speed_entry.insert(0, "600")
    left_speed_entry.grid(row=1, column=0)

    right_speed_label = ttk.Label(main_frame, text="Right")
    right_speed_label.grid(row=0, column=2)
    right_speed_entry = ttk.Entry(main_frame, width=8, justify=tkinter.RIGHT)
    right_speed_entry.insert(0, "600")
    right_speed_entry.grid(row=1, column=2)

    forward_button = ttk.Button(main_frame, text="Forward")
    forward_button.grid(row=2, column=1)
    forward_button['command'] = lambda: send_forward(mqtt_client,
                                                     int(
                                                         left_speed_entry.get()),
                                          int(right_speed_entry.get()))

    root.bind('<Up>', lambda event:send_forward(mqtt_client,
                                   int(left_speed_entry.get()),
                                     int(right_speed_entry.get())))

    left_button = ttk.Button(main_frame, text="Left")
    left_button.grid(row=3, column=0)
    left_button['command']= lambda: send_left(mqtt_client,
                                              int(left_speed_entry.get()),
                                              int(right_speed_entry.get()))
    root.bind("<Left>",lambda event: send_left(mqtt_client,
                                               int(left_speed_entry.get()),
                                               int(right_speed_entry.get())))

    stop_button = ttk.Button(main_frame, text="Stop")
    stop_button.grid(row=3, column=1)
    stop_button["command"]=lambda:send_stop(mqtt_client)
    root.bind("<space>",lambda event:send_stop(mqtt_client))


    right_button = ttk.Button(main_frame, text="Right")
    right_button.grid(row=3, column=2)
    right_button['command']=lambda: send_right(mqtt_client,
                                                int(left_speed_entry.get()),
                                               int(right_speed_entry.get()))
    root.bind("<Right>",lambda event: send_right(mqtt_client,
                                                left_speed_entry.get(),
                                               int(right_speed_entry.get())))

    back_button = ttk.Button(main_frame, text="Back")
    back_button.grid(row=4, column=1)
    back_button["command"]=lambda: send_back(mqtt_client,
                                             int(left_speed_entry.get()),
                                              int(right_speed_entry.get()))
    root.bind("<Down>",lambda event: send_back(mqtt_client,
                                             int(left_speed_entry.get()),
                                             int(right_speed_entry.get())))

    up_button = ttk.Button(main_frame, text="Up")
    up_button.grid(row=5, column=0)
    up_button['command'] = lambda: send_up(mqtt_client)
    root.bind('<u>', lambda event: send_up(mqtt_client))

    down_button = ttk.Button(main_frame, text="Down")
    down_button.grid(row=6, column=0)
    down_button['command'] = lambda: send_down(mqtt_client)
    root.bind('<j>', lambda event: send_down(mqtt_client))

    q_button = ttk.Button(main_frame, text="Quit")
    q_button.grid(row=5, column=2)
    q_button['command'] = lambda: quit_program(mqtt_client, False)

    e_button = ttk.Button(main_frame, text="Exit")
    e_button.grid(row=6, column=2)
    e_button['command'] = lambda: quit_program(mqtt_client, True)

    tank1_button=ttk.Button(main_frame, text="Tank1")
    tank1_button.grid(row=7,column=0)
    tank1_button['command']=lambda : tank1_finder(mqtt_client,
                                                  int(left_speed_entry.get(

                                                  )),
                                                  int(
                                                      right_speed_entry.get()))
    return_button = ttk.Button(main_frame, text="Return")
    return_button.grid(row=7, column=2)
    return_button['command']=lambda :return_fun(mqtt_client,
                                                int(left_speed_entry.get(),
                                                    int(right_speed_entry.get())))
    tank2_button = ttk.Button(main_frame, text="Tank2")
    tank2_button.grid(row=7, column=0)
    tank2_button['command'] = lambda: tank1_finder(mqtt_client,
                                                   int(left_speed_entry.get(

                                                   )),
                                                   int(
                                                       right_speed_entry.get()))


    root.mainloop()

    def return_fun(mqtt_client,left_speed,right_speed):
        print("Return to the base")
        mqtt_client.send_message("drive_inches",[3,left_speed])
        while not robot.color_sensor.color==ev3.ColorSensor.COLOR_BLUE:
            if robot.color_sensor.reflected_light_intensity < 95:
                mqtt_client.send_message("go_forward",[left_speed,right_speed])
            else:
                mqtt_client.send_message("turn_right",[left_speed,
                                                       right_speed])
        robot.stop()
        mqtt_client.send_message("turn_degree", [180, left_speed])
        print(" Done ")

    def send_up(mqtt_client):
        print("arm_up")
        mqtt_client.send_message("arm_up")

    def send_down(mqtt_client):
        print("arm_down")
        mqtt_client.send_message("arm_down")

    def send_forward(mqtt_client, left_speed_entry, right_speed_entry):
        print("forward")
        mqtt_client.send_message("go_forward",
                                 [left_speed_entry, right_speed_entry])

    def send_left(mqtt_client, left, right):
        print("left")
        mqtt_client.send_message("turn_left", [left, right])

    def send_stop(mqtt_client):
        print("stop")
        mqtt_client.send_message("stop")

    def send_right(mqtt_client, left, right):
        print("right")
        mqtt_client.send_message("turn_right", [left, right])

    def send_back(mqtt_client, left, right):
        print("back")
        mqtt_client.send_message("go_back", [left, right])

    def quit_program(mqtt_client, shutdown_ev3):
        if shutdown_ev3:
            print("Value checking robot is shutdown")
            mqtt_client.send_message("shutdown")
        mqtt_client.close()
        exit()

    def tank1_finder(mqtt_client,left_speed,right_speed):
        print("Checking Tank1 Volume")
        mqtt_client.send_message("drive_inches", [3, left_speed])
        while not robot.color_sensor.color==ev3.ColorSensor.COLOR_BLUE:
            if robot.color_sensor.reflected_light_intensity < 95:
                mqtt_client.send_message("go_forward",[left_speed,right_speed])
            else:
                mqtt_client.send_message("turn_right",[left_speed,
                                                       right_speed])
        robot.stop()
        mqtt_client.send_message("drive_inches",[1,left_speed])
        volume_tank1=robot.color_sensor.reflected_light_intensity
        mqtt_client.send_message("turn_degree", [180, left_speed])
        print("the volume of chemical inside the Tank1 is".format(volume_tank1))
        print("Done")


main()