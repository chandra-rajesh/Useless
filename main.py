from machine import Pin, PWM
import time

servo = PWM(Pin(15))
servo.freq(50)
rain = Pin(14, Pin.IN)
button = Pin(13, Pin.IN, Pin.PULL_UP)


def move_servo(angle):
    duty = int((angle / 180) * 5000 + 2500)
    servo.duty_u16(duty)


def wipe(times, delay):
    for i in range(times):
        move_servo(90)
        time.sleep(delay)
        move_servo(210)
        time.sleep(delay)
    move_servo(0)

last_press = 0
press_count = 0

while True:
    print(rain.value())
    
    if rain.value() == 0:  
        print("Rain detected! Wiping...")
        wipe(5, 0.5)
        time.sleep(1)

    
    if button.value() == 0:  
        now = time.ticks_ms()
        if now - last_press < 400:  
            press_count += 1
        else:
            press_count = 1
        last_press = now

        
        while button.value() == 0:
            time.sleep(0.05)

        
        if press_count == 1:
            print("Single press: Normal wipe")
            wipe(5, 0.5)

       
        if press_count == 2:
            print("Double press: Fast wipe")
            wipe(10, 0.2)
            press_count = 0  

    time.sleep(0.05)
