# TODO: kernel version? UI_DEV_SETUP?
# TODO: generic vendor and product id

import fcntl
import time
import unittest
from unittest import skip

from uinput_api import *


class UInputApiTest(unittest.TestCase):
    def test_macros(self):
        self.assertEqual(1, IOC_WRITE)
        self.assertEqual(1073741824, IOC_WRITE << IOC_DIRSHIFT)
        self.assertEqual(0, IOC_NRSHIFT)
        self.assertEqual(8, IOC_TYPESHIFT)
        self.assertEqual(16, IOC_SIZESHIFT)
        self.assertEqual(30, IOC_DIRSHIFT)
        self.assertEqual(85, UINPUT_IOCTL_BASE)
        self.assertEqual(1074025828, UI_SET_EVBIT)
        self.assertEqual(1079792899, UI_DEV_SETUP)
        self.assertEqual(21761, UI_DEV_CREATE)
        self.assertEqual(21762, UI_DEV_DESTROY)

    @staticmethod
    @skip("uncompleted")
    def test_send_space_to_virtual_uinput_device():
        with open("/dev/uinput", "wb") as fp:
            fcntl.ioctl(fp, UI_SET_EVBIT, EV_KEY)
            fcntl.ioctl(fp, UI_SET_KEYBIT, KEY_SPACE)

            uinput_setup = UIntputSetup()
            uinput_setup.name = bytes("Linux Remote Control Android App", encoding="utf-8")
            uinput_setup.input_id.bustype = BUS_USB
            uinput_setup.input_id.vendor = 0x1234
            uinput_setup.input_id.product = 0x5678

            fcntl.ioctl(fp, UI_DEV_SETUP, bytes(uinput_setup))
            fcntl.ioctl(fp, UI_DEV_CREATE)

            # wait for device initialization
            time.sleep(1)

            def emit(fp, _type, code, value):
                input_event = InputEvent()
                input_event.type = _type
                input_event.code = code
                input_event.value = value

                fp.write(bytes(input_event))
                fp.flush()

            emit(fp, EV_KEY, KEY_SPACE, 1)
            emit(fp, EV_SYN, SYN_REPORT, 0)
            emit(fp, EV_KEY, KEY_SPACE, 0)
            emit(fp, EV_SYN, SYN_REPORT, 0)

            fcntl.ioctl(fp, UI_DEV_DESTROY)


if __name__ == "__main__":
    unittest.main()
