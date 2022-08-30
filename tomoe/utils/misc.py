import janda
import argparse
import os
import logging
import re
from xhtml2pdf import pisa

logging.basicConfig(format="%(asctime)s - %(message)s", level=logging.INFO)


def choose():
    my_parser = argparse.ArgumentParser()

    my_parser.add_argument(
        "--nhentai", "-nhentai", action="store", nargs='+'
    )
    my_parser.add_argument(
        "--pururin", "-pururin", action="store", nargs='+'
    )
    my_parser.add_argument(
        "--simply", "-simply", action="store", nargs='+'
    )
    my_parser.add_argument(
        "--hentaifox", "-hentaifox", action="store", nargs='+'
    )
    my_parser.add_argument(
        "--hentai2read", "-hentai2read", action="store", nargs='+',
    )
    my_parser.add_argument(
        "--asmhentai", "-asmhentai", action="store", nargs='+'
    )
    my_parser.add_argument(
        "--bulk", "-bulk", action="store", metavar=("BULK"), type=str
    )

    args = my_parser.parse_args()
    return args


def split_name(string):
    """Split string into name and extension

    Parameters
    ----------
    string : str
        String to split

    Returns
    -------
    name : str
        Name of the file
    """
    get_name = os.path.basename(string).split(".")[0]
    return get_name


def get_size(string):
    """Get size of a file

    Parameters
    ----------
    string : str
        Path to file

    Returns
    -------
    size : int
        Size of the file
    """
    file = round(os.path.getsize(string) / 1024 / 1024, 2)
    return file


def get_size_folder(folder):
    """Get size of a folder

    Parameters
    ----------
    folder : str
        Path to folder

    Returns
    -------
    size : int
        Size of the folder
    """
    total_size = 0
    for dirpath, dirnames, filenames in os.walk(folder):
        for f in filenames:
            fp = os.path.join(dirpath, f)
            total_size += os.path.getsize(fp)
    return round(total_size / 1024 / 1024, 2)


def project():
    return '<p><b><h1>Generated from tomoe: <a href="https://pypi.org/project/tomoe/">pypi.org/project/tomoe</a></b><h1>'


def convert_html_to_pdf(source_html, output_filename):
    """Convert html to pdf

    Parameters
    ----------
    source_html : str
        Path to html file
    output_filename : str
        Path to pdf file
    """

    result_file = open(output_filename, "w+b")
    pisa_status = pisa.CreatePDF(source_html, dest=result_file)

    result_file.close()
    return pisa_status.err


def nums(first_number, last_number, step=1):
    """Generate access index of a list

    Parameters
    ----------
    first_number : int
        First number
    last_number : int
        Last number
    step : int
        Step

    Returns
    -------
    list
        List of numbers
    """
    return range(first_number, last_number + 1, step)


def need_args():
    """Check if arguments are given

    Returns
    -------
    bool
    """
    return print("No arguments was given")


def log_data(case, note):
    """Logging data

    Parameters
    ----------
    case : str
        Case of the log

    note : str
        Note of the log
    """
    logging.info(f"{case}: {note}")


def log_file(file: str, size: str, took: str):
    """Logging file

    Parameters
    ----------
    case : str
        Case of the log

    file : str
        File name

    size : str
        File size

    took : str
        Time took
    """
    logging.info(f"Successfully downloaded {file}: {size} MB, took: {took} Seconds")

def log_warn(case: str, note: str):
    """Logging warning

    Parameters
    ----------
    case : str
        Case of the log

    note : str
        Note of the log
    """
    logging.info(f"{case}: {note}")


def log_final(taken: str, total_size: str):
    """Final log

    Parameters
    ----------
    taken : str
        Time took

    total_size : str
        Total size
    """
    logging.info(
        f"Successfully downloaded all images taken {taken} minutes with total size {total_size} MB"
    )
