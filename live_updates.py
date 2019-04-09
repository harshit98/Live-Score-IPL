"""
This python script will scrap the live updates from this site: https://demo.entitysport.com/
by downloading the whole page.
"""

# Import necessary libraries for scraping.
import argparse
import requests
import time

from bs4 import BeautifulSoup
from plyer import notification

parser = argparse.ArgumentParser()
parser.add_argument(
    "--team",
    action="store",
    dest="team",
    default="A",
    choices={"A","B"},
    help="Team A or Team B",
    required=False
)

results = parser.parse_args()
team = results.team
