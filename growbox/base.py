# -*- coding: utf-8 -*-

"""Generic base interface for working with devices"""


def _name(key):
    return ':'.split(key)[0]


def _display(key):
    return ':'.split(key)[1]


class DeviceBase:
    display = []
    monitor = []
    commands = []

    command_overrides = {}

    def __init__(self, device, serial_interface=None, bus=None, port=1,
                 address=None, addr_jump=False, **kwargs):
        self.device = device(serial_interface=serial_interface, bus=bus,
                             port=port, address=address, addr_jump=addr_jump,
                             **kwargs)

    def override_command(self, command, name):
        """
        Cosmetic function to rename a device's actions (commands) by name.
        """
        self.command_overrides[command] = name

    def begin(self):
        """Setup the device and its applications"""
        self.device.begin()

        # If the device has commands and we don't, bring them up to self
        if not self.commands and self.device.commands:
            self.commands = self.device.commands

        self.update()  # First run to initialize devices

    def update(self):
        """
        Override this to execute updates on the main application loop.
        """
        pass

    def shutdown(self):
        """
        Override this to perform cleanup for your system or its devices.
        """
        pass

    def get_display(self):
        """
        Returns a list of attributes to display from a device.
        """
        return {
            _display(key): getattr(self, _name(key),
                                   getattr(self.device, _name(key)))
            for key in self.monitor
        }

    def get_monitor(self):
        """
        Returns a list of attributes to monitor from a device.
        """
        return {
            key: getattr(self, key, getattr(self.device, key))
            for key in self.monitor
        }

    def act(self, command, *args, **kwargs):
        """
        Performs an action on a device.  Use override_command to rename a
        command to a more useful name.
        """
        # Resolve overriden names first
        if command in self.command_overrides:
            command = self.command_overrides[command]

        # TODO: Generate a function call from command name
        cmd = getattr(self, command, getattr(self.device, command, None))
        return cmd(*args, **kwargs)
