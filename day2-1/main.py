import logging
import time

import click


def run_with_input_file(inputFilePath: str) -> str:
    validCount = 0
    with open(inputFilePath, 'r') as inputFile:
        for line in inputFile:
            if line.strip():
                policyString, password = line.split(': ')
                minMaxString, character = policyString.split(' ')
                minCountString, maxCountString = minMaxString.split('-')
                characterCount = password.count(character)
                if characterCount >= int(minCountString) and characterCount <= int(maxCountString):
                    validCount += 1
    return str(validCount)


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
