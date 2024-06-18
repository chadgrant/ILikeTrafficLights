"""
Second attempt at implementing mode switching but using functions

There is an issue with running two while loops with the simon func
so I need to figure out how to run a global variable to keep track 
of the mode and switch to next mode when mode button pressed.
"""

import random
import board
import digitalio
import neopixel
import keypad
import adafruit_rfm9x
import time
import audiocore
import audiopwmio

# Set up NeoPixel.
pixel = neopixel.NeoPixel(board.NEOPIXEL, 1)
pixel.brightness = 0.5

# Set up SIMON input buttons (USE KEYPAD module instead of direct pullup stuff)
# it debounces and sends as one key press. We set to false b/c pin goes low when pressed
# Set PULL to true b/c we dont have external resistor, so pin held high when not pressed
buttons = {
    'red': keypad.Keys((board.TX,), value_when_pressed=False, pull=True),
    'yellow':keypad.Keys((board.RX,), value_when_pressed=False, pull=True),
    'green' : keypad.Keys((board.D25,), value_when_pressed=False, pull=True),
    'blue' : keypad.Keys((board.D24,), value_when_pressed=False, pull=True),
    'mode' : keypad.Keys((board.D13,), value_when_pressed=False, pull=True)
}

# Setup Sounds
sounds = {
    'meow' : audiocore.WaveFile(open("meow1.wav", "rb")),
    'bark' : audiocore.WaveFile(open("bark1.wav", "rb")),
    'fart' : audiocore.WaveFile(open("fart1.wav", "rb")),
    'blip' : audiocore.WaveFile(open("blip.wav", "rb"))
}

pins = {
    'red' : board.D5,
    'yellow' : board.D6,
    'green' : board.D9,
    'blue' : board.D10
}

pressing = {
    'red' : buttons["red"].events.get(),
    'yellow' : buttons["yellow"].events.get(),
    'green' : buttons["green"].events.get(),
    'blue' : buttons["blue"].events.get(),
}

# Check if the ModeButton is pressed right after initialization
# I don't know why but this ensures it starts in mode 1
# without this it goes to mode 2 immediately? WEIRD
if buttons['mode'].events.get().pressed:
    print("ModeButton is pressed immediately after initialization")

for i in pins:
    pin = digitalio.DigitalInOut(pins[i])
    pin.direction = digitalio.Direction.OUTPUT

audio = audiopwmio.PWMAudioOut(board.A0)

# Define radio frequency in MHz. Must match your
# module. Can be a value like 915.0, 433.0, etc.
RADIO_FREQ_MHZ = 915.0

# Define Chip Select and Reset pins for the radio module.
CS = digitalio.DigitalInOut(board.RFM_CS)
RESET = digitalio.DigitalInOut(board.RFM_RST)

# Initialise RFM95 radio
rfm95 = adafruit_rfm9x.RFM9x(board.SPI(), CS, RESET, RADIO_FREQ_MHZ)

# Define the modes
current_mode = "ControllerMode"

# Define a function for each mode
def ControllerMode():
    # THIS IS STANDARD CONTROLLER MODE
    # Check for button presses. If pressed, send a packet, set NeoPixel Color,
    # turn on the SIMON LED, Play a sound.
    # When released, turn off the NeoPixel and SIMON LED
    RedPress = buttons["red"].events.get()
    YellowPress = buttons["yellow"].events.get()
    GreenPress = buttons["green"].events.get()
    BluePress = buttons["blue"].events.get()

    if RedPress:
        pins["red"].value = RedPress.pressed

        if RedPress.pressed:
            rfm95.send(bytes("R", "UTF-8"))
            pixel.fill((255, 0, 0))
            audio.play(sounds['meow'])
            print("RED!")

        if RedPress.released:
            pixel.fill((0, 0, 0))

    elif YellowPress:
        pins["yellow"].value = RedPress.pressed

        if YellowPress.pressed:
            rfm95.send(bytes("Y", "UTF-8"))
            pixel.fill((255, 245, 0))
            audio.play(sounds['bark'])
            print("YELLOW!")

        if YellowPress.released:
            pixel.fill((0, 0, 0))

    elif GreenPress:
        pins["green"].value = GreenPress.pressed

        if GreenPress.pressed:
            rfm95.send(bytes("G", "UTF-8"))
            pixel.fill((0, 255, 0))
            audio.play(sounds['fart'])
            print("GREEN!")

        if GreenPress.released:
            pixel.fill((0, 0, 0))

    elif BluePress:
        pins["blue"].value = BluePress.pressed

        if BluePress.pressed:
            rfm95.send(bytes("B", "UTF-8"))
            pixel.fill((0, 0, 255))
            audio.play(sounds['blip'])
            print("BLUE!")

        if BluePress.released:
            pixel.fill((0, 0, 0))

