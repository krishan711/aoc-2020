import re
import logging
import time
import math
from typing import List
from typing import Optional
from collections import defaultdict
import dataclasses

import click

@dataclasses.dataclass
class Instruction:
    code: str
    value: int

    @classmethod
    def from_string(cls, instructionString):
        instructionStringParts = instructionString.strip().split(' ')
        return Instruction(code=instructionStringParts[0], value=int(instructionStringParts[1]))

def run_with_input_file(inputFilePath: str) -> str:
    instructions = []
    with open(inputFilePath, 'r') as inputFile:
        for line in inputFile:
            inputLine = line.strip()
            if not inputLine:
                continue
            instruction = Instruction.from_string(inputLine)
            instructions.append(instruction)
    accumulator = 0
    index = 0
    visitedIndices = set()
    while True:
        currentInstruction = instructions[index]
        print(index, currentInstruction)
        if index in visitedIndices:
            return str(accumulator)
        visitedIndices.add(index)
        if currentInstruction.code == 'nop':
            index += 1
        elif currentInstruction.code == 'acc':
            accumulator += currentInstruction.value
            index += 1
        elif currentInstruction.code == 'jmp':
            index += currentInstruction.value
    return str(0)


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
