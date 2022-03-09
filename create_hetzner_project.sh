#!/bin/bash

mkdir -p /tmp/hetzner_api_token
chown 1200:1201 /tmp/hetzner_api_token

docker build -t hetzner_login . 

docker run --rm -it \
        -v /tmp/hetzner_api_token:/home/seluser/hetzner_api_token \
        -e USERNAME=simonlauber@outlook.de \
        -e PASSWORD=W:3s#9nW% \
        -e PROJECT=Vanilla \
        -e PERMISSIONS="Read & Write" \
        -e EMAIL_MEMBER=simonparmesan@outlook.de \
        -e MEMBER_ROLE=admin \
        hetzner_login python3 hetzner_login.py


password=$(cat /tmp/hetzner_api_token/HETZNER_API_TOKEN)
echo "Hetzner API Token: $password"
rm -rf /tmp/hetzner_api_token