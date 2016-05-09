import RPi.GPIO as GPIO
from time import sleep

# Codes for switching on and off the sockets
#        all     1       2       3       4
ON  = ['1011', '1111', '1110', '1101', '1100']
OFF = ['0011', '0111', '0110', '0101', '0100']

# The GPIO pins for the Energenie module
BITS = {
    "rev1" : {
        "bits" : [ 11, 15, 16, 13 ],
        "on_off" : 18,
        "enable" : 22,
        "gpio" : GPIO.BOARD
    },
    "other" : {
        "bits" : [ 17, 22, 23, 27 ],
        "on_off" : 24,
        "enable" : 25,
        "gpio" : GPIO.BCM
    }
}

config = BITS["rev1" if GPIO.RPI_REVISION == 1 else "other"]
config["pins"] = config["bits"] + [ config["on_off"], config["enable"] ]

GPIO.setmode(config["gpio"])
GPIO.setwarnings(False)

# Initial pin setup
[ GPIO.setup(b, GPIO.OUT) for b in config["pins"] ]
[ GPIO.output(b, False)   for b in config["pins"] ]

def change_plug_state(socket, on_or_off):
    total = len(config["bits"])
    for i in range(total):
        GPIO.output(config["bits"][i], on_or_off[socket][total - i - 1] == '1')
        
    
    sleep(0.1)
    GPIO.output(config["enable"], True)
    sleep(0.25)
    GPIO.output(config["enable"], False)


def switch_on(socket=0):
    change_plug_state(socket, ON)


def switch_off(socket=0):
    change_plug_state(socket, OFF)
