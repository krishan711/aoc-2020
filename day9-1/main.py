import re
import logging
import time
import math
from typing import List
from typing import Optional
from collections import defaultdict
import dataclasses

import click

def is_valid(value: int, precedingValues: List[int]) -> bool:
    sortedValues = sorted(precedingValues)
    print(f'is_valid: {value} {sortedValues}')
    for index, subValue in enumerate(sortedValues):
        if subValue > value / 2:
            return False
        if value - subValue in sortedValues[index + 1:]:
            return True
    return False

def run_with_input_file(inputFilePath: str) -> str:
    preambleSize = 25
    values = []
    with open(inputFilePath, 'r') as inputFile:
        for line in inputFile:
            inputLine = line.strip()
            if not inputLine:
                continue
            value = int(inputLine)
            if len(values) >= preambleSize and not is_valid(value=value, precedingValues=values[len(values) - preambleSize:len(values)]):
                return str(value)
            values.append(value)
    return str(-1)

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
