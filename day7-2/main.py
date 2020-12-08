import re
import logging
import time
import math
from typing import List
from typing import Optional
from collections import defaultdict
import dataclasses

import click

def run_with_input_file(inputFilePath: str) -> str:
    rules = dict()
    with open(inputFilePath, 'r') as inputFile:
        for line in inputFile:
            inputLine = line.strip()
            if not inputLine:
                continue
            lineMatch = re.search(r'([a-z ]+) bags contain ([a-z0-9, ]+)', inputLine)
            bagColor = lineMatch.group(1).strip()
            bagContentString = lineMatch.group(2).strip()
            if not bagColor or not bagContentString:
                raise Exception(f'Failed to parse line: {inputLine}')
            bagContentColors = dict()
            if not bagContentString == 'no other bags':
                bagContents = bagContentString.split(', ')
                for bagContent in bagContents:
                    contentMatches = re.match(r'([\d]+) ([a-z ]+) bags?', bagContent)
                    bagContentCount = int(contentMatches.group(1))
                    bagContentColor = contentMatches.group(2)
                    if not bagContentCount or not bagContentColor:
                        raise Exception(f'Failed to parse bag content: {bagContent}')
                    bagContentColors[bagContentColor] = bagContentCount
            rules[bagColor] = bagContentColors
    print('rules', rules)
    totalCounts = {'shiny gold': None}
    while True:
        print('totalCounts', totalCounts)
        remainingColors = set(color for color, count in totalCounts.items() if count is None)
        print('remainingColors', remainingColors)
        if len(remainingColors) == 0:
            break
        for color in remainingColors:
            print('color', color)
            colorRules = rules[color]
            print('colorRules', colorRules)
            if len(colorRules) == 0:
                totalCounts[color] = 0
                continue
            ruleRemainingColors = set(subColor for subColor in colorRules.keys() if totalCounts.get(subColor) is None)
            print('ruleRemainingColors', ruleRemainingColors)
            if len(ruleRemainingColors) == 0:
                colorCount = 0
                for subColor, count in colorRules.items():
                    colorCount += (1 + totalCounts[subColor]) * count
                totalCounts[color] = colorCount
                continue
            for ruleRemainingColor in ruleRemainingColors:
                totalCounts[ruleRemainingColor] = None
    return totalCounts['shiny gold']


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
