from requests_html import HTMLSession
from bs4 import BeautifulSoup
import spotipy
from spotipy.oauth2 import SpotifyOAuth
import datetime

date = input("What date would you like? Use YYYY-MM-DD :")
WEB_PAGE = f"https://www.billboard.com/charts/hot-100/{date}"
WEB_FILE = f"{date}_billboard.html"

YOUR_UNIQUE_CLIENT_ID = "583918135ccb495897d18e0b741e99d7"
YOUR_UNIQUE_CLIENT_SECRET = "08aa3b036c37436c82d2f507b95c2c2e"
REDIRECT_URI = "http://example.com"


# Using requests_html to render JavaScript
def get_web_page():
    # create an HTML Session object
    session = HTMLSession()
    # Use the object above to connect to needed webpage
    response = session.get(WEB_PAGE)
    # Run JavaScript code on webpage
    response.html.render()

    # Save web page to file
    with open(WEB_FILE, mode="w", encoding="utf-8") as fp:
        fp.write(response.html.html)


def read_web_file():
    try:
        open(WEB_FILE)
    except FileNotFoundError:
        get_web_page()
    finally:
        # Read the web page from file
        with open(WEB_FILE, mode="r", encoding="utf-8") as fp:
            content = fp.read()
        return BeautifulSoup(content, "html.parser")


# Read web file if it exists, load from internet if it doesn't exist
# result = read_web_file()

soup = read_web_file()
print(soup.prettify())

song_list = [rank.getText() for rank in soup.find_all
             (name="span",
             class_="chart-element__information__song text--truncate color--primary")]

print(song_list)

sp = spotipy.Spotify(
    auth_manager=SpotifyOAuth(
        scope="playlist-modify-private",
        redirect_uri=REDIRECT_URI,
        client_id=YOUR_UNIQUE_CLIENT_ID,
        client_secret=YOUR_UNIQUE_CLIENT_SECRET,
        show_dialog=True,
        cache_path="token.txt"
    )
)
user_id = sp.current_user()["id"]

song_uris = []
year = date.split("-")[0]
month = date.split("-")[1]
day = date.split("-")[2]
x = datetime.datetime(int(year), int(month), int(day))
short_month = (x.strftime("%b"))

for song in song_list:
    result = sp.search(q=f"track:{song} year:{year}", type="track")
    print(result)
    try:
        uri = result["tracks"]["items"][0]["uri"]
        song_uris.append(uri)
    except IndexError:
        print(f"{song} doesn't exist in Spotify. Skipped.")

playlist = sp.user_playlist_create(user=user_id, name=f"Billboard 100 for {day} {short_month} {year}", public=False)

sp.playlist_add_items(playlist_id=playlist["id"], items=song_uris)
