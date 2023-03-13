import sys
import time
import click
from rich.live import Live
from rich.table import Table
from rich.text import Text
from rich.console import Console
from rich import print

# функция для живого отображения процесса RLE-кодирования в консоли
def live_rle_encoding(plaintext):
    encoded_text = ""
    console = Console()
    print("RLE encoding process: ")
    # используем rich.live для отображения промежуточных результатов кодирования
    with Live(console=console, auto_refresh=True, refresh_per_second=500000) as live:
        i = 0
        while i < len(plaintext):
            count = 1
            # считаем количество подряд идущих символов
            while i + 1 < len(plaintext) and plaintext[i] == plaintext[i + 1]:
                count += 1
                i += 1
            # если количество подряд идущих символов больше 1, то кодируем их, иначе добавляем символ в закодированный текст
            if count > 1:
                encoded_text += str(count) + plaintext[i]
            else:
                encoded_text += plaintext[i]
            # создаем текст, в котором промежуточный результат кодирования отображается зеленым, а следующая группа символов - красным
            t = f"[green]{encoded_text[:-1]}[/][red]{encoded_text[-1]}[/]{plaintext[i+1:]}"
            live.update(t)
            time.sleep(0.05)
            i += 1
        t = f"[green]{encoded_text}[/]"
        live.update(t)
    return encoded_text


@click.command()
@click.argument('plaintext', required=True)
@click.option('--file', '-f', 'file_mode', default=False, is_flag=True, help='File input mode. If active, it will encode the file passed in the plaintext attribute')
@click.option('--live', '-l', 'live_mode', default=False, is_flag=True, help='Live encoding mode. Displays the encoding process in live mode in the console.')
@click.option('--time', '-t', 'show_time', default=False, is_flag=True, help='Displays the program runtime')
def main(plaintext, file_mode, live_mode, show_time):
    start_time = time.time()
    console = Console()
    encoded_text = ""

    if file_mode:
        plaintext = open(plaintext, "r").read()

    if live_mode:
        encoded_text = live_rle_encoding(plaintext)
    else:
        i = 0
        while i < len(plaintext):
            count = 1
            while i + 1 < len(plaintext) and plaintext[i] == plaintext[i + 1]:
                count += 1
                i += 1
            if count > 1:
                encoded_text += str(count) + plaintext[i]
            else:
                encoded_text += plaintext[i]
            i += 1
        console.print(f'[green]{encoded_text}[/]')
    console.print("Encoding complete!")
    console.print(f"The text size has been reduced by {len(plaintext) - len(encoded_text)} characters")
    duration = time.time() - start_time
    if show_time:
        console.print(f"Execution took: {duration} seconds")


if __name__ == '__main__':
    main()
