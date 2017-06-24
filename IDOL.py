#!/usr/bin/env python

"""This module filters the packets
in the input file and generates output files
with packets seperated by addresants
using some conditions"""

import sys
import os

# global constants

# addresant names
IVAN = 'Ivan'
DMYTRO = 'Dmytro'
OSTAP = 'Ostap'
LESYA = 'Lesya'

# for Lesya
END_STR = 'end'

# extension for output files
OUTPUT_FILE_EXT = 'txt'

# addressants
contacts = (IVAN, DMYTRO, OSTAP, LESYA)
# conditions; with default contidion - False
# if condition wasn't set to the addresant then
# it will skip messages for him
conditions = dict.fromkeys(contacts, lambda x: False)


def check_IVAN(msg):
    """check condition for @str for Ivan and return boolean"""

    if msg:
        return len(msg) % 2 == 0
    return False


def check_DMYTRO(msg):
    """check condition for @str for Dmytro and return boolean"""

    if msg:
        return not check_IVAN(msg) and msg[0].isupper()
    return False


def check_LESYA(msg):
    """check condition for @str for Lesya and return boolean"""

    if msg:
        return msg.split()[-1] == END_STR
    return False


def check_OSTAP(msg):
    """check condition for @str for Ostap and return boolean"""

    if msg:
        return not (check_IVAN(msg)
                    or check_DMYTRO(msg)
                    or check_LESYA(msg))


def usage():
    """Output the usage message to user"""

    print('Usage: {} [path to messages file]'.format(sys.argv[0]))


def parse_messages_file(msg_path):
    """Parses messages file placed in @msg_path
    and returns a dictionary of messages
    filtred for all adresants"""

    # messages dictionary
    messages = {addr: [] for addr in contacts}

    # for line without \n
    for line in [x.rstrip('\n') for x in open(msg_path)]:
        for addresant in contacts:
            # if condition for line for current addresant
            # is true then append message to messages list
            # of that addresant 
            if conditions[addresant](line):
                messages[addresant].append(line)

    return messages


def gen_messages_files(messages):
    """Generates files by contacts using
    messages dictionary"""

    for contact in messages:
        with open(contact + '.' + OUTPUT_FILE_EXT, 'w') as output_file:
            output_file.write('\n'.join(messages[contact]))


def main():
    # initializing conditions list
    conditions['Ivan'] = check_IVAN
    conditions['Dmytro'] = check_DMYTRO
    conditions['Lesya'] = check_LESYA
    conditions['Ostap'] = check_OSTAP

    # path to file with packets
    messages_path = ''
    try:
        messages_path = sys.argv[1]
    except IndexError:
        usage()
        exit(1)

    if not os.path.isfile(messages_path):
        usage()
        print('Not a file')
        exit(1)

    messages = parse_messages_file(messages_path)
    gen_messages_files(messages)


if __name__ == '__main__':
    main()
