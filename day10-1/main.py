import re
import logging
import time
import math
from typing import List
from typing import Optional
from collections import defaultdict
import dataclasses

import click

def run_with_input_file(inputFilePath: str) -> str:
    values = []
    target = None
    with open(inputFilePath, 'r') as inputFile:
        for line in inputFile:
            inputLine = line.strip()
            if not inputLine:
                continue
            value = int(inputLine)
            values.append(value)
    print('values', values)
    sortedValues = sorted(values)
    print('sortedValues', sortedValues)
    currentValue = 0
    diffs = defaultdict(int)
    for value in sortedValues:
        diffs[value - currentValue] += 1
        currentValue = value
    diffs[3] += 1
    print('diffs', diffs)
    return str(diffs[1] * diffs[3])

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
