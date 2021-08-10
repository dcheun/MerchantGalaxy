#!/usr/bin/env python

"""app.py - Merchant's Guide to the Galaxy

This application is a smart calculator for helping space merchants calculate and convert
between intergalactic units and roman numerals.

"""

import re

__author__ = "Danny Cheun"
__credits__ = ["Danny Cheun"]
__version__ = "1.0.0"
__maintainer__ = "Danny Cheun"
__email__ = "dcheun@gmail.com"


# Globals
# Maps roman numeral to int.
roman = {
    'I': 1,
    'V': 5,
    'X': 10,
    'L': 50,
    'C': 100,
    'D': 500,
    'M': 1000,
    'IV': 4,
    'IX': 9,
    'XL': 40,
    'XC': 90,
    'CD': 400,
    'CM': 900
}

# To store and map between intergalactic units to roman numeral equivalent.
i_units = {}

# To store intergalactic unit multiplier and its value.
i_mult = {}


def units_to_rn(arr):
    """Converts from galactic units to roman numeral string.
    
    :param arr: A list containing galactic units as strings.
    :return: roman numeral string.
    """
    s = ''
    for i in arr:
        s += i_units.get(i,'')
    return s


def rn_to_int(s):
    """Converts roman numeral string to integer.
    
    :param s: String containing roman numeral
    :return: The integer equivalent.
    """
    i = 0
    num = 0
    while i < len(s):
        if i+1 < len(s) and s[i:i+2] in roman:
            num += roman[s[i:i+2]]
            i += 2
        else:
            num += roman[s[i]]
            i += 1
    return num


def process_mult(m):
    """Calculates and stores intergalactic multipliers found in the input.
    
    :param m: The match object returned from regular expression matching.
    """
    multiplier = m[0][0].split()[-1]
    units = m[0][0].split()[:-1]
    roman_str = units_to_rn(units)
    num = rn_to_int(roman_str)
    i_mult[multiplier] = int(m[0][1]) / num


def process_credits(m):
    """Calculate the credit from input.
    
    :param m: The match object returned from regular expression matching.
    """
    multiplier = m[0].split()[-1]
    units = m[0].split()[:-1]
    # Process scenario with no multiplier.
    if multiplier not in i_mult:
        units.append(multiplier)
        roman_str = units_to_rn(units)
        num = rn_to_int(roman_str)
        print(f'{m[0].strip()} is {num}')
    # Process scenario with multiplier.
    else:
        roman_str = units_to_rn(units)
        num = rn_to_int(roman_str)
        credits = num * i_mult[multiplier]
        print(f'{m[0].strip()} is {round(credits)} Credits')


def print_err_msg():
    print('I have no idea what you are talking about')


def process(input):
    """Main processor."""
    for i in input.splitlines():
        line = i.strip()
        if not line:
            continue
        m = re.findall('^([^ ]+) is ([IVXLCDM])$', line)
        if m:
            i_units[m[0][0]] = m[0][1]
            continue
        
        m = re.findall('^(.+) is ([0-9]+) Credits$', line, re.IGNORECASE)
        if m:
            process_mult(m)
            continue
    
        m = re.findall('^how .+ is (.+)\?$', line, re.IGNORECASE)
        if m:
            process_credits(m)
            continue
   
        print_err_msg()


def main():
    process('''
    glob is I
    prok is V
    pish is X
    tegj is L
    glob glob Silver is 34 Credits
    glob prok Gold is 57800 Credits
    pish pish Iron is 3910 Credits
    how much is pish tegj glob glob ?
    how many Credits is glob prok Silver ?
    how many Credits is glob prok Gold ?
    how many Credits is glob prok Iron ?
    how much wood could a woodchuck chuck if a woodchuck could chuck wood ?
    ''')


if __name__ == '__main__':
    main()
