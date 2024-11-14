import pytest
from encoder.encoder import EncodeStepResult
from rle_encoder import RLEEncoder

def test_rle_encoder_repeated_sequence():
    source_data = "00000000"
    encoder = RLEEncoder(source_data)
    
    result = encoder.encode_step()
    
    # Должен создать сжатую последовательность повторяющихся байтов
    assert result.encoded == bytes([0b10000110, 0x00])  # [1|6] с 0
    assert result.finished

def test_rle_encoder_single_sequence():
    # Проверяем последовательность без повторяющихся элементов
    source_data = "123456"
    encoder = RLEEncoder(source_data)
    
    result = encoder.encode_step()
    
    # Ожидается, что все элементы будут считаться одиночными
    assert result.encoded == bytes([0b00000101, 0x31, 0x32, 0x33, 0x34, 0x35, 0x36])  # [0|5] с байтами 1, 2, 3, 4, 5, 6
    assert result.finished

def test_rle_encoder_mixed_sequence():
    # Проверяем смесь одиночных и повторяющихся элементов
    source_data = "00004444808080800202FFFFFFFF00"
    encoder = RLEEncoder(source_data)

    expected_results = [
        bytes([0b10000100, 0x00]),                      # [1|4] с 0
        bytes([0b00000010, 0x34, 0x32, 0x30]),          # [0|2] с байтами 4, 2, 0
        bytes([0b10000101, 0x34]),                      # [1|5] с 4
        bytes([0b10000010, 0x50]),                      # [1|2] с 80
        bytes([0b00000000, 0x00]),                      # [0|0] с байтом 0
        bytes([0b10000010, 0x32]),                      # [1|2] с 2
        bytes([0b10000011, 0xFF]),                      # [1|3] с 255
        bytes([0b10000000, 0x00]),                      # [1|0] с 0
    ]

    for expected in expected_results:
        result = encoder.encode_step()
        assert result.encoded == expected
        assert not result.finished if expected != expected_results[-1] else result.finished

def test_rle_encoder_empty_input():
    # Проверка пустой строки
    source_data = ""
    encoder = RLEEncoder(source_data)
    
    result = encoder.encode_step()
    
    # Ожидаем пустой результат, сразу завершенный
    assert result.encoded == bytes()
    assert result.finished

def test_rle_encoder_short_repeated():
    # Проверяем последовательность из двух повторяющихся элементов
    source_data = "AA"
    encoder = RLEEncoder(source_data)
    
    result = encoder.encode_step()
    
    # Ожидается [1|0] с байтом 'A' (0x41)
    assert result.encoded == bytes([0b10000000, 0x41])
    assert result.finished

def test_rle_encoder_long_single_sequence():
    # Проверяем длинную последовательность одиночных элементов
    source_data = "1234567890" * 12  # Строка длиной 120 символов
    encoder = RLEEncoder(source_data)

    # Результат должен быть в виде нескольких шагов, каждый не более 128 элементов
    steps = []
    while True:
        result = encoder.encode_step()
        steps.append(result.encoded)
        if result.finished:
            break

    assert len(steps) == 1
    assert steps[0][:1] == bytes([0b00011111])  # [0|31] (120 элементов в одном блоке одиночных)
    assert result.finished
