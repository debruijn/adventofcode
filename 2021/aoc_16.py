import numpy as np
from collections import Counter

with open('aoc_16_example_data') as f:
    data = f.readlines()

data = [row.replace('\n', '') for row in data]

data = [bin(int(row, 16))[2:].zfill(8) for row in data]
data = ["0" * np.mod((8-np.mod(len(row), 8)), 8) + row for row in data]


class Packet:

    def __init__(self, bits):

        self.subpackets = []
        self.version_bits = bits[0:3]
        self.type_bits = bits[3:6]

        self.version = int(self.version_bits, 2)
        self.type = int(self.type_bits, 2)

        if self.type == 4:
            data_bits = bits[6:]

            last_found = False
            bit_nr = ""
            while not last_found:
                if data_bits[0] == '0':
                    last_found = True
                bit_nr = bit_nr + data_bits[1:5]
                data_bits = data_bits[5:]
            self.data = int(bit_nr, 2)
            self.bits_left = data_bits
        else:
            self.length_type_id = bits[6]
            if self.length_type_id == '1':
                self.nr_subpackets = int(bits[7:18], 2)
                self.subpackets, self.bits_left = self.get_subpackets_1(bits[18:], self.nr_subpackets)
            else:
                self.bit_length = int(bits[7:22], 2)
                self.subpackets = self.get_subpackets(bits[22:22+self.bit_length])
                self.bits_left = bits[22+self.bit_length:]

    def print(self):
        if self.type == 4:
            print(f"Version: {self.version}, type: {self.type}, data: {self.data}")
        else:
            print(f"Version: {self.version}, type: {self.type}, length type: {self.length_type_id} with subpackets: ")
            [x.print() for x in self.subpackets]

    def get_sum_of_version(self):
        return sum([x.get_sum_of_version() for x in self.subpackets]) + self.version

    def get_bits_left(self):
        return self.bits_left

    def get_subpackets(self, bits):

        packets = []
        while not bits == '':
            packet = Packet(bits)
            bits = packet.get_bits_left()
            packets.append(packet)
        return packets

    def get_subpackets_1(self, bits, nr):

        packets = []
        for i in range(nr):
            packet = Packet(bits)
            bits = packet.get_bits_left()
            packets.append(packet)
        return packets, bits

    def get_value(self):
        if self.type == 4:
            return self.data
        elif self.type == 0:
            return sum([x.get_value() for x in self.subpackets])
        elif self.type == 1:
            return np.prod([x.get_value() for x in self.subpackets])
        elif self.type == 2:
            return np.min([x.get_value() for x in self.subpackets])
        elif self.type == 3:
            return np.max([x.get_value() for x in self.subpackets])
        elif self.type == 5:
            return 0 + (self.subpackets[0].get_value() > self.subpackets[1].get_value())
        elif self.type == 6:
            return 0 + (self.subpackets[0].get_value() < self.subpackets[1].get_value())
        elif self.type == 7:
            return 0 + (self.subpackets[0].get_value() == self.subpackets[1].get_value())


for row in data:
    packet = Packet(row)
    # packet.print()
    print(f"Version-sum: {packet.get_sum_of_version()}, value: {packet.get_value()}")
