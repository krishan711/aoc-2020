import sys
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
        rules = [(index, int(value)) for index, value in enumerate(inputFile.readline().strip().split(',')) if value != 'x']
    logging.debug(f'rules: {rules}')
    ruleKeys = [a for a,b in rules]
    for (offest, busId) in rules:
        if busId in ruleKeys:
            print('HERE:', busId)
    rules = sorted(rules, key=lambda tup: -tup[1])
    (i, a) = rules[0]
    rules = rules[1:]
    logging.debug(f'rules: {rules}')
    logging.debug(f'(i, a): {(i, a)}')
    # t*a, t*a + 1 = y*b, t*a + 2 = w*c, t*a + 3 = v*d
    for t in range(sys.maxsize):
        v = t * a - i
        print(v)
        if all((v + offset) % busId == 0 for offset, busId in rules):
            return str(v)
    output = -1
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
