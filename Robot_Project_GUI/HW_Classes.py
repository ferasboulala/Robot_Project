''' This file contains all the classes for general usage of
    hardware for hobby robotics. They are intended for easy of use
    aswell as reusability.

    Most of the classes' methods are here for good measure. They
    aren't used thoughout the code (ex: change a motor's GPIO can be done
    but since it requires physical contact with the robot, it has practically
    no use.
'''

import pigpio, time

# Motor class that all the specific motors will derive from.
class Motor:
    def __init__(self, gpio_list, name, pi):
        self.name = name
        self.gpio = gpio_list
        self.pi = pi
        for pin in self.gpio:
            self.pi.set_mode(pin, pigpio.OUTPUT)
            self.pi.write(pin,0) # Set to 0 for precaution


    def getName(self):
        return self.name

    
    def getGPIO(self):
        return self.gpio


    def clear(self, full = False):
        self.pi.stop()
        print('%s %s %s %s' % ('Motor ', self.__class__.__name__, self.name, ' pins are 0'))
        self.gpio = None
        if full:
            self.name = 'Motor cleaned'


    def setName(self, name):
        self.name = name

        
    def setGPIO(self, gpio_list):
        self.clear()
        self.gpio = gpio_list
        self.pi = pigpio.pi(self.name)
        for pin in self.gpio:
            self.pi.set_mode(pin, pigpio.OUTPUT)
            self.pi.write(pin,0)

# ------------------------- DC MOTOR ------------------------- #
class dcMotor(Motor):
    def __init__(self, gpio_list, name, pi, frequency = 50):
        Motor.__init__(self, name = name, gpio_list = gpio_list, pi = pi)
        self.frequency = frequency
        self.pi.set_PWM_frequency(self.gpio[0], self.frequency)
        self.pi.set_PWM_frequency(self.gpio[1], self.frequency) 
        self.pi.set_PWM_dutycycle(self.gpio[0], 0)
        self.pi.set_PWM_dutycycle(self.gpio[1], 0)


    def getFrequency(self):
        return self.frequency


    def setFrequency(self, frequency):
        self.frequency = frenquency
        self.pi.set_PWM_frequency(self.gpio[0], self.frequency)
        self.pi.set_PWM_frequency(self.gpio[1], self.frequency)
    def setGPIO(self, gpio_list):

        
        Motor.setGPIO(self, gpio_list = gpio_list)
        self.pi.set_PWM_frequency(self.gpio[0], self.frequency)
        self.pi.set_PWM_frequency(self.gpio[1], self.frequency)
        self.pi.set_PWM_dutycycle(self.gpio[0], 0)
        self.pi.set_PWM_dutycycle(self.gpio[1], 0)
        

    def rotate(self, speed = 1):
        if speed >= 0:
            self.pi.set_PWM_dutycycle(self.gpio[0], 255 * speed)
            self.pi.set_PWM_dutycycle(self.gpio[1], 0)
        else:
            self.pi.set_PWM_dutycycle(self.gpio[0], 0)
            self.pi.set_PWM_dutycycle(self.gpio[1], 255 * abs(speed))

# ------------------------- SERVO MOTOR ------------------------- #
class Servo(Motor):
    def __init__(self, pi, gpio_list, name = '', frequency = 50, minPulse = 0.0006, maxPulse = 0.0024, sleep = 0.01):
        Motor.__init__(self, name = name, gpio_list = gpio_list, pi = pi)
        self.frequency = frequency
        self.minPulse = minPulse
        self.maxPulse = maxPulse
        self.sleep = sleep
        self.pi.set_PWM_frequency(self.gpio[0], self.frequency)
        self.pi.set_PWM_dutycycle(self.gpio[0], 0)
        
