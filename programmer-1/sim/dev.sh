#!/bin/bash -e
cd /code
pipenv install --system --deploy
yarn install
cd /
exec /usr/bin/supervisord -n -c /dev.supervisor.conf
