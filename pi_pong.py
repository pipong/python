# Pi-Pong Scoring
# Follow the README.md file before running

print("Running Pi-Pong Scoring...")

# Library setup
import RPi.GPIO as GPIO
from Tkinter import *
import tkFont

# Time before score button can be pressed again (in milleseconds)
delayTime = 500

# White team GPIO input pin
whitegpio = 18

# Blue team GPIO input pin
bluegpio = 4

# Scores
blueScore = 0
whiteScore = 0

# Create window for application
window = Tk()

# Set font
labelFont = tkFont.Font(family= 'Arial', size=300, weight='bold')
exitFont = tkFont.Font(family= 'Arial', size=20)

# Set window parameters
window.title("Pi-Pong")
w, h = window.winfo_screenwidth(), window.winfo_screenheight()
window.overrideredirect(1)
window.geometry("%dx%d+0+0" % (w, h))
window.configure(bg='black')

# Exit button
def endProgram():
    window.destroy()
exitButton = Button(window, text="Exit", command = endProgram, font=exitFont, borderwidth=0, fg='white', bg='black', highlightthickness=0)
exitButton.pack()
exitButton.place(relx=1.0, rely=0.0, anchor=NE)

# Blue Team Score Label
blueLabel = Label(window, text="0", font=labelFont, fg='blue', bg='black')
blueLabel.pack()
blueLabel.place(relx=0.25, rely=0.50, anchor=CENTER)

# White Team Score Label
whiteLabel = Label(window, text="0", font=labelFont, fg='white', bg='black')
whiteLabel.pack()
whiteLabel.place(relx=0.75, rely=0.50, anchor=CENTER)

# GPIO pin setup
GPIO.setmode(GPIO.BCM)
GPIO.setup(bluegpio, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(whitegpio, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

# Callback statements
def blue_score(channel):
    global blueScore
    global whiteScore
    blueScore = blueScore + 1
    blueLabel["text"] = blueScore
    blueLabel.place(relx=0.25, rely=0.50, anchor=CENTER)
    if blueScore >= 11:
        if (blueScore - whiteScore) >= 2:
            blueScore = 0
            whiteScore = 0
    whiteLabel["text"] = whiteScore
    blueLabel["text"] = blueScore
    whiteLabel.place(relx=0.75, rely=0.50, anchor=CENTER)
    blueLabel.place(relx=0.25, rely=0.50, anchor=CENTER)

def white_score(channel):
    global whiteScore
    global blueScore
    whiteScore = whiteScore + 1
    if whiteScore >= 11:
        if (whiteScore - blueScore) >= 2:
            blueScore = 0
            whiteScore = 0
    whiteLabel["text"] = whiteScore
    blueLabel["text"] = blueScore
    whiteLabel.place(relx=0.75, rely=0.50, anchor=CENTER)
    blueLabel.place(relx=0.25, rely=0.50, anchor=CENTER)


# GPIO event detection
GPIO.add_event_detect(bluegpio, GPIO.FALLING, callback=blue_score, bouncetime=delayTime)
GPIO.add_event_detect(whitegpio, GPIO.FALLING, callback=white_score, bouncetime=delayTime)

# Begins mainloop
mainloop()
