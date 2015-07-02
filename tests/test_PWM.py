import unittest

from mock import Mock, patch

import CardosoTech_GPIO.PWM as PWM
import CardosoTech_GPIO.Platform as Platform


class TestRPi_PWM_Adapter(unittest.TestCase):
    def test_setup(self):
        rpi_gpio = Mock()
        pwm = PWM.RPi_PWM_Adapter(rpi_gpio)
        pwm.start(1, 50)
        rpi_gpio.PWM.assert_called_with(1, 2000)

    def test_set_duty_cycle_valid(self):
        rpi_gpio = Mock()
        pwm = PWM.RPi_PWM_Adapter(rpi_gpio)
        pwm.start(1, 50)
        pwm.set_duty_cycle(1, 75)
        # Implicit verification that no assertion or other error thrown.

    def test_set_duty_cycle_invalid(self):
        rpi_gpio = Mock()
        pwm = PWM.RPi_PWM_Adapter(rpi_gpio)
        pwm.start(1, 50)
        self.assertRaises(ValueError, pwm.set_duty_cycle, 1, 150)
        self.assertRaises(ValueError, pwm.set_duty_cycle, 1, -10)

    def test_set_frequency(self):
        rpi_gpio = Mock()
        pwm = PWM.RPi_PWM_Adapter(rpi_gpio)
        pwm.start(1, 50)
        pwm.set_frequency(1, 1000)
        # Implicit verification that no assertion or other error thrown.


class TestBBIO_PWM_Adapter(unittest.TestCase):
    def test_setup(self):
        bbio_pwm = Mock()
        pwm = PWM.BBIO_PWM_Adapter(bbio_pwm)
        pwm.start('P9_16', 50)
        bbio_pwm.start.assert_called_with('P9_16', 50, 2000)

    def test_set_duty_cycle_valid(self):
        bbio_pwm = Mock()
        pwm = PWM.BBIO_PWM_Adapter(bbio_pwm)
        pwm.start('P9_16', 50)
        pwm.set_duty_cycle('P9_16', 75)
        bbio_pwm.set_duty_cycle.assert_called_with('P9_16', 75)

    def test_set_duty_cycle_invalid(self):
        bbio_pwm = Mock()
        pwm = PWM.BBIO_PWM_Adapter(bbio_pwm)
        pwm.start('P9_16', 50)
        self.assertRaises(ValueError, pwm.set_duty_cycle, 'P9_16', 150)
        self.assertRaises(ValueError, pwm.set_duty_cycle, 'P9_16', -10)

    def test_set_frequency(self):
        bbio_pwm = Mock()
        pwm = PWM.BBIO_PWM_Adapter(bbio_pwm)
        pwm.start('P9_16', 50)
        pwm.set_frequency('P9_16', 1000)
        bbio_pwm.set_frequency.assert_called_with('P9_16', 1000)


class TestGetPlatformPWM(unittest.TestCase):
    @patch.dict('sys.modules', {'RPi': Mock(), 'RPi.GPIO': Mock()})
    @patch('CardosoTech_GPIO.Platform.platform_detect', Mock(return_value=Platform.RASPBERRY_PI))
    def test_raspberrypi(self):
        pwm = PWM.get_platform_pwm()
        self.assertIsInstance(pwm, PWM.RPi_PWM_Adapter)

    @patch.dict('sys.modules', {'Adafruit_BBIO': Mock(), 'Adafruit_BBIO.PWM': Mock()})
    @patch('CardosoTech_GPIO.Platform.platform_detect', Mock(return_value=Platform.BEAGLEBONE_BLACK))
    def test_beagleboneblack(self):
        pwm = PWM.get_platform_pwm()
        self.assertIsInstance(pwm, PWM.BBIO_PWM_Adapter)

    @patch('CardosoTech_GPIO.Platform.platform_detect', Mock(return_value=Platform.UNKNOWN))
    def test_otherplatform(self):
        self.assertRaises(RuntimeError, PWM.get_platform_pwm)
