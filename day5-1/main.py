import logging
import time
import math
from typing import List
from typing import Optional
import dataclasses

import click

def get_seat_from_string(seatString: str)-> (int, int):
    maxRow = 127
    minRow = 0
    maxCol = 7
    minCol = 0
    rowString = seatString[:7]
    colString = seatString[7:]
    for character in rowString:
        if character == 'F':
            maxRow -= math.floor(((maxRow - minRow) / 2) + 1)
        elif character == 'B':
            minRow += math.floor(((maxRow - minRow) / 2) + 1)
        else:
            raise Exception(f'Invalid row character: {character}')
        # print(minRow, maxRow)
    if maxRow != minRow:
        raise Exception(f'Failed to reach single answer for row: {minRow}-{maxRow}')
    for character in colString:
        if character == 'L':
            maxCol -= math.floor(((maxCol - minCol) / 2) + 1)
        elif character == 'R':
            minCol += math.floor(((maxCol - minCol) / 2) + 1)
        else:
            raise Exception(f'Invalid col character: {character}')
        # print(minCol, maxCol)
    if maxCol != minCol:
        raise Exception(f'Failed to reach single answer for col: {minCol}-{maxCol}')
    return (minRow, minCol)

def run_with_input_file(inputFilePath: str) -> str:
    maxSeatId = 0
    with open(inputFilePath, 'r') as inputFile:
        for line in inputFile:
            inputLine = line.strip()
            if not inputLine:
                continue
            seat = get_seat_from_string(inputLine)
            (row, col) = seat
            seatId = row*8 + col
            print(inputLine, seat, seatId)
            maxSeatId = max(maxSeatId, seatId)
    return str(maxSeatId)


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
