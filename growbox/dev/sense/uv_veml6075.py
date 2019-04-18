# -*- coding: utf-8 -*-

"""Relay implementations"""


from growbox.wire import Wire


class QuadRelay(Wire):
    """
    SparkFun's QWIIC quad relay device and corresponding interface.
    """
    address = 0x6D
    jumper_address = 0x6C

    status_offset = 0x05

    # commands
    turn_all_off = 0xA
    turn_all_on = 0xB
    toggle_all = 0xC

    status_results = {
        0: False,
        15: True,
    }

    relay_addresses = [
        0x01,
        0x02,
        0x03,
        0x04,
    ]

    def all_off(self):
        """Turn off all relays."""
        self.write(self.turn_all_off)

    def all_on(self):
        """Turn on all relays."""
        self.write(self.turn_all_on)

    def all_toggle(self):
        """Toggle all relays."""
        self.write(self.toggle_all)

    def toggle(self, relay_id):
        """Toggle a relay by index starting at 0."""
        self.write(self.relay_addresses[relay_id])

    def status(self, relay_id):
        """Check a relay status by index starting at 0."""
        return self.status_results[
            self.read(self.status_offset + relay_id)]

    def all_status(self):
        """Check all relays status."""
        return [
            self.status_results[resp] for resp in
            self.read(self.status_offset, len(self.relay_addresses))
        ]


class Relay:
    pass
