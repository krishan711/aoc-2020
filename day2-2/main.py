import logging
import time

import click


def run_with_input_file(inputFilePath: str) -> str:
    validCount = 0
    with open(inputFilePath, 'r') as inputFile:
        for line in inputFile:
            if line.strip():
                policyString, password = line.split(': ')
                positionString, character = policyString.split(' ')
                positionString1, positionString2 = positionString.split('-')
                matchesFirst = password[int(positionString1) - 1] == character
                matchesSecond = password[int(positionString2) - 1] == character
                if (matchesFirst and not matchesSecond) or (not matchesFirst and matchesSecond):
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
