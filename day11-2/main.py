import re
import logging
import time
import math
from typing import Optional
from collections import defaultdict
import dataclasses

import click

def print_grid(grid: list[list[str]]) -> None:
    logging.debug('-'*len(grid[0]))
    for row in grid:
        logging.debug(''.join(row))
    logging.debug('-'*len(grid[0]))

def grid_to_string(grid: list[list[str]]) -> None:
    s = '-' * len(grid[0])
    for row in grid:
        s += ''.join(row)
    s += '-'*len(grid[0])
    return s

def run_with_input_file(inputFilePath: str) -> str:
    grid = []
    with open(inputFilePath, 'r') as inputFile:
        for line in inputFile:
            inputLine = line.strip()
            if not inputLine:
                continue
            values = list(inputLine)
            grid.append(values)
    print_grid(grid)
    nextGrid = [list(row) for row in grid]
    while True:
        for rowIndex in range(len(grid)):
            for colIndex in range(len(grid[rowIndex])):
                value = grid[rowIndex][colIndex]
                indicesToCheck = [(-1, -1), (-1, 0), (-1, +1), (0, +1), (+1, +1), (+1, 0), (+1, -1), (0, -1)]
                if value == '.':
                    continue
                elif value == 'L':
                    shouldOccupy = True
                    for (r, c) in indicesToCheck:
                        newR = rowIndex
                        newC = colIndex
                        while True:
                            newR += r
                            newC += c
                            if newR < 0 or newC < 0 or newR >= len(grid) or newC >= len(grid[newR]):
                                break
                            if grid[newR][newC] == '.':
                                continue
                            shouldOccupy = grid[newR][newC] != '#'
                            break
                        if not shouldOccupy:
                            break
                    if shouldOccupy:
                        nextGrid[rowIndex][colIndex] = '#'
                elif value == '#':
                    visibleCount = 0
                    for (r, c) in indicesToCheck:
                        newR = rowIndex
                        newC = colIndex
                        while True:
                            newR += r
                            newC += c
                            if newR < 0 or newC < 0 or newR >= len(grid) or newC >= len(grid[newR]):
                                break
                            if grid[newR][newC] == '.':
                                continue
                            visibleCount += grid[newR][newC] == '#'
                            break
                        if visibleCount >= 5:
                            break
                    if visibleCount >= 5:
                        nextGrid[rowIndex][colIndex] = 'L'
                    # if sum(1 if grid[rowIndex + r][colIndex + c] == '#' else 0 for (r, c) in indicesToCheck if rowIndex + r >=0 and colIndex + c >=0 and rowIndex + r < len(grid) and colIndex + c < len(grid[rowIndex + r])) >= 4:
                    #     nextGrid[rowIndex][colIndex] = 'L'
                logging.debug(f'({rowIndex}, {colIndex}): {grid[rowIndex][colIndex]} -> {nextGrid[rowIndex][colIndex]}')
        print_grid(nextGrid)
        if grid_to_string(grid) == grid_to_string(nextGrid):
            break
        grid = [list(row) for row in nextGrid]
    output = grid_to_string(nextGrid).count('#')
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
