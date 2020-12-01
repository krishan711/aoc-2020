import logging
import time

import click


def run_with_input_file(inputFilePath: str) -> str:
    numbers = []
    with open(inputFilePath, 'r') as inputFile:
        for line in inputFile:
            if line.strip():
                numbers.append(int(line.strip()))
    for index, number in enumerate(numbers):
        for number2 in numbers[index + 1:]:
            if number + number2 == 2020:
                return str(number * number2)
    return ''


@click.command()
@click.option('-i', '--input-file', 'inputFilePath', required=True, type=str)
@click.option('-v', '--verbose', 'verbose', required=False, is_flag=True, default=False)
def run(inputFilePath: str, verbose: bool):
    logging.basicConfig(level=logging.DEBUG if verbose else logging.INFO)
    startTime = time.time()
    output = run_with_input_file(inputFilePath=inputFilePath)
    print(f'Time taken: {time.time() - startTime}')
    print(output)

if __name__ == '__main__':
    run()
