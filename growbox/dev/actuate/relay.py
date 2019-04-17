# -*- coding: utf-8 -*-

"""Relay implementations"""


from growbox.wire import Wire


class Relay:


class QuadRelay(Wire):
    address = 0x60

    status_offset = 0x05

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

    def toggle_all(self):
        self.write(
    def toggle(self, relay_id):
        self.write(self.relay_addresses[relay_id]

    def get_status(self, relay_id):
        return self.status_results[
            self.request_response(self.status_offset + relay_id)]

    def get_relays_status(self):
        return [
            self.status_results[resp] for resp in
            self.request_response(self.status_offset, len(self.relay_addresses))
        ]

