import re
import logging
import time
import math
from typing import Optional
from collections import defaultdict
import dataclasses

import click

def run_with_input_file(inputFilePath: str) -> str:
    allDirections = [(1, 0), (0, -1), (-1, 0), (0, 1)]
    direction = (1, 0)
    position = (0, 0)
    with open(inputFilePath, 'r') as inputFile:
        for line in inputFile:
            inputLine = line.strip()
            if not inputLine:
                continue
            command = inputLine[0]
            value = int(inputLine[1:])
            logging.debug(f'cmd: {command} val: {value}')
            if command == 'N':
                position = (position[0] + 0, position[1] + value)
            if command == 'S':
                position = (position[0] + 0, position[1] - value)
            if command == 'E':
                position = (position[0] + value, position[1] + 0)
            if command == 'W':
                position = (position[0] - value, position[1] + 0)
            if command == 'L':
                if value % 90 != 0:
                    raise Exception()
                direction = allDirections[(allDirections.index(direction) - int(value / 90)) % len(allDirections)]
            if command == 'R':
                if value % 90 != 0:
                    raise Exception()
                direction = allDirections[(allDirections.index(direction) + int(value / 90)) % len(allDirections)]
            if command == 'F':
                position = (position[0] + direction[0] * value, position[1] + direction[1] * value)
            logging.debug(f'new pos: {position} dir: {direction}')
    return str(abs(position[0]) + abs(position[1]))

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
