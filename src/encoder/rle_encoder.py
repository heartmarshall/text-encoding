from encoder import Encoder, EncodeStepResult

class RLEEncoder(Encoder):
    def __init__(self, source_text: str):
        super().__init__()
        self.source_text = source_text
        self.encoded_text = ""
        self.current_position = 0

    def set_source_text(self, text: str):
        self.source_text = text
        self.refresh()

    def refresh(self):
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
        count = 1
        
        while (self.current_position + count < len(self.source_text) and 
               self.source_text[self.current_position + count] == current_char):
            count += 1
        
        encoded_fragment = f"{count}{current_char}"
        self.encoded_text += encoded_fragment
        self.current_position += count
        
        return EncodeStepResult(current_char * count, encoded_fragment)