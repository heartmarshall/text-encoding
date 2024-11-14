from abc import ABC, abstractmethod


class EncodeStepResult:
    def __init__(self, source_symbols: str, encoded_symbols: str, is_end=False):
        self.source_symbols = source_symbols
        self.encoded_symbols = encoded_symbols
        self.is_end = is_end

    def __eq__(self, other):
        if not isinstance(other, EncodeStepResult):
            return False
        return (self.source_symbols == other.source_symbols and
                self.encoded_symbols == other.encoded_symbols and
                self.is_end == other.is_end)
    

class Encoder(ABC):
    @abstractmethod
    def set_source_text(self, text: str):
        """Sets the source text for encoding"""
        pass

    @abstractmethod
    def refresh(self):
        """Resets the encoder's state, clearing the encoded text and resetting position."""
        pass

    @abstractmethod
    def encode_step(self) -> EncodeStepResult:
        """Processes the next fragment to get a character in the new encoding"""
        pass

    @abstractmethod
    def get_current_position(self):
        """Returns the current position in the source text"""
        pass

    @abstractmethod
    def get_encoded_text(self):
        """Returns the processed (encoded) text"""
        pass

    @abstractmethod
    def get_encoded_text(self):
        pass

class SimpleEncoder(Encoder):
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

    def get_encoded_text(self):
        return self.encoded_text
        
    def encode_step(self):
        if self.current_position >= len(self.source_text):
            return EncodeStepResult("", "", True)
        
        step_result = EncodeStepResult(self.source_text[self.current_position], self.source_text[self.current_position])
        self.encoded_text += self.source_text[self.current_position]
        self.current_position += 1
        return step_result
    
    def encode_to_end(self):
        while not self.encode_step().is_end:
            continue