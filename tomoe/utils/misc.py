import argparse
import os

def choose():
    my_parser = argparse.ArgumentParser()
    my_parser.add_argument('--nhentai', action='store', type=int)
    my_parser.add_argument('--pururin', action='store', type=int)
    my_parser.add_argument('--simply', action='store', type=str)
    my_parser.add_argument('--hentaifox', action='store', type=int)
    my_parser.add_argument('--hentai2read', action='store', type=str)
    

    args = my_parser.parse_args()
    return args

def split_name(string):
    get_name = os.path.basename(string).split('.')[0]
    return get_name