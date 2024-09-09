#!/bin/sh

USERNAME=${OPT_USERNAME}
PASSWORD=${OPT_PASSWORD}

echo "Generating password for username ${USERNAME}"

CRYPTPWD=`openssl passwd -apr1 ${PASSWORD}`

echo "${USERNAME}:${CRYPTPWD}" >> /etc/nginx/.htpasswd
