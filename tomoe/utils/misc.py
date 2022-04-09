import argparse
import os
from xhtml2pdf import pisa


def choose():
    my_parser = argparse.ArgumentParser()

    my_parser.add_argument(
        "--nhentai", "-nhentai", action="store", metavar=("ID"), type=int
    )
    my_parser.add_argument(
        "--pururin", "-pururin", action="store", metavar=("ID"), type=int
    )
    my_parser.add_argument(
        "--simply", "-simply", action="store", metavar=("PATH_AFTER_WWW"), type=str
    )
    my_parser.add_argument(
        "--hentaifox", "-hentaifox", action="store", metavar=("ID"), type=int
    )
    my_parser.add_argument(
        "--hentai2read",
        "-hentai2read",
        nargs=2,
        action="store",
        metavar=("PATH", "CHAPTER"),
        type=str,
    )
    my_parser.add_argument(
        "--qhentai", "-qhentai", action="store", metavar=("PATH_AFTER_WWW"), type=str
    )
    my_parser.add_argument(
        "--asmhentai", "-asmhentai", action="store", metavar=("ID"), type=int
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
    """watermark hehe"""
    return '<p><b><h1><a href="https://pypi.org/project/tomoe/">Generated from tomoe: https://pypi.org/project/tomoe</a></b><h1>'


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
