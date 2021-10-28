from ctypes import Structure, c_long, c_uint16, c_uint32, c_int32, c_int, sizeof, c_char

# see: https://github.com/torvalds/linux/search?q=_IOC_SIZEBITS
# see: https://github.com/torvalds/linux/blob/v5.4/include/uapi/asm-generic/ioctl.h#L23
IOC_NRBITS = 8
IOC_TYPEBITS = 8
IOC_SIZEBITS = 14
IOC_DIRBITS = 2

IOC_NRSHIFT = 0
IOC_TYPESHIFT = (IOC_NRSHIFT + IOC_NRBITS)
IOC_SIZESHIFT = (IOC_TYPESHIFT + IOC_TYPEBITS)
IOC_DIRSHIFT = (IOC_SIZESHIFT + IOC_SIZEBITS)

IOC_NONE = 0
IOC_WRITE = 1
IOC_READ = 2


def IOC(_dir, _type, nr, size):
    return (_dir << IOC_DIRSHIFT) | \
           (_type << IOC_TYPESHIFT) | \
           (nr << IOC_NRSHIFT) | \
           (size << IOC_SIZESHIFT)


def IO(_type, nr):
    return IOC(IOC_NONE, _type, nr, 0)


def IOR(_type, nr, c_type):
    return IOC(IOC_READ, _type, nr, sizeof(c_type))


def IOW(_type, nr, c_type):
    return IOC(IOC_WRITE, _type, nr, sizeof(c_type))


# see: https://github.com/torvalds/linux/blob/v5.4/include/uapi/asm-generic/posix_types.h#L89
kernel_time_t = c_long

# see: https://github.com/torvalds/linux/blob/v5.4/include/uapi/asm-generic/posix_types.h#L41
kernel_suseconds_t = c_long


# see: https://github.com/torvalds/linux/blob/v5.4/include/uapi/linux/time.h#L16
class Timeval(Structure):
    _fields_ = [
        ("tv_sec", kernel_time_t),
        ("tv_usec", kernel_suseconds_t),
    ]


# see: https://github.com/torvalds/linux/blob/v5.4/include/uapi/linux/input-event-codes.h#L38
# Event types
EV_SYN = 0x00
EV_KEY = 0x01

# Synchronization events
SYN_REPORT = 0

# Keys and buttons
KEY_SPACE = 57

# see: https://github.com/torvalds/linux/blob/v5.4/include/uapi/linux/input.h#L252
BUS_USB = 0x03


# see: https://github.com/torvalds/linux/blob/v5.4/include/uapi/linux/input.h#L58
class InputId(Structure):
    _fields_ = [
        ("bustype", c_uint16),
        ("vendor", c_uint16),
        ("product", c_uint16),
        ("version", c_uint16),
    ]


# see: https://github.com/torvalds/linux/blob/v5.4/include/uapi/linux/input.h#L28
class InputEvent(Structure):
    _fields_ = [
        ("time", Timeval),
        ("type", c_uint16),
        ("code", c_uint16),
        ("value", c_int32),
    ]


# see: https://github.com/torvalds/linux/blob/v5.4/include/uapi/linux/uinput.h#L47
UINPUT_MAX_NAME_SIZE = 80

# see: https://github.com/torvalds/linux/blob/v5.4/include/uapi/linux/uinput.h#L63
UINPUT_IOCTL_BASE = ord('U')

UI_DEV_CREATE = IO(UINPUT_IOCTL_BASE, 1)
UI_DEV_DESTROY = IO(UINPUT_IOCTL_BASE, 2)


class UIntputSetup(Structure):
    _fields_ = [
        ("input_id", InputId),
        ("name", c_char * UINPUT_MAX_NAME_SIZE),
        ("ff_effects_max", c_uint32),
    ]


UI_DEV_SETUP = IOW(UINPUT_IOCTL_BASE, 3, UIntputSetup)

# see: https://github.com/torvalds/linux/blob/v5.4/include/uapi/linux/uinput.h#L137
UI_SET_EVBIT = IOW(UINPUT_IOCTL_BASE, 100, c_int)
UI_SET_KEYBIT = IOW(UINPUT_IOCTL_BASE, 101, c_int)
UI_GET_SYSNAME = lambda len: IOC(IOC_READ, UINPUT_IOCTL_BASE, 44, len)
