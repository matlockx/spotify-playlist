# spotify-playlist

Creates a new playlist for your 'Discover Weekly' playlist from spotify with the new name 'DiscoverWeekly_KW[CalendarWeek], e.g. 'DiscoverWeekly_KW43'. When you run it for the first time and you open the 

###How to run

####Spotify App

* Create an app here: https://developer.spotify.com/my-applications/#!/applications/create
* Save your client_id and client_secret in your head or somewhere, you need it later
* Add http://localhost:8080/success to the redirects URIs and do not forget to hit the save button at the end of the page
  * boot2docker: http://[boot2docker_ip]:8080/success , e.g. http://192.168.59.103:8080/success

#### Docker

```
docker run -d -e "USER=[YOUR_SPOTIFY_USER_NAME]" -e "CLIENT_ID=[YOUR_CLIENT_ID]" -e "CLIENT_SECRET=[YOUR_CLIENT_SECRET]" -p 8080:8080 matlockx/spotify-playlist
```

Open your browser at http://localhost:8080/create-playlist or http://[boot2docker_ip]:8080/create-playlist

#### Direct

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
