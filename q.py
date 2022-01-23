from sodapy import Socrata
from dotenv import load_dotenv
import argparse
import os

load_dotenv()

API_KEY = os.environ.get("API_KEY")
APP_TOKEN = os.environ.get("APP_TOKEN")
API_SECRET = os.environ.get("API_SECRET")


def socrata():
    """
    docstring
    """

    with Socrata("data.cityofnewyork.us", APP_TOKEN, API_KEY, API_SECRET) as client:
        response = client.get("erm2-nwe9", limit=2)
        print(response)
        import pdb
        pdb.set_trace()


def gen_django_field(inpfile):
    """
    docstring
    """
    buffer = ''
    with open(inpfile, 'rt', newline='') as infile:
        for idx, line in enumerate(infile.readlines()):
            line = line.strip(" \r\n\t")
            if (idx % 2) == 0:
                right = f"models.CharField(_('{line}'), null=True, blank=True, max_length=200)"
            else:
                buffer += f"{line} = {right}\n"

        print(buffer)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--genfields")
    args = parser.parse_args()
    if args.genfields:
        gen_django_field(args.genfields)
    # socrata()
