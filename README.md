# `STONE-RPWBA` Reverse Proxy (with basic auth)

## Local installation

Start by building the image:

```commandline
$ docker build {{build-args}} -t stone-rpwba .
```
* Required Build Args:
  * `--build-arg OPTS_PROXY_PASS=...` one or multiple service private network urls. If regusting several urls, separate them with `;` (e.g., `http://...:8080;http://...:8888`).
  * `--build-arg OPTS_SERVER_NAME=...` one or multiple services server names. Must match by position to the ordering of the `OPTS_PROXY_PASS` urls. If registering several domain names, separate the with `;` (e.g., `site1.domain.com;site2.domain.com`).
* Optional Build Args:
  * `--build-arg USERNAME=...` the username to use on the basic auth.
  * `--build-arg PASSWORD=...` the password to use on the basic auth.

If your proxy-pass only contains one site url, use `OPTS_SERVER_NAME=_` to forward without any subdomains. Example:

```commandline
docker build \
  --build-arg OPTS_SERVER_NAME=_ \
  --build-arg OPTS_PROXY_PASS={{service-url}} \
  ... \
  -t stonebase-rpwba .
```

To run the container:

```commandline
$ docker run -d \
  -e ENABLE_ALPINE_PRIVATE_NETWORKING=true \
  --name stonebase-rpwba \
  -p 8910:8910 \
  stone-rpwba
```
* Stop: `docker stop /stone-rpwba`
* Remove: `docker rm /stone-rpwba`

## Railway 

