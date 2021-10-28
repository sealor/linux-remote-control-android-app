#include <stdio.h>
#include <linux/uinput.h>

void main() {
	printf("_IOC_WRITE: %d\n", _IOC_WRITE);

	printf("_IOC_WRITE << _IOC_DIRSHIFT: %d\n", _IOC_WRITE << _IOC_DIRSHIFT);

	printf("_IOC_NRSHIFT: %d\n", _IOC_NRSHIFT);
	printf("_IOC_TYPESHIFT: %d\n", _IOC_TYPESHIFT);
	printf("_IOC_SIZESHIFT: %d\n", _IOC_SIZESHIFT);
	printf("_IOC_DIRSHIFT: %d\n", _IOC_DIRSHIFT);

	printf("UINPUT_IOCTL_BASE: %d\n", UINPUT_IOCTL_BASE);
	printf("UI_SET_EVBIT: %ld\n", UI_SET_EVBIT);

	printf("UI_DEV_SETUP: %ld\n", UI_DEV_SETUP);
	printf("UI_DEV_CREATE: %d\n", UI_DEV_CREATE);
	printf("UI_DEV_DESTROY: %d\n", UI_DEV_DESTROY);
}
/*
$ cc uinput_api_macros.c -o uinput_api_macros.out && ./uinput_api_macros.out
_IOC_WRITE: 1
_IOC_WRITE << _IOC_DIRSHIFT: 1073741824
_IOC_NRSHIFT: 0
_IOC_TYPESHIFT: 8
_IOC_SIZESHIFT: 16
_IOC_DIRSHIFT: 30
UINPUT_IOCTL_BASE: 85
UI_SET_EVBIT: 1074025828
UI_DEV_SETUP: 1079792899
UI_DEV_CREATE: 21761
UI_DEV_DESTROY: 21762
*/