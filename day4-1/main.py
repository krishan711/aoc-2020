import logging
import time
from typing import List
from typing import Optional
import dataclasses

import click

@dataclasses.dataclass
class Passport:
    byr: Optional[str] = None
    iyr: Optional[str] = None
    eyr: Optional[str] = None
    hgt: Optional[str] = None
    hcl: Optional[str] = None
    ecl: Optional[str] = None
    pid: Optional[str] = None
    cid: Optional[str] = None

    def get_is_valid(self) -> bool:
        return bool(self.byr and self.iyr and self.eyr and self.hgt and self.hcl and self.ecl and self.pid)

def run_with_input_file(inputFilePath: str) -> str:
    passports = []
    currentPassport = None
    with open(inputFilePath, 'r') as inputFile:
        for line in inputFile:
            if not line.strip():
                currentPassport = None
            else:
                if not currentPassport:
                    currentPassport = Passport()
                    passports.append(currentPassport)
                entries = line.strip().split(' ')
                for entry in entries:
                    entryParts = entry.split(':')
                    key = entryParts[0]
                    value = entryParts[1]
                    setattr(currentPassport, key, value)
    validCount = 0
    print(len(passports))
    for passport in passports:
        isValid = passport.get_is_valid()
        print(passport, isValid)
        validCount += 1 if isValid else 0
    return str(validCount)


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
