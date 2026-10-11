from pybricks.hubs import PrimeHub
from robot import drive_base, left_arm, right_arm, set_speed
from pybricks.parameters import Stop
from pybricks.tools import wait

#combining leafcutter, humongous fungus, window to the past, biocentric architecture, keystone species
def run():
    hub = PrimeHub()

    wait(200)
    drive_base.reset()
    drive_base.use_gyro(True)
    #starting humongous fungus mission:
    set_speed(speed=250)
    drive_base.straight(358)
    set_speed(turn_rate=200,turn_accel=200, speed=400)
    drive_base.turn(90)    
    drive_base.straight(616)
    set_speed(50)
    drive_base.straight(90)
    wait(200)

    drive_base.turn(-10)
    set_speed(110)
    drive_base.straight(-90)

    #starting window to the past
    drive_base.turn(210)
    set_speed(accel=600, speed=500, turn_rate=90)
    drive_base.straight(70)
    drive_base.turn(-20)
    drive_base.turn(20)
    drive_base.straight(-70)

    #starting leafcutter mission
    set_speed(turn_rate=165)
    drive_base.turn(65)
    set_speed(200)
    drive_base.straight(260)
    drive_base.turn(-47)
    set_speed(speed=100, accel=100)
    #wait(100)
    drive_base.straight(-300)    
    #starting biocentric architecture
    drive_base.turn(-9.5)
    set_speed(speed=200, turn_rate=150)
    drive_base.straight(520)
    drive_base.turn(57)
    set_speed(speed=250, accel=200)
    drive_base.straight(55)
    drive_base.straight(-30)
    drive_base.turn(35)
    set_speed(speed=500, accel=500)    
    set_speed(speed=400, accel=400)
    drive_base.straight(-700, Stop.COAST)
    drive_base.use_gyro(False)
    
    #drive_base.straight(200)
    #drive_base.turn(70)
    #wait(30000)
    #drive_base.use_gyro(False)

    #starting Window to the Past mission

    
    #drive_base.straight(130)
    #drive_base.turn(-93)
    #set_speed(500)
    #drive_base.straight(800)
    #drive_base.use_gyro(False)
    



