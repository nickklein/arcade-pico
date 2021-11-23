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
    # init variables
    buttons = []
    leds = []
    midiNotes = []
    midiList = {0: [0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15], 1: [16,17,18,19,20,21,22,23,24,25,26,27,28,29,30,31,31]}
    armedButton = None
    # init pins
    buttonPins = [board.GP6, board.GP7]
    armedButtonPin = board.GP11
    ledPins = [1,2]

    def init(self):
        self.assignMidiNotes(0)
        self.initButtons()
        self.initArmedButton()
        self.initLEDs()
        self.loop()

    def assignMidiNotes(self, buttonPosition):
        self.midiNotes = self.midiList[buttonPosition]

    def initButtons(self):
        # init buttons and save them to global buttons
        for buttonPin in self.buttonPins:
            pin = digitalio.DigitalInOut(buttonPin)
            pin.direction = digitalio.Direction.INPUT
            pin.pull = digitalio.Pull.UP
            self.buttons.append(pin)

    def initArmedButton(self):
        pin = digitalio.DigitalInOut(self.armedButtonPin)
        pin.direction = digitalio.Direction.INPUT
        pin.pull = digitalio.Pull.UP
        self.armedButton = pin

    def initLEDs(self):
        i2c = busio.I2C(board.GP1, board.GP0, frequency=1000000)
        aw = adafruit_aw9523.AW9523(i2c)
        for ledPin in self.ledPins:
            led_pin = aw.get_pin(ledPin)
            led_pin.direction = digitalio.Direction.OUTPUT
            self.leds.append(led_pin)

    # Main Loop that makes the whole thing work
    def loop(self):
        # initilize midi channel
        midi = adafruit_midi.MIDI(midi_out=usb_midi.ports[1], out_channel=0)
        # Get the amount of buttons
        pinCounts = len(self.buttonPins)
        while True:
            isArmed = self.armedButtonListener(pinCounts)
            # Only run midiListener if armedButton is off
            if isArmed is False:
                self.midiListener(midi, pinCounts)
            time.sleep(0.1)

    # Listen to the armed button
    # Armed Button allows the user to change the midi notes
    def armedButtonListener(self, pinCounts):
        # If button is pushed
        if self.armedButton.value is False:
            return self.armedButtonEvent(pinCounts)
        else:
            return False

    # Execute armed event
    def armedButtonEvent(self, pinCounts):
        self.turnOnArcadeLights(pinCounts)
        while True:
            for buttonKey in range(pinCounts):
                # If button is pushed then light up LED, and send midi
                if self.buttons[buttonKey].value is False:
                    self.assignMidiNotes(buttonKey)
                    self.turnOffArcadeLights(pinCounts)
                    time.sleep(1)
                    return False

    # Turn on arcade button lights
    def turnOnArcadeLights(self, pinCounts):
        for key in range(pinCounts):
            self.leds[key].value = True

    # Turn off arcade button lights
    def turnOffArcadeLights(self, pinCounts):
        for key in range(pinCounts):
            self.leds[key].value = False

    def midiListener(self, midi, pinCounts):
        # Loop through length of buttonPins
        for key in range(pinCounts):
            # If button is pushed then light up LED, and send midi
            if self.buttons[key].value is False:
                print("PUSHED")
                midi.send(NoteOn(self.midiNotes[key], 120))
                self.leds[key].value = True
            else:
                midi.send(NoteOff(self.midiNotes[key], 120))
                self.leds[key].value = False

midiFighter = MidiFighter()
midiFighter.init()