def LightsMode():
    # Add functionality for LightsMode
    # THIS IS STANDARD CONTROLLER MODE BUT NO SOUNDS
    # Check for button presses. If pressed, send a packet, set NeoPixel Color,
    # turn on the SIMON LED, Play a sound.
    # When released, turn off the NeoPixel and SIMON LED
    RedPress = buttons["red"].events.get()
    YellowPress = buttons["yellow"].events.get()
    GreenPress = buttons["green"].events.get()
    BluePress = buttons["blue"].events.get()

    if RedPress:
        pins["red"].value = RedPress.pressed

        if RedPress.pressed:
            rfm95.send(bytes("R", "UTF-8"))
            pixel.fill((255, 0, 0))
            pins["red"].value = True
            print("RED!")

        if RedPress.released:
            pixel.fill((0, 0, 0))

    elif YellowPress:
        pins["yellow"].value = YellowPress.pressed

        if YellowPress.pressed:
            rfm95.send(bytes("Y", "UTF-8"))
            pixel.fill((255, 245, 0))
            print("YELLOW!")

        if YellowPress.released:
            pixel.fill((0, 0, 0))

    elif GreenPress:
        pins["green"].value = GreenPress.pressed

        if GreenPress.pressed:
            rfm95.send(bytes("G", "UTF-8"))
            pixel.fill((0, 255, 0))
            print("GREEN!")
        if GreenPress.released:
            pixel.fill((0, 0, 0))

    elif BluePress:
        pins["blue"].value = BluePress.pressed

        if BluePress.pressed:
            rfm95.send(bytes("B", "UTF-8"))
            pixel.fill((0, 0, 255))
            print("BLUE!")

        if BluePress.released:
            pixel.fill((0, 0, 0))

def SoundMode():
    # Add functionality for SoundMode
    # THIS IS STANDARD CONTROLLER MODE BUT NO LIGHTS
    # Check for button presses. If pressed, send a packet, set NeoPixel Color,
    # turn on the SIMON LED, Play a sound.
    # When released, turn off the NeoPixel and SIMON LED

    RedPress = buttons["red"].events.get()
    YellowPress = buttons["yellow"].events.get()
    GreenPress = buttons["green"].events.get()
    BluePress = buttons["blue"].events.get()

    if RedPress:

        if RedPress.pressed:
            rfm95.send(bytes("R", "UTF-8"))
            pixel.fill((255, 0, 0))
            audio.play(sounds['meow'])
            print("RED!")

        if RedPress.released:
            pixel.fill((0, 0, 0))

    elif YellowPress:
        
        if YellowPress.pressed:
            rfm95.send(bytes("Y", "UTF-8"))
            pixel.fill((255, 245, 0))
            audio.play(sounds['bark'])
            print("YELLOW!")

        if YellowPress.released:
            pixel.fill((0, 0, 0))

    elif GreenPress:

        if GreenPress.pressed:
            rfm95.send(bytes("G", "UTF-8"))
            pixel.fill((0, 255, 0))
            audio.play(sounds['fart'])
            print("GREEN!")

        if GreenPress.released:
            pixel.fill((0, 0, 0))

    elif BluePress:

        if BluePress.pressed:
            rfm95.send(bytes("B", "UTF-8"))
            pixel.fill((0, 0, 255))
            audio.play(sounds['blip'])
            print("BLUE!")
        if BluePress.released:
            pixel.fill((0, 0, 0))


def SimonGame():
    # Add functionality for SimonGameMode
    # Initialize the delay time and round counter
    delay_time = 0.5
    round_counter = 0

    while True:  # Outer loop to restart the game
        # Game sequence
        game_sequence = []

        # Game state
        game_over = False

        while not game_over:
            # Add a new color to the sequence at the start of each round
            new_color = random.choice(range(4))
            game_sequence.append(new_color.lower())

            # Play the sequence to the player
            for color in game_sequence:
                pins[color].value = True
                audio.play(sounds[color])
                time.sleep(delay_time)
                pins[color].value = False
                time.sleep(delay_time)

            # Get the player's response ( this hangs until a button is pressed )
            for color in game_sequence:
                button_pressed = False
                while not button_pressed:
                    for _, button in enumerate(buttons):
                        if not button.value:  # Button is pressed (value is False when pressed because of pull-up resistor)
                            button_pressed = True
                            if button != color:  # Player pressed the wrong button
                                game_over = True
                            else:
                                pins[button].value = True  # Light up the LED when the button is pressed
                                audio.play(sounds[i])  # Play the sound when the button is pressed
                                while not button.value:  # Keep the LED lit as long as the button is pressed
                                    pass
                                pins[button].value = False  # Turn off the LED when the button is released
                            break
                if game_over:
                    break

            # Add a delay after the user inputs the correct sequence
            if not game_over:
                time.sleep(1)
                round_counter += 1
                if round_counter % 2 == 0:  # After every 2 rounds
                    delay_time *= 0.8  # Decrease the delay time by 20%

        # Game over, flash all LEDs and play the fart sound
        for _ in range(6):
            for led in pins:
                led.value = True
            time.sleep(0.1)
            for led in pins:
                led.value = False
            time.sleep(0.1)

        audio.play(sounds['fart'])  # Play the fart sound

        # Reset the delay time and round counter for the next game
        delay_time = 0.5
        round_counter = 0

        # Delay before restarting the game
        time.sleep(5)


modes = {
    "ControllerMode": ControllerMode,
    "LightsMode": LightsMode,
    "SoundMode": SoundMode,
    "SimonGame": SimonGame
}

while True:
    # Check if the mode button is pressed
    ModePress = buttons["mode"].events.get()

    if ModePress and ModePress.pressed:
        # Switch to the next mode
        current_mode = (current_mode + 1) % len(modes)
        print(f"Switched to {modes[current_mode]}")

    # Run the function for the current mode
    f = modes[current_mode]
    if f is None:
        print(f"Mode {current_mode} not found")
    else:
        f()