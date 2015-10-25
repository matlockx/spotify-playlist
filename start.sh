#!/usr/bin/env bash

docker rm -fv spotify-playlist
docker run -d -p 8080:8080 --name spotify-playlist spotify-playlist
open http://192.168.59.103:8080/create-playlist
