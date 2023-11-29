#!/usr/bin/env python

import time
import explorerhat

print("""
SD_GIT_2324_U06_template
Software-based binary counter

This code uses a binary counter to count upwards or downwards
Here is a short description:

LEDs:
- The LEDs represent a binary number of four bits

Button 5 toggles the Number Input Mode. When True,
you may enter a binary number by pressing buttons
1 to 4. The corresponding LED indicates whether the
bit is set (LED on) or not (LED off). Pressing a
button again toggles the current mode

Button 6 increases the counter value if not in Number
Input Mode

Button 7 decreases the counter value if not in Number
Input Mode

Button 8 sets the counter to 0 and leaves the Number
Input Mode in case it was activated

Buttons 1 to 4 are only active in Number Input Mode
""")


# binToDec transforms a binary representation
# of a number into a decimal representation
def binToDec(binArray):
    # the leftmost element in the array has index 3, it marks
    # the most significant bit. At four bits, this bit has a
    # weight of 8, the next one of 4 and so forth
    decimal = binArray[3]*2^3 + binArray[2]*2^2 + binArray[1]*2^1 + binArray[0]*2^0
    print("{} as decimal is {}".format(binArray, decimal))
    return decimal
# decTiBin calculates the binary representation
# of a positive decimal number <= 15. The binary
# representation is stored within an array of length 4
# called binArray
def decToBin(decimal):
    print("in Function decToBin")
    if decimal > 15:
        decimal = decimal % 16
        print("Zahl ist zu groß! Kürze zu {}".format(decimal))
    temporaer = decimal
    # the array which will contain the results
    binArray = [0] * 4
    for i in range(4):
        binArray[i] = decimal % 2
        decimal = decimal // 2
    print(f"{temporaer} als Binärzahl ist {binArray[::-1]}")
    # we print and return the resulting binArray
    return binArray


# visualizeBinary represents a binary number of four bits
# by the LEDs 1 to 4 on the Explorer hat.
def visualizeBinary(decimal):
    # note that the leds are internally numbered [0] to [3]
    # the buttons are labeled:
    # buttons:       1    2    3    4
    # internal nr:  [0]  [1]  [2]  [3]
    # but your binary number is numbered that way:
    # binArray =     1    1    0    1   (e.g., number 13)
    #               [3]  [2]  [1]  [0]
    print("in Function visualizeBinary")
    binArray = decToBin(decimal)
    for i in range(4):
        print(i)
        if binArray[i] == 1:
            explorerhat.light[3 - i].on()
            print("Licht {} ist an!".format(4 - i))
# Here we initialize our counter variable
counterInBin = [0] * 4
# short test to set a bit within counterInBin:
# counterInBin[2] = 1

# Here, we convert our binary counter value to a decimal value
counterInDec = binToDec(counterInBin)


# and for test reasons, we may do it backwards and visualize the result
# decToBin(counterInDec)
# visualizeBinary(counterInBin)

# the following to functions increase and decrease
# the global counter value. In an atomic fashion,
# the decimal and the binary representation are
# both changed.
def increaseCounter():
    # since we want to modify a global variable
    # we need to employ the keyword global
    print("in Function increaseCounter")
    global counterInDec
    if counterInDec < 16:
        counterInDec += 1
        print("Die Zahl wurde auf {} erhöht".format(counterInDec))
        visualizeBinary(counterInDec)
    else:
        print("Die maximale Zahl wurde erreicht")
def decreaseCounter():
    # since we want to modify a global variable
    # we need to employ the keyword global
    print("in Function decreaseCounter")
    global counterInDec
    if counterInDec > 0:
        counterInDec -= 1
        print("Die Zahl wurde auf {} verringert".format(counterInDec))
        visualizeBinary(counterInDec)
    else:
        print("Die kleinste Zahl wurde erreicht")


# for test reasons we may invoke increaseCounter()
# as well as decreaseCounter()
# increaseCounter()
# increaseCounter()
# increaseCounter()
# decreaseCounter()
# decreaseCounter()
# decreaseCounter()
# decreaseCounter()
# decreaseCounter()
# decreaseCounter()
# decreaseCounter()

# Here, we define the global variable NumberInputMode
NumberInputMode = False


# This handler reacts to button press events
def evaluateButtons(channel, event):
    global NumberInputMode
    # Toggling Number Input Mode
    if channel == 5 and event == "press":
        NumberInputMode = not NumberInputMode
        print("Number Input Mode is {}".format(NumberInputMode))
    # In case the Number Input Mode is inactive, we may increase or decrease
    # the conuter by buttons 6 or 7, respectively
    if channel == 6 and event == "press" and NumberInputMode == False:
        increaseCounter()
        print("Button press to increase Counter")
    if channel == 7 and event == "press" and NumberInputMode == False:
        decreaseCounter()
        print("Button press to decrease Counter")

    # In case the Number Input Mode is active, channels 1 to 4 are used
    # to modify our global counter variable counterInBin
    # We need to change counterInDec as well
    if channel < 5 and event == "press" and NumberInputMode == True:
        # as for the LEDs, you have to use your brain yet again (ugh...)
        # the buttons are labeled:
        # buttons:       1    2    3    4
        # internal nr:  [0]  [1]  [2]  [3]
        # but your binary number is numbered that way:
        # binArray =     1    1    0    1   (e.g., number 13)
        #              [3]  [2]  [1]  [0]
        # ...
        print("Code to set/unset binary position")
        global counterInDec
        binArray = decToBin(counterInDec)
        for i in range(4):
            if channel == i and event == "press":
                binArray[3 - i] = 1
                visualizeBinary(binToDec(binArray))
                print("Licht {} ist an!".format(i + 1))
    # Press on Button 8 performs a reset
    if channel == 8 and event == "press":
        if NumberInputMode:
            NumberInputMode = not NumberInputMode
        else:
            global counterInDec
            counterInDec = 0
        print("reset")
# In order to invoke the function evaluateButtons() on a button press
# we need to register this function as a handler for button press events
explorerhat.touch.pressed(evaluateButtons)
explorerhat.pause()
