#! /bin/bash

sudo docker stop lazarnikolic/porter-live

sudo docker rm lazarnikolic/porter-live

sudo docker build -t lazarnikolic/porter-live .
sudo docker run -p 8004:8004 lazarnikolic/porter-live
