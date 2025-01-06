import serial
import uinput
import vgamepad

serial_port = "/dev/ttyUSB0"
baud_rate = 115200
ser = serial.Serial(serial_port, baud_rate, timeout=1)

DS4_AXES = {
    "steering" : uinput.ABS_X,
    "accelerator" : uinput.ABS_RZ,
    "brake" : uinput.ABS_Z
}

gamepad = vgamepad.VDS4Gamepad()

def scale_value(value):
    return int(1023 - (value / 1023) * 255)

try:
    while True:
        if ser.in_waiting > 0:
            raw_data = ser.readline().decode('utf-8').strip()
            values = raw_data.split(',')

            if len(values) >= 5:
                try:
                    steering_value = int(values[2])
                    accel_value = int(values[3])
                    break_value = int(values[4])

                    print(values)

                    gamepad.right_trigger(scale_value(break_value))
                    gamepad.left_joystick(scale_value(steering_value), 128)

                    #gamepad.right_trigger(scale_value(brake_value))
                    if accel_value < 120:
                        print("pressed")
                        gamepad.press_button(vgamepad.DS4_BUTTONS.DS4_BUTTON_CIRCLE)
                    else:
                        gamepad.release_button(vgamepad.DS4_BUTTONS.DS4_BUTTON_CIRCLE)

                    gamepad.update()

                except ValueError:
                    print("Non-numeric data received:", raw_data)

except KeyboardInterrupt:
    print("Exiting...")
finally:
    ser.close()