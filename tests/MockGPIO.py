import CardosoTech_GPIO as GPIO

class MockGPIO(GPIO.BaseGPIO):
    def __init__(self):
        self.pin_mode = {}
        self.pin_written = {}
        self.pin_read = {}

    def setup(self, pin, mode):
        self.pin_mode[pin] = mode

    def output(self, pin, bit):
        self.pin_written.setdefault(pin, []).append(1 if bit else 0)

    def input(self, pin):
        if pin not in self.pin_read:
            raise RuntimeError('No mock GPIO data to read for pin {0}'.format(pin))
        return self.pin_read[pin].pop(0) == 1
