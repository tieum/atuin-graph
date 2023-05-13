# atuin-graph
activity graph for [atuin](https://atuin.sh) self hosted sync server

<img src="https://github.com/tieum/atuin-graph/raw/main/img/shell.history.gif">

It connects to the PostgreSQL atuin database, using by default the `db_uri` setting from atuin `server.toml` config file

Two ways to run it are available, whether in command line or as a flask web application

Required Python version: >= 3.11 (uses the [tomllib parser](https://docs.python.org/3/library/tomllib.html))

## installation

```bash
pip install atuin-graph
```

## cli / standalone
***- `atuin-graph`***: takes a username as input and outputs a `atuin-{user}.png` file

The `-until` and `--from` parameters allow to query from / up to a specified date, this is useful to create one png per day and create a gif with `imagemagick` for example (`convert -delay 10 -loop 1 *.png atuin.gif`)

```bash
atuin-graph -h
usage: atuin-graph [-h] --user USER [--from FROM] [--until UNTIL] [--atuin_server_config ATUIN_SERVER_CONFIG]

options:
  -h, --help            show this help message and exit
  --user USER           user to draw the graph for
  --from FROM           day (yyyy-mm-dd) to query from
  --until UNTIL         day (yyyy-mm-dd) to query until
  --atuin_server_config ATUIN_SERVER_CONFIG
                        atuin server config path
```
##  web app
This package also ships a Flask app which dynamically serves a png for a given user and optional dates

 |📅️ | |
|--------------- | --------------- |
|from a date| `https://my-atuin-server/graph/username/from/yyyy-mm-dd`|
|until a date| `https://my-atuin-server/graph/username/until/yyyy-mm-dd` <br/> `https://my-atuin-server/graph/username/yyyy-mm-dd` |
|between dates| `https://my-atuin-server/graph/username/yyyy-mm-dd/yyyy-mm-dd`|


one way to run it:

```bash
GUNICORN_CMD_ARGS="--bind=127.0.0.1:8889" SCRIPT_NAME=/graph gunicorn atuin_graph.web:app
```

and on nginx side

	location /graph {
	
                proxy_bind              $server_addr;
                proxy_pass              http://127.0.0.1:8889;
        }


