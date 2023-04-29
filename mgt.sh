#!/bin/bash

pushd src/management_server

git reset ---hard
git pull origin dev-na
sh run_mgt_server.sh