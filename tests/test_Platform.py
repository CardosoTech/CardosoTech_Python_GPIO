import unittest

from mock import Mock, patch

import CardosoTech_GPIO.Platform as Platform


class TestPlatformDetect(unittest.TestCase):
    @patch('platform.platform', Mock(return_value='Linux-3.8.13-bone47-armv7l-with-debian-7.4'))
    def test_beaglebone_black(self):
        result = Platform.platform_detect()
        self.assertEquals(result, Platform.BEAGLEBONE_BLACK)

    @patch('platform.platform', Mock(return_value='Darwin-13.2.0-x86_64-i386-64bit'))
    def test_unknown(self):
        result = Platform.platform_detect()
        self.assertEquals(result, Platform.UNKNOWN)


class TestPiRevision(unittest.TestCase):
    def test_revision_1(self):
        with patch('__builtin__.open') as mock_open:
            handle = mock_open.return_value.__enter__.return_value
            handle.__iter__.return_value = iter(['Revision : 0000'])
            rev = Platform.pi_revision()
            self.assertEquals(rev, 1)
        with patch('__builtin__.open') as mock_open:
            handle = mock_open.return_value.__enter__.return_value
            handle.__iter__.return_value = iter(['Revision : 0002'])
            rev = Platform.pi_revision()
            self.assertEquals(rev, 1)
        with patch('__builtin__.open') as mock_open:
            handle = mock_open.return_value.__enter__.return_value
            handle.__iter__.return_value = iter(['Revision : 0003'])
            rev = Platform.pi_revision()
            self.assertEquals(rev, 1)

    def test_revision_2(self):
        with patch('__builtin__.open') as mock_open:
            handle = mock_open.return_value.__enter__.return_value
            handle.__iter__.return_value = iter(['Revision : 000e'])
            rev = Platform.pi_revision()
            self.assertEquals(rev, 2)

    def test_unknown_revision(self):
        with patch('__builtin__.open') as mock_open:
            handle = mock_open.return_value.__enter__.return_value
            handle.__iter__.return_value = iter(['foobar'])
            self.assertRaises(RuntimeError, Platform.pi_revision)

