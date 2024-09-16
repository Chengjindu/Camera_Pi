import RPi.GPIO as GPIO
import time
import sys
import signal

# Setup GPIO pins, change the GPIOs for your setting
out1 = 11
out2 = 12
out3 = 23
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
GPIO.setup(out1, GPIO.OUT)
GPIO.setup(out2, GPIO.OUT)
GPIO.setup(out3, GPIO.OUT)
GPIO.output(out1, False)
GPIO.output(out2, False)
GPIO.output(out3, False)

# Function to clean up GPIO pins and turn off LEDs
def cleanup_gpio(signum, frame):
    GPIO.output(out1, False)
    GPIO.output(out2, False)
    GPIO.output(out3, False)
    GPIO.cleanup()  # Clean up GPIO to ensure a clean exit
    sys.exit(0)  # Exit the script

# Attach the cleanup function to SIGTERM signal
signal.signal(signal.SIGTERM, cleanup_gpio)

try:
    while True:
        GPIO.output(out1, GPIO.HIGH)
        GPIO.output(out2, GPIO.HIGH)
        GPIO.output(out3, GPIO.HIGH)
except KeyboardInterrupt:
    # This block may not be necessary if the script is always run in the background
    pass
finally:
    # Ensure LEDs are turned off before exiting
    cleanup_gpio(None, None)
