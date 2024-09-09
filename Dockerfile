FROM nginx:alpine

RUN apk add --no-cache python3 
RUN apk add --no-cache openssl

ARG ENABLE_ALPINE_PRIVATE_NETWORKING=true

ARG OPT_PORT=8910
ARG OPTS_PROXY_PASS=http://localhost:8910
ARG OPTS_SERVER_NAME=_

ARG OPT_USERNAME=admin
ARG OPT_PASSWORD=admin

ENV ENABLE_ALPINE_PRIVATE_NETWORKING=$ENABLE_ALPINE_PRIVATE_NETWORKING
ENV OPT_PORT=$OPT_PORT
ENV PORT=$OPT_PORT

WORKDIR /etc/nginx

COPY ./nginx_config.py nginx_config.py
COPY ./nginx_config_templates nginx_config_templates
RUN ["python3", "nginx_config.py"]

ENV OPT_USERNAME=$OPT_USERNAME
ENV OPT_PASSWORD=$OPT_PASSWORD
COPY ./nginx_password.sh nginx_password.sh
RUN ["chmod", "+x", "nginx_password.sh"]
RUN ./nginx_password.sh

EXPOSE ${PORT}
