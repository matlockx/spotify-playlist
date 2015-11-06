spotify-playlist
================

Creates a new playlist for your 'Discover Weekly' playlist from spotify with the new name 'DiscoverWeekly*[CurentYear]*[CurrentCalendarWeek], e.g. 'DiscoverWeekly_2015_43'.

You must run it every week otherwise you will not get the newest playlists any more (create a cron job, run it manually, change the code to run with a scheduler, etc.)

###How to run

#### 1. Create Spotify App

-	Create an app here: https://developer.spotify.com/my-applications/#!/applications/create
-	Save your client_id and client_secret in your head or somewhere, you need it later
-	Add http://localhost:8080/success to the redirects URIs and do not forget to hit the save button at the end of the page
  -	boot2docker: http://[boot2docker_ip]:8080/success , e.g. http://192.168.59.103:8080/success

#### 2. Docker

Docker Image: https://hub.docker.com/r/matlockx/spotify-playlist/

```
docker run -d -e "USER=[YOUR_SPOTIFY_USER_NAME]" -e "CLIENT_ID=[YOUR_CLIENT_ID]" -e "CLIENT_SECRET=[YOUR_CLIENT_SECRET]" -p 8080:8080 matlockx/spotify-playlist
```

Open your browser at [http://localhost:8080/create-playlist](http://localhost:8080/create-playlist) or [http://[boot2docker_ip]:8080/create-playlist](http://[boot2docker_ip]:8080/create-playlist)

When you run it for the first time and you open the browser you need to login to spotify with your username and password and you need to allow the requested grants. Currently these are requested:

-	playlist-read-private
-	playlist-read-collaborative
-	playlist-modify-public
-	playlist-modify-private

I don't know whether you need all of them (I'm too lazy to look it up) but you need at least the private permissions otherwise the playlist cannot be created.

---

##### Run it directly

Create virtual environment:

```
mkdir ~/.virtualenvs
pyvenv-3.5 ~/.virtualenvs/spotify
source ~/.virtualenvs/spotify/bin/activate
pip install -r requirements.txt
```

Create a small bash script, e.g. run.sh:

```
#!/usr/bin/env bash

export CLIENT_ID=[YOUR_CLIENT_ID]
export CLIENT_SECRET=[YOUR_CLIENT_SECRET]
export USER=[YOUR_SPOTIFY_USER_NAME]

open http://localhost:8080/create-playlist && python -m bottle -b 0.0.0.0:8080 main --debug
```

Run it:

```
chmod +x run.sh
./run.sh
```
