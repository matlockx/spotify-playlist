#!/usr/bin/env bash

export CLIENT_ID=
export CLIENT_SECRET=
export USER=

open http://localhost:8080/create-playlist && python -m bottle -b 0.0.0.0:8080 main --debug
