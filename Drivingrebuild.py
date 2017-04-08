# Embedded file name: Driving.py
import viz
import vizconnect
import vizact
import vizinfo
import vizinput
import vizcam

maxspeed = 120
handmax = 30
handle = 0.4
accel = 0.2
deaccel = 0.1
brake = 1.5
maxgear = 5
gear = 0
auto = 0

handlerightmax = handmax
handleleftmax = -handmax

offsetNode = viz.addChild("ball.wrl")
offsetNode.alpha(0)
car = viz.addChild("mini.osg", parent = offsetNode) #load car model here
car.setPosition(0.3,-1.1,0.2) 
viz.setMultiSample(4)
NUM_CARS = 0
carlist = []
pivot = [0, 0, 0]
carchoice = 1
currentcar = 'Mini'
speed = 0.0
steer = 0.0
motion = 0
rotateY = 0.0
rotateX = 0.0
viz.clip(0.1, 30000)
vizconnect.go('camera.py')
viz.splashScreen('assets/tracksplash.jpg')
viz.phys.enable()
#carchoiceinit = vizinput.choose('Choose a car:', ['Mini','BMW','Ford Thunderbird','Ford Focus','Lamborghini Murcielago','TVR Speed 12','Dodge Challenger', 'Caterham Seven'])
#carchoice = carchoiceinit + 1
environmentchoice = vizinput.choose('Select time of day:', ['Day', 'Night'])
viz.message('Arrow Keys to steer. Z to go down a gear, X to go up a gear. G to swap between automatic/manual. Up to accelerate, Down to reverse (Automatic only). Spacebar to brake.')
#import Drivingfunctions
track = viz.addChild('assets/environment/track.osgb')
station = viz.addChild('assets/environment/gasStation.fbx')
#buildings = viz.addChild('assets/environment/City.osgb')
tower = viz.addChild('assets/environment/Building.fbx')
if environmentchoice == 0:
    environment = viz.addChild('sky_day.osgb')
else:
    environment = viz.addChild('sky_night.osgb')
environment.setScale(10, 10, 10)
track.setScale(5, 0, 5)
station.setScale(5, 5, 5)
#buildings.setScale(1, 1, 1)
station.setEuler(90, 0, 0)
track.setPosition(260, -3, 15)
tower.setPosition(500, -3, -75)
tower.setScale(1.5, 4, 1.5)
station.setPosition(-100, -3.3, 250)
station.collideMesh()
#buildings.collideMesh()
tower.collideMesh()
speeddisplay = viz.addTextbox()
speeddisplay.setPosition(0.11, 0.985)
steerdisplay = viz.addTextbox()
steerdisplay.setPosition(0.11, 0.95)
cardisplay = viz.addTextbox()
cardisplay.setPosition(0.9, 0.02)
geardisplay = viz.addTextbox()
geardisplay.setPosition(0.11, 0.915)
headLight = viz.MainView.getHeadLight()
headLight.disable()
myLight = viz.addLight()
view = viz.MainView
if environmentchoice == 0:
    myLight.intensity(1)
else:
    myLight.intensity(0.25)
myLight.setEuler(45, 12, 0)
camera = vizconnect.getTransport('orientation')
rotcam = viz.link(offsetNode, camera.getNode3d())

viz.mergeLinkable(rotcam, view)

def ChangeCar(direction):
    global carchoice
    global speed
    global accel
    global steer
    if direction == 2:
        carchoice += 1
        if carchoice > NUM_CARS:
            carchoice = 1
    else:
        carchoice -= 1
        if carchoice <= 0:
            carchoice = NUM_CARS
    offsetNode.setPosition(0, 0, 0)
    offsetNode.setEuler(0, 0, 0)
    speed = 0.0
    steer = 0.0
    accel = 0
    rotateX = 0
    rotateY = 0
    view.setEuler(0, 0, 0)


def CarUpdate():
    global rotateX
    global currentcar
    global speed
    global rotateY
    global deaccel

    if speed > 0:
        speed -= deaccel
    if speed < 0:
        speed += deaccel


    if speed < 0.1:
        motion = 0
    else:
        motion = 1
    move = vizact.move([0, 0, speed / 1.5], 0.1)
    rotate = vizact.spin(0, 1, 0, steer * (speed / 1.5) * 0.05, 0.1)
    viewmoveX = vizact.spinTo(quat=[rotateX,rotateY,0, 2], time=0.1)
    offsetNode.clearActions()
    offsetNode.clearActionList()
    offsetNode.add(move, 0)
    offsetNode.add(rotate, 1)
    environment.setPosition(offsetNode.getPosition())
    speeddisplay.message('Speed: ' + str(speed))
    steerdisplay.message('Steer: ' + str(steer))
    if auto:
        geardisplay.message('Gear: Automatic')
    else:
        if gear < 0:
            geardisplay.message('Gear: Reverse')
        if gear == 0:
            geardisplay.message('Gear: Neutral')
        else:
            geardisplay.message('Gear: ' + str(gear))
    cardisplay.message(str(currentcar))


def Accelerate():
    global speed
    global maxspeed
    global accel
    global auto
    global gear
    
    if auto:
        if speed < maxspeed + accel:
            speed += accel
        else:
            speed = maxspeed + accel
    else:
        if gear > 0:
            if speed < ((maxspeed / maxgear) * gear) + accel:
                speed += accel
            else:
                speed = ((maxspeed / maxgear) * gear) + accel
        if gear < 0:
            if speed > -(maxspeed / 3):
                speed -= accel / 3
                #accel = 1

def Brake():
    global speed
    global brake
    if speed > 0:
        speed -= brake
    if speed < 0:
        speed += brake



def SteerRight():
    global steer
    global handle
    global handlerightmax
    if steer < handlerightmax:
        steer += handle


def SteerLeft():
    global steer
    global handle
    global handleleftmax
    if steer > handleleftmax:
        steer -= handle


def Reverse():
    global motion
    global speed
    global accel
    global gear
    global auto
    
    if auto:
        if motion == 0:
            if speed > -(maxspeed / 3):
                speed -= accel / 3
                #accel = 1
            
def GearUp():
    global gear
    
    if gear < maxgear:
        gear += 1
    
def GearDown():
    global gear
    
    if gear > -1:
        gear -= 1
        
def SwapAuto():
    global auto
    global gear
    global speed
    global steer
    
    if auto == 1:
        auto = 0
    else:
        auto = 1
        
    gear = 0
    speed = 0
    steer = 0
    



#vizact.onkeydown('[', ChangeCar, 1)
#vizact.onkeydown(']', ChangeCar, 2)
vizact.ontimer(0.1, CarUpdate)
vizact.whilekeydown(viz.KEY_UP, Accelerate)
vizact.whilekeydown(' ', Brake)
vizact.whilekeydown(viz.KEY_LEFT, SteerLeft)
vizact.whilekeydown(viz.KEY_RIGHT, SteerRight)
vizact.whilekeydown(viz.KEY_DOWN, Reverse)
vizact.onkeydown('z', GearDown)
vizact.onkeydown('x', GearUp)
vizact.onkeydown('g', SwapAuto)