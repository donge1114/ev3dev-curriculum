import tkinter
from tkinter import ttk

import mqtt_remote_method_calls as com


def main():
    mqtt_client = com.MqttClient()
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
    # forward_button and '<Up>' key is done for your here...
    forward_button['command'] = lambda: send_forward(mqtt_client, left_speed_entry, right_speed_entry)
    root.bind('<Up>', lambda event: send_forward(mqtt_client, left_speed_entry, right_speed_entry))

    left_button = ttk.Button(main_frame, text="Left")
    left_button.grid(row=3, column=0)
    # left_button and '<Left>' key
    left_button['command'] = lambda: send_left(mqtt_client, left_speed_entry, right_speed_entry)
    root.bind('<Up>', lambda event: send_left(mqtt_client, left_speed_entry, right_speed_entry))

    stop_button = ttk.Button(main_frame, text="Stop")
    stop_button.grid(row=3, column=1)
    # stop_button and '<space>' key (note, does not need left_speed_entry, right_speed_entry)
    stop_button['command'] = lambda: send_stop(mqtt_client)
    root.bind('<Up>', lambda event: send_stop(mqtt_client))

    right_button = ttk.Button(main_frame, text="Right")
    right_button.grid(row=3, column=2)
    # right_button and '<Right>' key
    right_button['command'] = lambda: send_right(mqtt_client, left_speed_entry, right_speed_entry)
    root.bind('<Up>', lambda event: send_right(mqtt_client, left_speed_entry, right_speed_entry))

    back_button = ttk.Button(main_frame, text="Back")
    back_button.grid(row=4, column=1)
    # back_button and '<Down>' key
    back_button['command'] = lambda: send_back(mqtt_client, left_speed_entry, right_speed_entry)
    root.bind('<Up>', lambda event: send_back(mqtt_client, left_speed_entry, right_speed_entry))

    up_button = ttk.Button(main_frame, text="Up")
    up_button.grid(row=5, column=0)
    up_button['command'] = lambda: send_up(mqtt_client)
    root.bind('<u>', lambda event: send_up(mqtt_client))

    down_button = ttk.Button(main_frame, text="Down")
    down_button.grid(row=6, column=0)
    down_button['command'] = lambda: send_down(mqtt_client)
    root.bind('<j>', lambda event: send_down(mqtt_client))

    # Buttons for quit and exit
    q_button = ttk.Button(main_frame, text="Quit")
    q_button.grid(row=5, column=2)
    q_button['command'] = (lambda: quit_program(mqtt_client, False))

    e_button = ttk.Button(main_frame, text="Exit")
    e_button.grid(row=6, column=2)
    e_button['command'] = (lambda: quit_program(mqtt_client, True))

    speak_label = ttk.Label(main_frame, text="Speak: ")
    speak_label.grid(row=7, column=0, sticky='w')
    string = ttk.Entry(main_frame, width=20)
    string.insert(0, "Hello World")
    string.grid(row=7, column=1, columnspan=2, sticky='w')
    var = tkinter.IntVar()

    r1 = ttk.Radiobutton(main_frame, text="Dance", variable=var, value=1)
    r1.grid(row=8, column=0, sticky='w')
    r1['command'] = (lambda: dance(mqtt_client, left_speed_entry, right_speed_entry))

    r2 = ttk.Radiobutton(main_frame, text="Drive", variable=var, value=2)
    r2.grid(row=9, column=0, sticky='w')
    r2['command'] = (lambda: send_forward(mqtt_client, left_speed_entry, right_speed_entry))

    r3 = ttk.Radiobutton(main_frame, text="Play music", variable=var, value=3)
    r3.grid(row=10, column=0, sticky='w')
    r3['command'] = (lambda: music(mqtt_client))

    r4 = ttk.Radiobutton(main_frame, text="Speak", variable=var, value=4)
    r4.grid(row=11, column=0, sticky='w')
    r4['command'] = (lambda: speak(mqtt_client, string.get()))

    photo = tkinter.PhotoImage(file='FE.gif')
    button1 = ttk.Button(main_frame, image=photo)
    button1['command'] = (lambda: find_beacon(mqtt_client))
    button1.image = photo
    button1.grid(row=0, column=4, rowspan=7)

    root.mainloop()


def send_forward(mqtt_client, left_speed_entry, right_speed_entry):
    print("forward")
    mqtt_client.send_message("go_forward", [int(left_speed_entry.get()), int(right_speed_entry.get())])


def send_back(mqtt_client, left_speed_entry, right_speed_entry):
    print("back")
    mqtt_client.send_message("go_back", [int(left_speed_entry.get()), int(right_speed_entry.get())])


def send_right(mqtt_client, left_speed_entry, right_speed_entry):
    print("right")
    mqtt_client.send_message("turn_right", [int(left_speed_entry.get()), int(right_speed_entry.get())])


def send_left(mqtt_client, left_speed_entry, right_speed_entry):
    print("left")
    mqtt_client.send_message("turn_left", [int(left_speed_entry.get()), int(right_speed_entry.get())])


def send_stop(mqtt_client):
    print("stop")
    mqtt_client.send_message("stop")


def send_up(mqtt_client):
    print("arm_up")
    mqtt_client.send_message("arm_up")


def send_down(mqtt_client):
    print("arm_down")
    mqtt_client.send_message("arm_down")


# Quit and Exit button callbacks
def quit_program(mqtt_client, shutdown_ev3):
    if shutdown_ev3:
        print("shutdown")
        mqtt_client.send_message("shutdown")
    mqtt_client.close()
    exit()


def find_beacon(mqtt_client):
    print("seek_beacon")
    mqtt_client.send_message("find_beacon")


def music(mqtt_client):
    print("Play music")
    mqtt_client.send_message("play_music")


def speak(mqtt_client, string):
    print("Speak")
    mqtt_client.send_message("speak", [string])


def dance(mqtt_client, left_speed_entry, right_speed_entry):
    print("Dance")
    mqtt_client.send_message("dance", [int(left_speed_entry.get()), int(right_speed_entry.get())])


main()