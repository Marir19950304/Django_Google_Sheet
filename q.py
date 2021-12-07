from sodapy import Socrata
from dotenv import load_dotenv
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


def gen_django_field():
    """
    docstring
    """
    buffer = ''
    with open('./fields.txt', 'rt', newline='') as infile:
        for idx, line in enumerate(infile.readlines()):
            line = line.strip(" \r\n\t")
            if (idx % 2) == 0:
                right = f"models.CharField(_('{line}'), max_length=100, null=True, blank=True)"
            else:
                buffer += f"{line} = {right}\n"

        print(buffer)


if __name__ == "__main__":
    socrata()
