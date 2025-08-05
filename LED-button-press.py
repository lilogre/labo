# Must install RPi.GPIO
# sudo apt-get install python3-rpi.gpio

import RPi.GPIO as GPIO
import threading
import time

# Pin configuration
LED_PIN = 18
BUTTON_PIN = 17

# GPIO setup
GPIO.setmode(GPIO.BCM)
GPIO.setup(LED_PIN, GPIO.OUT)
GPIO.setup(BUTTON_PIN, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

# Shared state
led_on = False
lock = threading.Lock()  # For thread-safe LED state changes

# Callback for button press (edge detected)
def handle_button_press(channel):
    global led_on
    with lock:
        led_on = not led_on  # Toggle LED state
        GPIO.output(LED_PIN, GPIO.HIGH if led_on else GPIO.LOW)
        print(f"Button pressed. LED {'ON' if led_on else 'OFF'}")

# Set up edge detection with debounce
GPIO.add_event_detect(BUTTON_PIN, GPIO.RISING, callback=handle_button_press, bouncetime=200)

try:
    print("Waiting for button press. Press CTRL+C to exit.")
    while True:
        time.sleep(1)  # Main thread does nothing; interrupt-driven

except KeyboardInterrupt:
    print("\nExiting program...")

finally:
    GPIO.cleanup()
