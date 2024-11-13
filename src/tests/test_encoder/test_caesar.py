import pytest
from encoder.caesar_cipher import CaesarEncoder
from encoder.encoder import EncodeStepResult

@pytest.fixture
def encoder():
    return CaesarEncoder("")

def test_empty(encoder):
    text = ""
    encoder = CaesarEncoder(text)
    encoder.encode_to_end()
    assert encoder.encoded_text == ""
    assert encoder.current_position == 0

def test_encoding_with_shift(encoder):
    text = "abc XYZ"
    expected_output = "def ABC"
    encoder = CaesarEncoder(text, shift=3)
    encoder.encode_to_end()
    assert encoder.encoded_text == expected_output

def test_encoding_with_custom_shift(encoder):
    text = "абв АБВ"
    expected_output = "вгд ВГД"
    encoder = CaesarEncoder(text, shift=2)
    encoder.encode_to_end()
    assert encoder.encoded_text == expected_output

def test_non_alphabetic_characters(encoder):
    text = "a b!@#"
    expected_output = "d e!@#"
    encoder = CaesarEncoder(text, shift=3)
    encoder.encode_to_end()
    assert encoder.encoded_text == expected_output

def test_encode_step(encoder):
    text = "abc"
    encoder = CaesarEncoder(text, shift=1)
    step1 = encoder.encode_step()
    step2 = encoder.encode_step()
    step3 = encoder.encode_step()
    end_step = encoder.encode_step()

    assert step1 == EncodeStepResult("a", "b")
    assert step2 == EncodeStepResult("b", "c")
    assert step3 == EncodeStepResult("c", "d")
    assert end_step == EncodeStepResult("", "", True)

def test_encode_to_end(encoder):
    text = "xyz"
    expected_output = "abc"
    encoder = CaesarEncoder(text, shift=3)
    encoder.encode_to_end()
    assert encoder.encoded_text == expected_output
    assert encoder.current_position == len(text)

def test_add_alphabet(encoder):
    text = "abc 123"
    expected_output = "def 456"
    encoder = CaesarEncoder(text, shift=3)

    new_alphabet = "0123456789"
    encoder.add_alphabet(new_alphabet)

    encoder.encode_to_end()
    assert encoder.encoded_text == expected_output
