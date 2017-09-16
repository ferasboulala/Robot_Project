from tkinter import *
from tkinter.messagebox import *
from HW_Classes import *
import time, _thread, pigpio, matplotlib, math, os, numpy as np
matplotlib.use("TkAgg")
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg


# The following function works on my desktop computer but not on the RPi.
# It makes it easier to control the robot without having to press b everytime
# you want to brake. You will find a good deal of global variables throughout
# this file as they are tied to this function. 
def move(event):
    ## global go
    moves = {'w': forward, 's': backward, 'a': left, 'd': right, 'b': brake, 'r': radar}
    ## if go == False:
        ##go = True
    moves[event.keysym]()
    ## else:
        ## pass
    

def forward(speed = 0.25):
    leftMotor.rotate(speed)
    rightMotor.rotate(speed)
    leftLed.setPulse(dc = 1)
    rightLed.setPulse(dc = 1)
    print('FORWARD')


def backward(speed = 0.25):
    leftMotor.rotate(-speed)
    rightMotor.rotate(-speed)
    leftLed.setPulse(dc = 0)
    rightLed.setPulse(dc = 0)
    print('BACKWARD')


def left(speed = 0.25):
    leftMotor.rotate(-speed)
    rightMotor.rotate(speed)
    leftLed.setPulse(dc = 0)
    rightLed.setPulse(dc = 1)
    print('LEFT')


def right(speed = 0.25):
    leftMotor.rotate(speed)
    rightMotor.rotate(-speed)
    leftLed.setPulse(dc = 1)
    rightLed.setPulse(dc = 0)
    print('RIGHT')


def brake(event=None):
    ## global go
    ## go = False
    leftMotor.rotate(0)
    rightMotor.rotate(0)
    leftLed.setPulse(dc = 0)
    rightLed.setPulse(dc = 0)
    print('BRAKE')


def sonar():
    return frontRadar.distance()


def frontVision(frontData):
    frontData.append(frontRadar.distance())


def movement(angle, moving):
    CRITICALDISTANCE = 30
    if not moving:
        forward()
        moving = True
    rotator.rotate(angle)
    time.sleep(0.25)
    distance = sonar()
    if distance > CRITICALDISTANCE:
        pass
    else:
        moving = False
        if angle == 0:
            right()
            time.sleep(0.25)
            return moving
        elif angle == 90:
            backward()
            time.sleep(1)
            brake()
            rotator.rotate(180)
            time.sleep(0.5)
            makeLeft = sonar()
            time.sleep(0.1)
            rotator.rotate(0)
            makeRight = sonar()
            time.sleep(0.5)
            if makeLeft < makeRight:
                left()
            else:
                right()
            time.sleep(0.5)
            return moving
        elif angle == 180:
            left()
            time.sleep(0.25)
            return moving
        elif angle == 150:
            left()
            time.sleep(0.5)
            return moving
        else:
            right()
            time.sleep(0.5)
    return moving


def autopilot():
    rotator.rotate(0)
    time.sleep(1)
    forward()
    moving = True
    first = [0, 30, 90, 150, 180]
    second = [150, 90, 30]
    while control:
        for angle in first:
            moving = movement(angle, moving)
        for angle in second:
            moving = movement(angle, moving)
    brake()
    time.sleep(1)

# Scans 180 degrees in front of the robot
def radar():
    frontData = []
    keepgoing = True
    rotator.rotate(angleR = 0)
    time.sleep(0.5)
    angles = [i * 2 for i in range(90)]
    for angleR in angles:
        rotator.rotate(angleR)
        frontVision(frontData)
        time.sleep(10 * rotator.getSleep())
    rotator.rotate(0)
    global drivePilot
    global firsttime
    interpreter(frontData, drivePilot, firsttime)
    if firsttime:
        firsttime = False

