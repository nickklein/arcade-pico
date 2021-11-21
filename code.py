import board
import busio
import time
import digitalio
import adafruit_aw9523
import usb_midi
import adafruit_midi
from adafruit_midi.note_on import NoteOn
from adafruit_midi.note_off import NoteOff


class MidiFighter:
    buttonAmount = 2
    buttons = []
    leds = []
    buttonPins = [board.GP6, board.GP7]
    ledPins = [1,2]
    midiNotes = [60,61,62,63,64,65,66,67,68,69,70,71,72,73,74,75]
    
    def init(self):
        self.initButtons()
        self.initLEDs()
        self.loop()
    
    def initButtons(self):
        for buttonPin in self.buttonPins:
            note_pin = digitalio.DigitalInOut(buttonPin)
            note_pin.direction = digitalio.Direction.INPUT
            note_pin.pull = digitalio.Pull.UP
            self.buttons.append(note_pin)
    def initLEDs(self):
        i2c = busio.I2C(board.GP1, board.GP0, frequency=1000000)
        aw = adafruit_aw9523.AW9523(i2c)
        for ledPin in self.ledPins:
            led_pin = aw.get_pin(ledPin)
            led_pin.direction = digitalio.Direction.OUTPUT
            self.leds.append(led_pin)
    def loop(self):
        midi = adafruit_midi.MIDI(midi_out=usb_midi.ports[1], out_channel=0)
        while True:
            for key in range(self.buttonAmount):
                if self.buttons[key].value is False:
                    print("PUSHED")
                    midi.send(NoteOn(self.midiNotes[key], 120))
                    self.leds[key].value = True
                else:
                    midi.send(NoteOff(self.midiNotes[key], 120))
                    self.leds[key].value = False
            time.sleep(0.1)
    
midiFighter = MidiFighter()
midiFighter.init()
