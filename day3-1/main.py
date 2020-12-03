import logging
import time

import click


def run_with_input_file(inputFilePath: str) -> str:
    stepsX = 3
    stepsY = 1
    grid = []
    with open(inputFilePath, 'r') as inputFile:
        for line in inputFile:
            if line.strip():
                grid.append(list(line.strip()))
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
    return str(hitCount)


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
