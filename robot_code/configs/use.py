import time

def mapping(x,min_val,max_val,aim_min,aim_max):
    x = aim_min + abs((x - min_val) / (max_val- min_val) * (aim_max-aim_min))
    return x

def soft_reset():
    from robot_code.utils.pin import Pin
    soft_reset_pin = Pin("D16")
    soft_reset_pin.low()
    time.sleep(0.01)
    soft_reset_pin.high()
    time.sleep(0.01)