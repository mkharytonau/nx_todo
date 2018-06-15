import argparse
from collections import namedtuple


def parse_owners(input_string):
    Owner = namedtuple('Owner', 'user_name access_level')
    owners_data = input_string.split()
    try:
        return Owner(owners_data[0], owners_data[1])
    except IndexError:
        msg = "'{}' is incorrect data, expected " \
              "'user_name access_level'".format(input_string)
        raise argparse.ArgumentTypeError(msg)