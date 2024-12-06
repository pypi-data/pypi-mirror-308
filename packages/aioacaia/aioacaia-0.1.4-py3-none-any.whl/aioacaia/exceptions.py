"""Exceptions for aioacaia."""

from bleak.exc import BleakDeviceNotFoundError, BleakError


class AcaiaScaleException(Exception):
    """Base class for exceptions in this module."""


class AcaiaDeviceNotFound(BleakDeviceNotFoundError):
    """Exception when no device is found."""


class AcaiaError(BleakError):
    """Exception for general bleak errors."""


class AcaiaUnknownDevice(Exception):
    """Exception for unknown devices."""
