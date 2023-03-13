import sys
import time
import click
from rich.live import Live
from rich.table import Table
from rich.text import Text
from rich.console import Console
from rich import print

# декоратор для замера времени выполнения функции
def timer(text):
    def decorator(func):
        def wrapper(*args, **kwargs):
            start_time = time.time()
            result = func(*args, **kwargs)
            end_time = time.time()
            duration = end_time - start_time
            print(f"{text} {duration} seconds")
            return result
        return wrapper
    return decorator

# генерация таблицы шифрования для шифра Цезаря с заданным сдвигом
def generate_caesar_table(shift: int) -> dict:
    russian_lower = ''.join(chr(l) for l in range(ord('а'), ord('я')+1))
    russian_upper = ''.join(chr(l) for l in range(ord('А'), ord('Я')+1))
    english_lower = ''.join(chr(l) for l in range(ord('a'), ord('z')+1))
    english_upper = ''.join(chr(l) for l in range(ord('A'), ord('Z')+1))

    caesar_table = {}
    for alphabet in [russian_lower, russian_upper, english_lower, english_upper]:
        caesar_table.update({sym: alphabet[(i + shift) % len(alphabet)] for i, sym in enumerate(alphabet)})
    return caesar_table

# шифрование текста с использованием таблицы шифрования
def caesar_cipher_text(text: str, table: dict):
    ciphertext = ""
    for letter in text:
        if letter in table:
            ciphertext += table[letter]
        else:
            ciphertext += letter
    return ciphertext

# функция для живого отображения процесса шифрования в консоли
def live_encoding(plaintext, table):
    encoded_text = ""
    console = Console()
    print("Encoding process: ")
    # используем rich.live для отображения промежуточных результатов шифрования
    with Live(console=console, auto_refresh=True, refresh_per_second=500000) as live:
        for i in range(len(plaintext)):
            encoded_text += caesar_cipher_text(plaintext[i], table)
            # создаем текст, в котором промежуточный результат шифрования отображается зеленым, а следующая буква - красным
            t = f"[green]{encoded_text[:-1]}[/][red]{encoded_text[-1]}[/]{plaintext[i+1:]}"
            live.update(t)
            time.sleep(0.05)
        t = f"[green]{encoded_text}[/]"
        live.update(t)


@click.command()
@click.argument('plaintext', required=True)
@click.option('--base', '-b', default=4, help='The base of the Caesar cipher.')
@click.option('--file', '-f', 'file_mode', default=False, is_flag=True, help='File input mode. If active, it will encode the file passed in the plaintext attribute')
@click.option('--live', '-l', 'live_mode', default=False, is_flag=True, help='Live encoding mode. Displays the encoding process in live mode in the console.')
@click.option('--time', '-t', 'show_time', default=False, is_flag=True, help='Displays the program runtime')
def main(plaintext, base, file_mode, live_mode, show_time):
    start_time = time.time()
    console = Console()
    caesar_table = generate_caesar_table(base)

    if file_mode:
        plaintext = open(plaintext, "r").read()

    if live_mode:
        live_encoding(plaintext, caesar_table)
    else:
        console.print(f'[green]{caesar_cipher_text(plaintext, caesar_table)}[/]')
    console.print("Encoding complete!")
    duration = time.time() - start_time
    if show_time:
        console.print(f"Execution took: {duration} seconds")
    
if __name__ == '__main__':
    main()
