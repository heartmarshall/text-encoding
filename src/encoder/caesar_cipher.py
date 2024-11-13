from encoder import SimpleEncoder, EncodeStepResult


class CaesarEncoder(SimpleEncoder):
    def __init__(self, source_text: str, shift: int = 3):
        self.source_text = source_text
        self.shift = shift
        self.encoded_text = ""
        self.current_position = 0
        russian_lower = ''.join(chr(l) for l in range(ord('а'), ord('я')+1))
        russian_upper = ''.join(chr(l) for l in range(ord('А'), ord('Я')+1))
        english_lower = ''.join(chr(l) for l in range(ord('a'), ord('z')+1))
        english_upper = ''.join(chr(l) for l in range(ord('A'), ord('Z')+1))

        self._caesar_table = {}
        for alphabet in [russian_lower, russian_upper, english_lower, english_upper]:
            self._caesar_table.update(
                {sym: alphabet[(i + self.shift) % len(alphabet)] for i, sym in enumerate(alphabet)})

    def encode_step(self) -> EncodeStepResult:
        if self.current_position >= len(self.source_text):
            return EncodeStepResult("", "", True)

        current_char = self.source_text[self.current_position]
        encoded_char = self._caesar_table.get(current_char, current_char)
        self.encoded_text += encoded_char
        self.current_position += 1
        return EncodeStepResult(current_char, encoded_char)

    def add_alphabet(self, alphabet: str) -> None:
        self._caesar_table.update(
            {sym: alphabet[(i + self.shift) % len(alphabet)] for i, sym in enumerate(alphabet)})