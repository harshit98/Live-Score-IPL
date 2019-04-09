"""
@author: Harshit Prasad

Description: This python script will scrap the live updates from this site: https://demo.entitysport.com/
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

# Gets Team A as default.
# Using --team argument to select Team A or B.
team = results.team

# Assign class of div w.r.t scraped data.
if team == "A":
    team_name = "teamaScore"
else:
    team_name = "teambScore"

previous_ball_update = 0

def SystemNotification(title, commentary, current_score):
    """ To display notification on the system """
    notification.notify(
        title=title, message="commentary" + " " + current_score, timeout=30
    )

def GetHTML(url="https://demo.entitysport.com/"):
    """Downloads the homepage structure"""
    # Attaching headers for browser compatibility.
    headers = {
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36"
    }
    html = requests.get(url, headers=headers)
    soup = BeautifulSoup(html.content, "html5lib")
    return soup

def GetMatchURL(soup):
    """Gets the ongoing match URL"""
    live_match_url = soup.find("a", attrs={"class": "match-status-3"})["href"]
    return live_match_url

def GetLiveUpdates(live_match_url):
    """Scrap live updates"""
    print("Fetching live updates...")
    global previous_ball_update
    while True:
        # Sleep for 5 seconds.
        time.sleep(5)

        # URL of live match.
        soup = GetHTML(live_match_url)

        # Get match title.
        title = soup.find("h1", attrs={"id":"heading"}).text.split(",")[0]

        # Get update from last ball.
        last_ball = soup.find("div", attrs={"class":"live-info4"}).span.text.strip()

        # Get current score.
        current_score = soup.find("div", attrs={"class":team_name}).text.strip()

        # Get current over.
        current_ball_update = soup.find("div", attrs={"class":"ovb"}).text.strip()

        if current_ball_update != previous_ball_update:
            # Wicket!
            if last_ball == "W":
                last_wicket_commentary = soup.find(
                    "div", attrs={"class":"comment-wicket"}
                )
                last_wicket_commentary = last_wicket_commentary.find(
                    "div", attrs={"class":"text"}
                ).text.strip()

                print("Last Wicket Commentary: " + last_wicket_commentary + " " + current_score)
                SystemNotification(title, last_wicket_commentary, current_score)
                time.sleep(60)
            
            # Four or Six!
            elif (last_ball == "4") or (last_ball == "6"):
                last_hit_commentary = soup.find("div", attrs={"class":"comment-ball"})
                last_hit_commentary = last_hit_commentary.find(
                    "div", attrs={"class":"text"}
                ).text.strip()

                print("Last Hit Commentary: " + last_hit_commentary + " " + current_score)
                SystemNotification(title, last_hit_commentary, current_score)
            
            previous_ball_update = current_ball_update

if __name__ == "__main__":
    soup = GetHTML()
    live_match_url = GetMatchURL(soup)

    # Get live updates! 
    GetLiveUpdates(live_match_url)