## Most of those functions are here for a form purpose. They will most likely
## never be used.
    def getFrequency(self):
        return self.frequency

    
    def getMinPulse(self):
        return self.minPulse

    
    def getMaxPulse(self):
        return self.maxPulse

    
    def getSleep(self):
        return self.sleep


    def setFrequency(self, frequency):
        self.frequency = frequency
        self.pi.set_PWM_frequency(self.gpio[0], self.frequency)

        
    def setMinPulse(self, minPulse):
        self.minPulse = minPulse

        
    def setMaxPulse(self, maxPulse):
        self.maxPulse = maxPulse

        
    def setSleep(self, sleep):
        self.sleep = sleep
        

    def setGPIO(self, gpio_list):
        Motor.setGPIO(self, gpio_list = gpio_list)
        self.pi.set_PWM_frequency(self.gpio[0], self.frequency)
        self.pi.set_PWM_dutycycle(self.gpio[0], 0)
        print('%s %s %s' % ('Frequency set to current frequency = ', self.frequency, ' Hz'))
        print('%s %s %s %s' % ('Motor ', self.__class__.__name__, self.name, 'gpios set'))


    def angle(self, angleR):
        dcMin = self.minPulse * self.frequency 
        dcMax = self.maxPulse * self.frequency 
        dc = angleR * (dcMax - dcMin) / 180 + dcMin
        return dc


    def pulsewidth(self, angleR):
        return (1000000 * ((self.maxPulse - self.minPulse) * angleR/180 + self.minPulse))


    def rotatew(self, angleR = 90):
        self.pi.set_servo_pulsewidth(self.gpio[0], self.pulsewidth(angleR = angleR))
        
        
    def rotate(self, angleR = 90):
        self.pi.set_PWM_dutycycle(self.gpio[0], int(255 * self.angle(angleR)))

# ------------------------- GENERAL PURPOSE LED ------------------------- #
class Led:
    def __init__(self, gpio, name, pi, frequency = 2):
        self.name = name
        self.gpio = gpio
        self.frequency = frequency
        self.pi = pi
        self.pi.set_mode(self.gpio, pigpio.OUTPUT) # Possibly useless along with the next line.
        self.pi.write(self.gpio, 0)
        self.pi.set_PWM_frequency(self.gpio, self.frequency)
        self.pi.set_PWM_dutycycle(self.gpio, 0)

    def getName(self):
        return self.name

    
    def getGPIO(self):
        return self.gpio

    
    def getFrequency(self):
        return self.frequency
    

    def setName(self, name):
        self.name = name
        

    def clear(self, full = False):
        self.pi.stop()
        self.gpio = None
        if full:
           self.name = 'LED cleaned.'
           

    def setFrequency(self, frequency):
       self.frequency = frequency
       self.pi.set_PWM_frequency(self.gpio, self.frequency)
       

    def setGPIO(self, gpio):
        self.clear()
        self.gpio = gpio
        self.pi = pigpio.pi(self.name)
        self.pi.set_PWM_frequency(self.gpio, self.frequency)
        self.pi.set_PWM_dutycycle(self.gpio, 0)
        print('LED gpio changed')
        

    def setPulse(self, dc):
        self.pi.set_PWM_dutycycle(self.gpio, (255 * dc))
        

    def blink(self):
        self.pi.set_PWM_dutycycle(self.gpio, (255 * 0.5))

# ------------------------- HC-SR04 ------------------------- #
class Sonic:
    def __init__(self, trig, echo, name, pi, sleep = 0.07):
        self.name = name
        self.trig = trig
        self.echo = echo
        self.pi = pi
        self.sleep = sleep
        self.pi.set_mode(trig, pigpio.OUTPUT)
        self.pi.set_mode(echo, pigpio.INPUT)
        self.pi.write(self.trig, 0)


    def getName(self):
        return self.name

    
    def getTrig(self):
        return self.trig

    
    def getEcho(self):
        return self.echo

    
    def getSleep(self):
        return self.sleep
    

    def clear(self, full = False):
        self.pi.stop()
        self.trig = None
        self.echo = None
        if full:
           self.name = 'Sonic sensor cleared.'
           

    def setGPIO(self, trig, echo):
        self.clear()
        self.trig = trig
        self.echo = echo
        self.pi = pigpio.pi(name)
        self.pi.set_mode(trig, pigpio.OUTPUT)
        self.pi.set_mode(echo, pigpio.INPUT)
        

    def distance(self):
        self.pi.write(self.trig, 1)
        time.sleep(0.00001)
        self.pi.write(self.trig, 0)
        toolong = time.time()
        while self.pi.read(self.echo) == 0:
            if (toolong - time.time()) >= 0.007:
                return (0.007 * 17000)
            pass
        start = time.time()
        while self.pi.read(self.echo) == 1:
            pass
        stop = time.time()
        return ((stop - start) * 17000)
    
