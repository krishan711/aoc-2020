import re
import logging
import time
import math
from typing import List
from typing import Optional
from collections import defaultdict
import dataclasses

import click

@dataclasses.dataclass(frozen=True)
class Instruction:
    code: str
    value: int

    @classmethod
    def from_string(cls, instructionString):
        instructionStringParts = instructionString.strip().split(' ')
        return Instruction(code=instructionStringParts[0], value=int(instructionStringParts[1]))

def switch_instruction_at_index(instructions: List[Instruction], index: int) -> List[Instruction]:
    instructionsCopy = [instruction for instruction in instructions]
    instructionToChange = instructionsCopy[index]
    if instructionToChange.code == 'jmp':
        instructionsCopy[index] = Instruction(code='nop', value=instructionToChange.value)
    elif instructionToChange.code == 'nop':
        instructionsCopy[index] = Instruction(code='jmp', value=instructionToChange.value)
    else:
        raise Exception('Cannot change this instruction!')
    return instructionsCopy

def run_instructions(instructions: List[Instruction]) -> int:
    accumulator = 0
    index = 0
    visitedIndices = set()
    while True:
        if index >= len(instructions):
            return accumulator
        currentInstruction = instructions[index]
        if index in visitedIndices:
            raise Exception(f'Repeated instruction at index: {index}')
        visitedIndices.add(index)
        if currentInstruction.code == 'nop':
            index += 1
        elif currentInstruction.code == 'acc':
            accumulator += currentInstruction.value
            index += 1
        elif currentInstruction.code == 'jmp':
            index += currentInstruction.value
    return accumulator

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
    instructionsCopy = instructions
    currentCopyIndex = -1
    while True:
        print(f'running with changed index: {currentCopyIndex}')
        try:
            accumulator = run_instructions(instructions=instructionsCopy)
            break
        except Exception as exception:
            print(f'Failed: {str(exception)}')
            while True:
                currentCopyIndex += 1
                if instructions[currentCopyIndex].code in {'jmp', 'nop'}:
                    instructionsCopy = switch_instruction_at_index(instructions=instructions, index=currentCopyIndex)
                    break
    return str(accumulator)

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
