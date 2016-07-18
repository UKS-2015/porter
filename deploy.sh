#! /bin/bash

sudo docker stop porter-live

sudo docker rm porter-live

sudo docker build -t porter-live .
sudo docker run -p 8004:8004 porter-live
