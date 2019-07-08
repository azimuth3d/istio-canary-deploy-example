#!/bin/bash
# Change docker image to your repo name 

docker build . -t docker.io/azimuth3d/flaskapp:v1
docker push azimuth3d/flaskapp
