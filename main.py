import datetime
import json
import os
from pprint import pprint

from attrdict import AttrDict
from bottle import redirect
import bottle
from rauth import OAuth2Service

CLIENT_ID = os.environ.get("CLIENT_ID")
CLIENT_SECRET = os.environ.get("CLIENT_SECRET")
USER = os.environ.get("USER")

#print("Trying to create a new weekly playlist for user {} CLIENT_ID {} and CLIENT_SECRET".format(USER, CLIENT_ID, CLIENT_SECRET))

WEEKLY_PLAYLIST_NAME = "DiscoverWeekly_KW{}".format(datetime.date.today().isocalendar()[1])

USER_GRANTS = "playlist-read-private playlist-read-collaborative playlist-modify-public playlist-modify-private"

spotify = OAuth2Service(
    name='spotify',
    client_id=CLIENT_ID,
    client_secret=CLIENT_SECRET,
    access_token_url='https://accounts.spotify.com/api/token',
    authorize_url='https://accounts.spotify.com/authorize/')

redirect_uri = "http://{}/success"


def get_weekly_playlist(session):
    return get_playlist_for_name(session, "Discover Weekly")


def get_playlist_for_name(session, name):
    response = session.get("https://api.spotify.com/v1/users/{}/playlists".format(USER))
    playlist = [playlist for playlist in response.json()['items'] if playlist['name'] == name] if response.ok else None
    return AttrDict(playlist[0]) if playlist and len(playlist) >= 1 else None


def create_new_playlist(session, name):
    response = session.post("https://api.spotify.com/v1/users/{}/playlists".format(USER), json={"name": name, "public": True})
    return AttrDict(json.loads(response.text))


def get_playlist_tracks(session, playlist, print_tracks=False):
    tracks = json.loads(session.get(playlist.tracks.href).text)
    for track in tracks['items']:
        artists = [artist['name'] for artist in track['track']['artists']]
        if print_tracks:
            pprint("{} - {}".format(", ".join(artists), track['track']['name']))

    uris = [track['track']['uri'] for track in tracks['items']]
    return uris


def add_tracks(session, endpoint, tracks):
    response = session.post(endpoint, json={"uris": tracks})
    return response


@bottle.route('/')
def index():
    return '<a href="/login">Log in using Spotify</a>'


@bottle.route('/create-playlist')
def index():
    redirect("/login")


@bottle.route('/login<:re:/?>')
def login():
    params = dict(
        scope=USER_GRANTS,
        response_type='code',
        redirect_uri=redirect_uri.format(bottle.request.get_header('host'))
    )
    url = spotify.get_authorize_url(**params)

    redirect(url)


def bytes_json(payload):
    return json.loads(payload.decode('utf-8'))


@bottle.route('/success<:re:/?>')
def login_success():
    code = bottle.request.params.get('code')
    print(code)
    session = spotify.get_auth_session(
        data=dict(
            code=code,
            redirect_uri=redirect_uri.format(bottle.request.get_header('host')),
            grant_type='authorization_code'
        ),
        json={"client_id": CLIENT_ID, "client_secret": CLIENT_SECRET},
        decoder=bytes_json
    )
    return create_playlist(session)


def create_playlist(session):
    playlist = get_weekly_playlist(session)
    print()
    print("Tracks of current Weekly Discovery Playlist:")
    tracks = get_playlist_tracks(session, playlist, True)
    print()

    new_playlist_name = WEEKLY_PLAYLIST_NAME
    new_playlist = get_playlist_for_name(session, new_playlist_name)
    if not new_playlist:
        new_playlist = create_new_playlist(session, new_playlist_name)
        if add_tracks(session, new_playlist.tracks.href, tracks).ok:
            print("Successfully created new playlist {}".format(new_playlist_name))
    else:
        print("Playlist {} already exists.".format(new_playlist_name))

    print()
    print("Playlist {} content:".format(new_playlist_name))
    result = get_playlist_for_name(session, new_playlist_name)
    pprint(result)
    return result

#
