from encoder import Encoder, EncodeStepResult

class CaesarEncoder(Encoder):
    def __init__(self, source_text: str, shift: int = 3):
        super().__init__()
        self.source_text = source_text
        self.shift = shift
        self.encoded_text = ""
        self.current_position = 0

    def set_source_text(self, text: str):
        self.source_text = text
        self.refresh()

    def refresh(self):
        """Resets the encoder's state, clearing the encoded text and resetting position."""
        self.encoded_text = ""
        self.current_position = 0

    def get_current_position(self):
        return self.current_position

    def get_processed_text(self):
        return self.encoded_text

    def encode_step(self) -> EncodeStepResult:
        if self.current_position >= len(self.source_text):
            return EncodeStepResult("", "", True)
        
        current_char = self.source_text[self.current_position]
        
        if current_char.isalpha():
            shift_base = 65 if current_char.isupper() else 97
            encoded_char = chr((ord(current_char) - shift_base + self.shift) % 26 + shift_base)
        else:
            encoded_char = current_char
        
        self.encoded_text += encoded_char
        self.current_position += 1
        return EncodeStepResult(current_char, encoded_char)