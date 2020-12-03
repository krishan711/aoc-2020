import logging
import time
from typing import List

import click

def run_with_input(grid: List[List[str]], stepsX: int, stepsY: int):
    gridHeight = len(grid)
    gridWidth = len(grid[0])
    currentX = 0
    currentY = 0
    hitCount = 0
    while currentY + stepsY < gridHeight:
        currentX = (currentX + stepsX) % gridWidth
        currentY = currentY + stepsY
        isHit = grid[currentY][currentX] == '#'
        print(currentX, currentY, isHit)
        hitCount += 1 if isHit else 0
    return hitCount


def run_with_input_file(inputFilePath: str) -> str:
    grid = []
    with open(inputFilePath, 'r') as inputFile:
        for line in inputFile:
            if line.strip():
                grid.append(list(line.strip()))
    output = 1
    for (stepsX, stepsY) in [(1,1), (3,1), (5,1), (7,1), (1,2)]:
        currentOutput = run_with_input(grid, stepsX, stepsY)
        print(stepsX, stepsY, currentOutput)
        output *= currentOutput
    return str(output)


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
