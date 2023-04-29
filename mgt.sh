#!/bin/bash

git reset --hard
git pull origin dev-na

pushd src/management_server

sh run_mgt_server.sh