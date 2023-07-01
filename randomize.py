import configparser
import spotipy
import random
from spotipy.oauth2 import SpotifyOAuth

# Read the config file
config = configparser.ConfigParser()
config.read('config.ini')

# Get the Spotify credentials from the config file
client_id = config['Spotify']['client_id']
client_secret = config['Spotify']['client_secret']
redirect_uri = config['Spotify']['redirect_uri']
username = config['Spotify']['username']

# Setup the Spotify OAuth
scope = 'user-library-read playlist-modify-public playlist-read-private playlist-read-collaborative'
token = SpotifyOAuth(client_id=client_id, client_secret=client_secret, redirect_uri=redirect_uri, scope=scope, username=username)

spotify = spotipy.Spotify(auth_manager=token)

# Unfollow the playlist if it already exists
print("Checking if playlist exists...")
playlists = spotify.user_playlists(username)
for playlist in playlists['items']:
    if playlist['name'] == "Randomized Liked Songs":
        print(f"Playlist found with id {playlist['id']}, unfollowing...")
        spotify.user_playlist_unfollow(username, playlist['id'])
        print("Playlist unfollowed.")
        break

# Create a new playlist
playlist = spotify.user_playlist_create(user=username, name="Randomized Liked Songs")
print(f"Created new playlist with id {playlist['id']}")

# Get the user's liked songs with pagination
print("Retrieving liked songs...")
results = spotify.current_user_saved_tracks()
tracks = []
while results:
    for item in results['items']:
        track = item['track']
        tracks.append(track['id'])
    if results['next']:
        results = spotify.next(results)
    else:
        results = None

print(f"Retrieved {len(tracks)} liked songs.")

# Shuffle the tracks
random.shuffle(tracks)
print("Shuffled the songs.")

# Add tracks to the playlist in chunks of 100
print("Adding songs to the playlist...")
for i in range(0, len(tracks), 100):
    spotify.user_playlist_add_tracks(user=username, playlist_id=playlist['id'], tracks=tracks[i:i+100])
    print(f"Added {i+100 if i+100 < len(tracks) else len(tracks)} songs.")
    
print("All songs added to the playlist.")
