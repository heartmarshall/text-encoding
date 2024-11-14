from encoder.encoder import SimpleEncoder, EncodeStepResult

SINGLE_SEQUENCE = 0x00
REPEATED_SEQUENCE = 0x80

class RLEEncoder(SimpleEncoder):
    def __init__(self, source_data: bytearray):
        self.source_data = source_data
        self.encoded_data = bytearray()
        self.current_position = 0

    def encode_step(self) -> EncodeStepResult:
        if self.current_position >= len(self.source_data):
            return EncodeStepResult(bytes(), bytes(), True)

        start_pos = self.current_position
        current_byte = self.source_data[start_pos]
        count = 1
        is_repeated = True

        for i in range(start_pos + 1, min(start_pos + 128, len(self.source_data))):
            if self.source_data[i] == current_byte and is_repeated:
                count += 1
            else:
                if count == 1:
                    is_repeated = False
                break

        if is_repeated:
            length_byte = (REPEATED_SEQUENCE | (count - 2))
            encoded_fragment = bytes([length_byte, current_byte])
        else:
            count = 1
            while (self.current_position + count < len(self.source_data) and 
                   count < 128 and
                   (self.source_data[self.current_position + count] != 
                    self.source_data[self.current_position + count - 1])):
                count += 1
            length_byte = (SINGLE_SEQUENCE | (count - 1))
            encoded_fragment = bytes([length_byte]) + self.source_data[self.current_position:self.current_position + count]

        self.encoded_data.extend(encoded_fragment)
        self.current_position += count

        return EncodeStepResult(self.source_data[start_pos:start_pos + count], encoded_fragment, self.current_position >= len(self.source_data))
