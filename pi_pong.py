# Pi-Pong Scoring
# Follow the README.md file before running

print("Running Pi-Pong Scoring...")

# Library setup
import RPi.GPIO as GPIO
from Tkinter import *
import tkFont

# Time before score button can be pressed again (in milleseconds)
delayTime = 500

# White and blue team GPIO pin assignments (Raspberry Pi B+)
whitegpio = 18
bluegpio = 4

# Color Assignments
whiteColor = "#F2F2F2"
blueColor = "#0067A0"

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
# Sets the window to be fullscreen
w, h = window.winfo_screenwidth(), window.winfo_screenheight()
window.overrideredirect(1)
window.geometry("%dx%d+0+0" % (w, h))
# Sets the window background color
window.configure(bg='black')

# Exit button setup
# Function that is called when exit button is clicked
def endProgram():
    window.destroy()
# Setup for the exit button
exitButton = Button(window, text="Exit", command = endProgram, font=exitFont, borderwidth=0, fg=whiteColor, bg='black', highlightthickness=0)
exitButton.pack()
exitButton.place(relx=1.0, rely=0.0, anchor=NE)

# Blue Team Score Label
blueLabel = Label(window, text="0", font=labelFont, fg=blueColor, bg='black')
blueLabel.pack()
blueLabel.place(relx=0.25, rely=0.50, anchor=CENTER)

# White Team Score Label
whiteLabel = Label(window, text="0", font=labelFont, fg=whiteColor, bg='black')
whiteLabel.pack()
whiteLabel.place(relx=0.75, rely=0.50, anchor=CENTER)

# GPIO pin setup
GPIO.setmode(GPIO.BCM)
GPIO.setup(bluegpio, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(whitegpio, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

# Blue team score +1 button was hit
def blue_score(channel):
    global blueScore
    global whiteScore
    # Increase blue team score by one
    blueScore = blueScore + 1
    # Checks to see if a winning score of 11 was reached
    if blueScore >= 11:
        # Checks to see if score won by atleast 2 points
        if (blueScore - whiteScore) >= 2:
            # Resets the score to zero for a new round since a winner was found
            blueScore = 0
            whiteScore = 0
    # Sets the label text equal to the score
    whiteLabel["text"] = whiteScore
    blueLabel["text"] = blueScore
    # Repositions the label text, this important for when the label changes from single to double digits... example: 9 to 10
    whiteLabel.place(relx=0.75, rely=0.50, anchor=CENTER)
    blueLabel.place(relx=0.25, rely=0.50, anchor=CENTER)

# White team score +1 button was hit
def white_score(channel):
    global whiteScore
    global blueScore
    # Increase white team score by one
    whiteScore = whiteScore + 1
    # Checks to see if a winning score of 11 was reached
    if whiteScore >= 11:
        # Checks to see if score won by atleast 2 points
        if (whiteScore - blueScore) >= 2:
            # Resets the score to zero for new round since a winner was found
            blueScore = 0
            whiteScore = 0
    # Sets the label text equal to the score
    whiteLabel["text"] = whiteScore
    blueLabel["text"] = blueScore
    # Repositions the label text, this important for when the label changes from single to double digits... example: 9 to 10
    whiteLabel.place(relx=0.75, rely=0.50, anchor=CENTER)
    blueLabel.place(relx=0.25, rely=0.50, anchor=CENTER)

# GPIO event detection
GPIO.add_event_detect(bluegpio, GPIO.FALLING, callback=blue_score, bouncetime=delayTime)
GPIO.add_event_detect(whitegpio, GPIO.FALLING, callback=white_score, bouncetime=delayTime)

# Begins mainloop
mainloop()
