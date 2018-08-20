import bitarray

class FlashCommandRead:
    def __init__(self, flash, address):
        if address > flash.data.length():
            raise Exception('Address too large.')
        self.flash = flash
        self.address = address
        self.flash.out_bit = self.flash.data[address]

    def clock(self, _):
        self.address += 1
        if self.address > self.flash.data.length():
            self.address = 0
        self.flash.out_bit = self.flash.data[self.address]

    def chip_disable(self):
        pass

class FlashCommandWrite:
    def __init__(self, flash, address):
        if address > flash.data.length():
            raise Exception('Address too large.')
        self.flash = flash
        self.address = address
        self.max_bytes = 256
        self.write_buffer = bitarray.bitarray(endian='big')

    def clock(self, in_bit):
        if self.write_buffer.length() / 8 == self.max_bytes:
            raise Exception('Write buffer full.')
        self.write_buffer.append(in_bit)

    def chip_disable(self):
        if self.write_buffer.length() % 8 != 0:
            raise Exception('Write only full bytes.')
        self.flash.write_enable = False

class FlashCommandWriteEnable:
    def __init__(self, flash):
        if flash.write_enable:
            raise Exception('Flash already write enabled.')
        self.flash = flash

    def clock(self, in_bit):
        raise Exception('Did not expect clock during write enable.')

    def chip_disable(self):
        self.flash.write_enable = True

class FlashCommandChipErase:
    def __init__(self, flash):
        if not flash.write_enable:
            raise Exception('Expected write enabled for chip erase.')
        self.flash = flash

    def clock(self, in_bit):
        raise Exception('Did not expect clock during chip erase.')

    def chip_disable(self):
        self.flash.data.setall(True)
        self.flash.write_enable = False

class FlashCommandReadAddress:
    def __init__(self, flash, next_command):
        self.flash = flash
        self.next_command = next_command
        self.address = bitarray.bitarray(endian='big')
        self.target_size = 24

    def clock(self, in_bit):
        if self.address.length() >= self.target_size:
            raise Exception('Did not expect more address bits.')
        self.address.append(in_bit)
        if self.address.length() != self.target_size:
            return None
        return self.next_command(self.flash, int(self.address.to01(), 2))

    def chip_disable(self):
        raise Exception('Did not expect chip disable during address phase.')

class FlashCommandReadOpcode:
    def __init__(self, flash):
        self.flash = flash
        self.opcode = bitarray.bitarray(endian='big')
        self.target_size = 8

    def clock(self, in_bit):
        if self.opcode.length() >= self.target_size:
            raise Exception('Did not expect more opcode bits.')
        self.opcode.append(in_bit)
        if self.opcode.length() != self.target_size:
            return None
        return {
            0x02: lambda f: FlashCommandReadAddress(f, FlashCommandWrite),
            0x03: lambda f: FlashCommandReadAddress(f, FlashCommandRead),
            0x06: FlashCommandWriteEnable,
            0xC7: FlashCommandChipErase
        }[int(self.opcode.to01(), 2)](self.flash)

    def chip_disable(self):
        raise Exception('Did not expect chip disable during opcode phase.')

class Flash:
    def __init__(self, size):
        self.data = bitarray.bitarray('1' * size, endian='big')
        self.reset()

    def reset(self):
        self.write_enable = False
        self.operation = None
        self.in_bit = False
        self.out_bit = False

    def clock(self):
        if not self.operation:
            raise Exception('No current operation.')
        next_operation = self.operation.clock(self.in_bit)
        if next_operation:
            self.operation = next_operation

    def chip_enable(self):
        if self.operation:
            raise Exception('Operation not complete.')
        self.operation = FlashCommandReadOpcode(self)

    def chip_disable(self):
        if not self.operation:
            raise Exception('No current operation.')
        self.operation.chip_disable()
        self.operation = None

    def set_in_bit(self):
        self.in_bit = True

    def clear_in_bit(self):
        self.in_bit = False

    def get_out_bit(self):
        return self.out_bit

f = Flash(4096)

# 0x03 - READ
f.chip_enable()
f.clear_in_bit()
f.clock()
f.clock()
f.clock()
f.clock()
f.clock()
f.clock()
f.set_in_bit()
f.clock()
f.clock()

# 0x00 - Starting at byte 0.
f.clear_in_bit()
f.clock()
f.clock()
f.clock()
f.clock()
f.clock()
f.clock()
f.clock()
f.clock()
f.clock()
f.clock()
f.clock()
f.clock()
f.clock()
f.clock()
f.clock()
f.clock()
f.clock()
f.clock()
f.clock()
f.clock()
f.clock()
f.clock()
f.clock()
f.clock()

# READ THE DATA
f.clock()