# Plots the received data
def interpreter(frontData, root, firsttime):
    x = []
    y = []
    frontRes = 180 / len(frontData)
    for i in range(len(frontData)):
        angle = frontRes * i
        x.append(float(frontData[i]) * (math.cos(math.radians(180 - angle))))
        y.append(float(frontData[i]) * (math.sin(math.radians(180 - angle))))

    fig, ax = plt.subplots()
    robot = plt.Circle((0,0), 5, color = 'blue')
    ax.add_artist(robot)
    ax.set_axis_bgcolor('black')
    plt.plot(x,y,'c+', markersize = 10, linestyle = '--')
    plt.axis([-100, 100, 0, 100])
##    ax.spines['left'].set_position('center')
##    ax.spines['left'].set_color('cyan')
##    ax.spines['bottom'].set_color('cyan')
##    ax.spines['right'].set_color('none')
##    ax.spines['top'].set_color('none')
##    ax.xaxis.label.set_color('black')
    ax.xaxis.label.set_size(10)
    ax.set_xlabel('Distance (cm)')
    ax.tick_params(axis = 'x', colors = 'black', size = 2)
    ax.grid(True)
    major_ticksx = np.arange(-100, 100, 20)
    major_ticksy = np.arange(0, 100, 10)
    ax.set_xticks(major_ticksx)
    ax.set_yticks(major_ticksy)
##    ax.set_xticks(minor_ticksx, minor = True)
##    ax.set_yticks(minor_ticksy, minor = True)
    gridlines = ax.get_xgridlines() + ax.get_ygridlines()
    for line in gridlines:
        line.set_color('white')
    vision = FigureCanvasTkAgg(fig, root)
##    vision.show()
    vision.get_tk_widget().pack(side=TOP)
##    if os.path.isfile('NOW WE SEE.png'):
##        os.remove('NOW WE SEE.png')
##        time.sleep(1)
##    plt.savefig('NOW WE SEE.png')
    plt.close()
    plt.clf()
    plt.cla()
    

pi = pigpio.pi()


leftMotor = dcMotor(name = 'Left motor', gpio_list = [14, 15], pi = pi)
rightMotor = dcMotor(name = 'Right motor', gpio_list = [23, 24], pi = pi)

rotator = Servo(name = 'Rotator', gpio_list = [27], pi = pi)

frontRadar = Sonic(name = 'Left radar', trig = 2, echo = 3, pi = pi)

leftLed = Led(name = 'Left led', gpio = 21, pi = pi)
rightLed = Led(name = 'Right led', gpio = 22, pi = pi)


def autopilot_thread():
    disableCheck()
    _thread.start_new_thread(autopilot, ())


def pilot_thread():
    disable()
    

def autopilotGUI():
    startAuto.config(state='normal')
    stopAuto.config(state='normal')
    startPilot.config(state=DISABLED)
    stopPilot.config(state=DISABLED)
    

def pilotGUI():  
    startAuto.config(state=DISABLED)
    stopAuto.config(state=DISABLED)
    startPilot.config(state='normal')
    stopPilot.config(state='normal')


def disableCheck():
    global control
    control=True
    choice1.config(state=DISABLED)
    choice2.config(state=DISABLED)


def enableCheck():
    global control
    control=False
    choice1.config(state='normal')
    choice2.config(state='normal')


def disablePilot():
    enableCheck()
    wForward.config(state=DISABLED)
    sBackward.config(state=DISABLED)
    aLeft.config(state=DISABLED)
    dRight.config(state=DISABLED)
    bBrake.config(state=DISABLED)
    rRadar.config(state=DISABLED)
    sBackward.focus_set()


def enablePilot():
    disableCheck()
    wForward.config(state='normal')
    sBackward.config(state='normal')
    aLeft.config(state='normal')
    dRight.config(state='normal')
    bBrake.config(state='normal')
    rRadar.config(state='normal')
    wForward.focus_set()

def callback():
    global control
    if askyesno('Verify', 'Do you really want to quit?'):
        control=False
        brake()
        time.sleep(0.5)
        root.quit()
        root.destroy()


def makemodal(win):
    win.focus_set()
    win.grab_set()
    win.wait_window()


