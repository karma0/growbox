# -*- coding: utf-8 -*-

"""Relay implementations"""


from growbox.common.enum import Enum
from growbox.common.wire import Wire


class QuadRelayCommands(Enum):
    # commands
    ALL_OFF = 0xA
    ALL_ON = 0xB
    ALL_TOGGLE = 0xC


class QuadRelay(Wire):
    """
    SparkFun's QWIIC quad relay device and corresponding interface.
    """
    address = 0x6D
    jumper_address = 0x6C

    status_offset = 0x05

    relay_addresses = [
        0x01,
        0x02,
        0x03,
        0x04,
    ]

    commands = [
        'on1',
        'on2',
        'on3',
        'on4',

        'off1',
        'off2',
        'off3',
        'off4',

        'toggle1',
        'toggle2',
        'toggle3',
        'toggle4',
    ]

    status = []

    status_results = {
        0: False,
        15: True,
    }

    def all_off(self):
        """Turn off all relays."""
        self.write(QuadRelayCommands.ALL_OFF)

    def all_on(self):
        """Turn on all relays."""
        self.write(QuadRelayCommands.ALL_ON)

    def all_toggle(self):
        """Toggle all relays."""
        self.write(QuadRelayCommands.ALL_TOGGLE)

    def off(self, relay_id):
        if self.status(relay_id):
            self.toggle(relay_id)

    def on(self, relay_id):
        if not self.status(relay_id):
            self.toggle(relay_id)

    def toggle(self, relay_id):
        """Toggle a relay by index starting at 0."""
        self.write(self.relay_addresses[relay_id])

    def get_status_by_id(self, relay_id, retry=3):
        """Check a relay status by index starting at 0."""
        if retry == 0:
            return None

        try:
            return self.status_results[
                self.read(self.status_offset + relay_id)]
        except KeyError:
            return self.get_status_by_id(relay_id, retry=(retry - 1))

    def get_status(self, retry=3):
        """Check all relays status."""
        try:
            return [
                self.status_results[resp] for resp in
                self.read(self.status_offset, len(self.relay_addresses))
            ]
        except KeyError:
            return self.get_status(retry=(retry - 1))

    @property
    def status(self):
        return self.get_status()
