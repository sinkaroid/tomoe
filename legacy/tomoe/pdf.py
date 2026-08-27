import os

from inputimeout import inputimeout

from .utils.const import TOMOE_HTML
from .utils.misc import choose, convert_html_to_pdf, get_size


def process_pdf(dir: str, id: str):
    if choose().pdf:
        render_pdf(dir, id)
    else:
        desired = inputimeout(
            prompt="Do you want to render it all to .pdf? (y/n) ",
            timeout=10,
        )
        to_pdf = desired

        if to_pdf == "y":
            try:
                render_pdf(dir, id)

            except Exception as e:
                print(f"Something went wrong while converting to pdf: {e}")

        elif to_pdf == "n":
            print("Okay")
            os.remove(dir + "/" + TOMOE_HTML)
            return

        else:
            print("Invalid input")
            os.remove(dir + "/" + TOMOE_HTML)
            return


def render_pdf(dir: str, id: str):
    source = open(f"{dir}/{TOMOE_HTML}")
    output = f"{dir}/{id}.pdf"
    filepdf = output.rsplit("/", 1)[-1]

    convert_html_to_pdf(source, output)
    print(f"Successfully rendered to {filepdf} | {get_size(output)} MB")