# Root
root = Tk()
root.title('Robot GUI program')
root.geometry("1000x600")
Label(root, text='ROBOT', font=('Arial', 20)).pack(side=TOP)
Label(root, text='by Feras Boulala', font=('Arial', 10)).pack(side=TOP)
programQuit = Button(root, text='Quit', command=callback, relief=RIDGE)
programQuit.pack(side=BOTTOM, fill=BOTH)

# Frames
mode = Frame(root, bd=4, relief=GROOVE)
mode.pack(side=LEFT, fill=BOTH, expand=TRUE)

drive = Frame(root, bd=4, relief=GROOVE)
drive.pack(side=RIGHT, fill=BOTH, expand=TRUE)
driveAuto = Frame(drive, bd=4)
driveAuto.pack(side=TOP, fill=BOTH)
drivePilot = Frame(drive, bd=4)
drivePilot.pack(side=TOP, fill=BOTH, expand=TRUE)

# The next two lines make the size of the frames constant
mode.pack_propagate(0)
drive.pack_propagate(0)
drivePilot.pack_propagate(0)

# Buttons
var = StringVar()
choice1 = Radiobutton(mode, text='Autopilot', command=autopilotGUI, variable=var, value='Autopilot', indicatoron=0)
choice2 = Radiobutton(mode, text='Pilot', command=pilotGUI, variable=var, value='Pilot', indicatoron=0)
choice1.pack(fill=BOTH, anchor=W)
choice2.pack(fill=BOTH, anchor=W)

control = False
startAuto = Button(driveAuto, text='Start autopilot', state=DISABLED, command=autopilot_thread)
startAuto.pack(fill=BOTH)
stopAuto = Button(driveAuto, text='Stop autopilot', state=DISABLED, command=enableCheck)
stopAuto.pack(fill=BOTH)
startPilot = Button(drivePilot, text='Start pilot', state=DISABLED, command=enablePilot)
startPilot.pack(fill=BOTH)
stopPilot = Button(drivePilot, text='Stop pilot', state=DISABLED, command=disablePilot)
stopPilot.pack(fill=BOTH)

# Movement
wForward = Label(drivePilot, text='W: fwd()', state=DISABLED)
sBackward = Label(drivePilot, text='S: bwd()', state=DISABLED)
aLeft = Label(drivePilot, text='A: left()', state=DISABLED)
dRight = Label(drivePilot, text='D: right()', state=DISABLED)
bBrake = Label(drivePilot, text='B: brake()', state=DISABLED)
firsttime = True
rRadar = Label(drivePilot, text='R: radar()', state=DISABLED)

## go = False
wForward.bind("<KeyPress>", move)
## wForward.bind("<KeyRelease>", brake)

wForward.pack(side=TOP)
sBackward.pack(side=BOTTOM)
aLeft.pack(side=LEFT)
dRight.pack(side=RIGHT)
bBrake.pack(side=BOTTOM)
rRadar.pack(side=TOP)

# Other widgets
descriptionF = Frame(mode, bd=4, relief=GROOVE)
descriptionF.pack()
description = Text(descriptionF)
description.pack()
description.insert(END, '''AUTOPILOT:\n\nThe robot starts moving automatically once the start button is pressed. It will move at relatively slow speed. Once it reaches a critical distance of 30 cm, it will chose a course of action. The user does not have to control the robot in any way. \nTo stop autopilot, press the button.\n\n
PILOT:\n\nThe robot will start moving after the user has pressed the start button and a movement key. Forward is w, backward
is s and left and right are a and d respectively.\nTo stop pilot mode, press the button.''')
description.insert(END, '''leftMotor = dcMotor(name = Left motor, gpio_list = [14, 15], pi = pi)\n
rightMotor = dcMotor(name = Right motor, gpio_list = [23, 24], pi = pi)\n
rotator = Servo(name = Rotator, gpio_list = [27], pi = pi)\n
frontRadar = Sonic(name = Left radar, trig = 2, echo = 3, pi = pi)\n
leftLed = Led(name = Left led, gpio = 21, pi = pi)\n
rightLed = Led(name = Right led, gpio = 22, pi = pi)''')
                   
root.mainloop()
