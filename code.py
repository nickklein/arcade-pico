import board
import busio
import time
import digitalio
import adafruit_aw9523

i2c = busio.I2C(board.GP1, board.GP0, frequency=1000000)
aw = adafruit_aw9523.AW9523(i2c)

note_pin = digitalio.DigitalInOut(board.GP6)
note_pin.direction = digitalio.Direction.INPUT
note_pin.pull = digitalio.Pull.UP

led_pin = aw.get_pin(0)
led_pin.direction = digitalio.Direction.OUTPUT

print(note_pin.value)

while True:
    if note_pin.value is False:
        print("pushed")
        led_pin.value = 1
    else:
        led_pin.value = 0
    time.sleep(0.1)
