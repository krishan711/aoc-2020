import logging
import time
from typing import List
from typing import Optional
import dataclasses

import click


def cast_to_int_or_none(value: str) -> Optional[int]:
    try:
        return int(value)
    except:
        return None


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

    def get_is_byr_valid(self) -> bool:
        if not self.byr:
            return False
        year = cast_to_int_or_none(self.byr)
        return year is not None and year >= 1920 and year <= 2020

    def get_is_iyr_valid(self) -> bool:
        if not self.iyr:
            return False
        year = cast_to_int_or_none(self.iyr)
        return year is not None and year >= 2010 and year <= 2020

    def get_is_eyr_valid(self) -> bool:
        if not self.eyr:
            return False
        year = cast_to_int_or_none(self.eyr)
        return year is not None and year >= 2020 and year <= 2030

    def get_is_hgt_valid(self) -> bool:
        if not self.hgt:
            return False
        if self.hgt.endswith('cm'):
            heightString = self.hgt.replace('cm', '', 1)
            height = cast_to_int_or_none(heightString)
            return height is not None and height >= 150 and height <= 193
        elif self.hgt.endswith('in'):
            heightString = self.hgt.replace('in', '', 1)
            height = cast_to_int_or_none(heightString)
            return height is not None and height >= 59 and height <= 76
        else:
            return False

    def get_is_hcl_valid(self) -> bool:
        if not self.hcl or len(self.hcl) != 7 or not self.hcl.startswith('#'):
            return False
        validCharacters = '0123456789abcdef'
        return all(c in validCharacters for c in self.hcl[1:])

    def get_is_ecl_valid(self) -> bool:
        return self.ecl and self.ecl in {'amb', 'blu', 'brn', 'gry', 'grn', 'hzl', 'oth'}

    def get_is_pid_valid(self) -> bool:
        if not self.pid or len(self.pid) != 9:
            return False
        return cast_to_int_or_none(self.pid) is not None

    def get_is_valid(self) -> bool:
        return bool(self.get_is_byr_valid() and self.get_is_iyr_valid() and self.get_is_eyr_valid() and self.get_is_hgt_valid() and self.get_is_hcl_valid() and self.get_is_ecl_valid() and self.get_is_pid_valid())

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
