import os
import sys
import textwrap
from typing import Optional


OPT_PORT = os.environ.get(
    "OPT_PORT",
    default=os.environ.get("PORT")  # Reference the PORT env.var when in railway
)
OPT_OUTPUT_DIRPATH = os.environ.get(
    "OPT_OUTPUT_DIRPATH",
    default=""
)

OPT_OUTPUT_FILENAME = os.environ.get(
    "OPT_OUTPUT_FILENAME",
    default="nginx.conf"
)
OPT_ENVSEP = os.environ.get(
    "OPT_ENVSEP",
    default=",",
)

OPTS_PROXY_PASS = os.environ.get(
    "OPTS_PROXY_PASS",
)
OPTS_SERVER_NAME = os.environ.get(
    "OPTS_SERVER_NAME",
)

class Template:

    def __init__(self, name: str, dirpath: Optional[str] = None):
        self.name = name
        self.dirpath = dirpath or "./nginx_config_templates"
        with open(self.filepath, "r") as fh:
            self.content = fh.read()

    @property
    def filepath(self) -> str:
        return os.path.join(self.dirpath, self.name)

    def apply(self, **kwargs) -> str:
        template = f"{self.content}"
        for key, val in kwargs.items():
            template = template.replace(f"<py:{key}>", val)
        return template


def main(
        nginx_output_dirpath: Optional[str] = None,
        nginx_output_filename: Optional[str] = None,
        templates_dirpath: Optional[str] = None,

):
    templates_dirpath = templates_dirpath or "./nginx_config_templates"
    nginx_filepath = os.path.join(
        nginx_output_dirpath or OPT_OUTPUT_DIRPATH,
        nginx_output_filename or OPT_OUTPUT_FILENAME
    )
    # Verify that the required options (env.vars) are defined.
    if not all([OPTS_PROXY_PASS, OPTS_SERVER_NAME, OPT_PORT]):
        raise ValueError("Missing required env.vars: OPTS_PROXY_PASS, OPTS_VERSER_NAME")
    # Extract the configuration options and verify length match
    opts_proxy_pass = OPTS_PROXY_PASS.split(OPT_ENVSEP)
    opts_server_name = OPTS_SERVER_NAME.split(OPT_ENVSEP)
    if not len(opts_proxy_pass) == len(opts_server_name):
        raise ValueError("Lenght mismatch between proxy-pass and server-names options.")
    # Server configs
    server_template = Template(name="nginx_server_config.txt", dirpath=templates_dirpath)
    server_configs = [
        server_template.apply(
            proxy_pass=proxy_pass,
            server_name=server_name,
            port=OPT_PORT,
        )
        for proxy_pass, server_name in zip(opts_proxy_pass, opts_server_name)
    ]
    if not server_configs:
        raise ValueError("Missing server configs... this shouldn't happen!")
    # NGINX Config
    nginx_template = Template(name="nginx_main_config.txt", dirpath=templates_dirpath)
    nginx_config = nginx_template.apply(
        server_section="\n".join(server_configs)
    )
    # Save nginx configuration
    with open(nginx_filepath, "w") as fh:
        fh.write(nginx_config)


if __name__ == "__main__":
    _, *args = sys.argv
    main(args)
