import re
import logging
import time
import math
from typing import Optional
from collections import defaultdict
import dataclasses

import click

def run_with_input_file(inputFilePath: str) -> str:
    with open(inputFilePath, 'r') as inputFile:
        startTime = int(inputFile.readline().strip())
        buses = [int(value) for value in inputFile.readline().strip().split(',') if value != 'x']
    logging.debug(f'startTime: {startTime}')
    logging.debug(f'buses: {buses}')
    waitTimes = [(busId - (startTime % busId)) for busId in buses]
    logging.debug(f'waitTimes: {waitTimes}')
    smallestIndex = waitTimes.index(min(waitTimes))
    output = waitTimes[smallestIndex] * buses[smallestIndex]
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
