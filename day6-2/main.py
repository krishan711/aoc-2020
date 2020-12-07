import logging
import time
import math
from typing import List
from typing import Optional
from collections import defaultdict
import dataclasses

import click

def run_with_input_file(inputFilePath: str) -> str:
    currentGroup = defaultdict(int)
    currentGroupSize = 0
    groups = []
    with open(inputFilePath, 'r') as inputFile:
        for line in inputFile:
            inputLine = line.strip()
            if not inputLine:
                if currentGroupSize > 0:
                    groups.append((dict(currentGroup), currentGroupSize))
                currentGroup = defaultdict(int)
                currentGroupSize = 0
                continue
            for character in set(inputLine):
                currentGroup[character] += 1
            currentGroupSize += 1
    if currentGroupSize > 0:
        groups.append((dict(currentGroup), currentGroupSize))
    print('groups', groups)
    memberCount = 0
    for group, size in groups:
        memberCount += list(group.values()).count(size)
        print('memberCount', memberCount)
    return str(memberCount)


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
