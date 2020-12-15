import re
import logging
import time
import math
from typing import Optional
from collections import defaultdict
import dataclasses

import click

def count_instances(minValue: int, maxValue: int, sortedValues: list[int], memory: dict[(int, int, list[int]), int]) -> int:
    logging.debug(f'counting from {minValue}-{maxValue} ({sortedValues})')
    memoKey = (minValue, maxValue, ','.join(str(i) for i in sortedValues))
    if memoKey in memory:
        return memory[memoKey]
    if len(sortedValues) == 0:
        return 1
    potentialValues = []
    for index, value in enumerate(sortedValues):
        if value - minValue > 3:
            break
        potentialValues.append((index, value))
    logging.debug('potentialValues', potentialValues)
    output = 0
    for index, value in potentialValues:
        subOutput = count_instances(minValue=value, maxValue=maxValue, sortedValues=sortedValues[index + 1:], memory=memory)
        logging.debug(f'subOutput for {minValue}-{maxValue} ({sortedValues}): {subOutput}')
        output += subOutput
    memory[memoKey] = output
    return output

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
    sortedValues = sorted(values)
    logging.debug('sortedValues', sortedValues)
    output = count_instances(minValue=0, maxValue=sortedValues[-1] + 3, sortedValues=sortedValues, memory=dict())
    return str(output)

@click.command()
@click.option('-i', '--input-file', 'inputFilePath', required=True, type=str)
@click.option('-v', '--verbose', 'verbose', required=False, is_flag=True, default=False)
def run(inputFilePath: str, verbose: bool):
    logging.basicConfig(level=logging.DEBUG if verbose else logging.INFO)
    startTime = time.time()
    output = run_with_input_file(inputFilePath=inputFilePath)
    logging.info(f'Time taken: {time.time() - startTime}')
    logging.info(output)

if __name__ == '__main__':
    run()
