import board
import busio
import time
import digitalio
import adafruit_aw9523
import usb_midi
import adafruit_midi
from adafruit_midi.note_on import NoteOn
from adafruit_midi.note_off import NoteOff

buttons = []
leds = []
i2c = busio.I2C(board.GP1, board.GP0, frequency=1000000)
aw = adafruit_aw9523.AW9523(i2c)
#  MIDI setup as MIDI out device
midi = adafruit_midi.MIDI(midi_out=usb_midi.ports[1], out_channel=0)

## Declare pins
buttonPins = [board.GP6, board.GP7]
ledPins = [1,2]
midiNotes = [60,61,62,63,64,65,66,67,68,69,70,71,72,73,74,75]


for buttonPin in buttonPins:
    note_pin = digitalio.DigitalInOut(buttonPin)
    note_pin.direction = digitalio.Direction.INPUT
    note_pin.pull = digitalio.Pull.UP
    buttons.append(note_pin)

for ledPin in ledPins:
    led_pin = aw.get_pin(ledPin)
    led_pin.direction = digitalio.Direction.OUTPUT
    leds.append(led_pin)

while True:
    for key in range(2):
        if buttons[key].value is False:
            print("PUSHED")
            midi.send(NoteOn(midiNotes[key], 120))
            leds[key].value = True
        else:
            #print("NOT PUSHED")
            midi.send(NoteOff(midiNotes[key], 120))
            leds[key].value = False

    time.sleep(0.1)
