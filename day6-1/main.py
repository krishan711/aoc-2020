import logging
import time
import math
from typing import List
from typing import Optional
import dataclasses

import click

def run_with_input_file(inputFilePath: str) -> str:
    currentGroup = set()
    answerCount = 0
    with open(inputFilePath, 'r') as inputFile:
        for line in inputFile:
            inputLine = line.strip()
            if not inputLine:
                answerCount += len(currentGroup)
                currentGroup = set()
                print('new', answerCount)
                continue
            currentGroup = currentGroup.union(set(inputLine))
            print('currentGroup', currentGroup)
    answerCount += len(currentGroup)
    return str(answerCount)


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
