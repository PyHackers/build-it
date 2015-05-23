#!/bin/bash
cd ../data/
sudo tar -cv * | sudo docker exec -i $0 /bin/tar x -C $1