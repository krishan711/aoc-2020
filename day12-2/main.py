import re
import logging
import time
import math
from typing import Optional
from collections import defaultdict
import dataclasses

import click

def run_with_input_file(inputFilePath: str) -> str:
    position = (0, 0)
    waypointPosition = (10, 1)
    with open(inputFilePath, 'r') as inputFile:
        for line in inputFile:
            inputLine = line.strip()
            if not inputLine:
                continue
            command = inputLine[0]
            value = int(inputLine[1:])
            logging.debug(f'cmd: {command} val: {value}')
            if command == 'N':
                waypointPosition = (waypointPosition[0] + 0, waypointPosition[1] + value)
            if command == 'S':
                waypointPosition = (waypointPosition[0] + 0, waypointPosition[1] - value)
            if command == 'E':
                waypointPosition = (waypointPosition[0] + value, waypointPosition[1] + 0)
            if command == 'W':
                waypointPosition = (waypointPosition[0] - value, waypointPosition[1] + 0)
            if command == 'L':
                if value % 90 != 0:
                    raise Exception()
                for turn in range(int(value / 90)):
                    waypointPosition = (- waypointPosition[1], waypointPosition[0])
            if command == 'R':
                if value % 90 != 0:
                    raise Exception()
                for turn in range(int(value / 90)):
                    waypointPosition = (waypointPosition[1], - waypointPosition[0])
            if command == 'F':
                position = (position[0] + waypointPosition[0] * value, position[1] + waypointPosition[1] * value)
            logging.debug(f'new pos: {position} wpos: {waypointPosition}')
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
