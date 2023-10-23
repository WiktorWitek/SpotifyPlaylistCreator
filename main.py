import requests
from bs4 import BeautifulSoup
import spotipy
from spotipy.oauth2 import SpotifyOAuth


C_ID = "" # client_id
C_SEC = "" # client_secret

year = input("Year (YYY-MM-DD): ")

req = requests.get(f"https://www.billboard.com/charts/hot-100/{year}")
data = req.text

soup = BeautifulSoup(data, "html.parser")

song_titles = soup.find_all("h3", class_="a-no-trucate", )
song_list = [song.getText().strip() for song in song_titles]
song_url_list = []

sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id=C_ID, client_secret=C_SEC, redirect_uri="http://example.com", scope="playlist-modify-private"))

user = sp.current_user()["id"]



for song in song_list:
    s = sp.search(q=song, limit=1, )
    song_url_list.append(s['tracks']['items'][0]['external_urls']['spotify'])




playlist = sp.user_playlist_create(user=user, name=year, public=False)
try:
    sp.playlist_add_items(playlist_id=playlist['id'], items=song_url_list)
except:
    pass