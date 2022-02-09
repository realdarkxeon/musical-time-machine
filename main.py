from bs4 import BeautifulSoup
import lxml, requests, spotipy, pprint
from spotipy.oauth2 import SpotifyOAuth

query_date = input("Which year do you want to travel to? "
                   "Type the date in this format YYYY-MM-DD\n")

billboardChartLink = "https://www.billboard.com/charts/hot-100/" + query_date
response = requests.get(billboardChartLink)
soup = BeautifulSoup(response.text, "lxml")

print("Parsing data from 'billboard.com'...")
try:
    songs_html = soup.select("h3.c-title.a-no-trucate.a-font-primary-bold-s.u-letter-spacing-0021.lrv-u-font-size-16.u-line-height-125.a-truncate-ellipsis")
    artists_html = soup.select("span.c-label.a-no-trucate.a-font-primary-s.u-letter-spacing-0021.lrv-u-display-block.a-truncate-ellipsis-2line.u-max-width-330")
except:
    print("Chart source is not available.")
    exit()

if not songs_html:
    print("Chart source is not available.")
    exit()

songs = [song.text.split("\n")[1] for song in songs_html]
artists = [artist.text.split("\n")[1] for artist in artists_html]

# Procedure for better search of the name of the song
prohibited = ["Featuring", "x", "X", "&", "/", "+"]

for i in range(len(artists)):
    parts = artists[i].split()
    substitute = ""
    for part in parts:
        if part in prohibited:
            continue
        if part == "Or":
            break
        if part[len(part)-1] == ',':
            part = part[0:len(part)-1]
        part += " "
        substitute += part
    artists[i] = substitute

client_id = <CLIENT_ID>
client_secret = <CLIENT_SECRET>
redirect_url = "http://example.com/"
scope = "playlist-modify-private"
print("Signing in to Spotify...")
sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id=client_id, client_secret=client_secret, redirect_uri=redirect_url, scope=scope))
user = sp.current_user()["id"]

# To successfully authorize via Spotipy, you must paste a link from redirected website (see redirect_url)

print("Creating playlist...")
playlist = sp.user_playlist_create(user=user, name=f"{query_date} Top 100 Billboard", public=False, description=f"Based on Billboard Chart of date {query_date}")
playlist_id = playlist["id"]
playlist_url = playlist["external_urls"]["spotify"]

tracks = []

for i in range(len(songs)):
    results = sp.search(f"{songs[i]} {artists[i]}")
    try:
        result = results["tracks"]["items"][0]["uri"]
    except:
        print(f"The song '{songs[i]}' by artist '{artists[i]}' not found.")
        result = None

    if result:
        tracks.append(result)

print(f"{len(tracks)}/100 tracks found.")

print("Adding tracks to our playlist...")
sp.playlist_add_items(playlist_id=playlist_id, items=tracks)

print("Well done! Here is the link:")
print(playlist_url)