#!/bin/sh

USER=${USERNAME}
PWD=${PASSWORD}

echo "Generating password for user ${USER}"

CRYPTPWD=`openssl passwd -apr1 ${PWD}`

echo "${USER}:${CRYPTPWD}" >> /etc/nginx/.htpasswd
