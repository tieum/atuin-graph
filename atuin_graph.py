#!/usr/bin/env python
"""
atuin_graph.py: standalone script to create a activity png for a user / optional "until" date
"""
import argparse
import os
import matplotlib.pyplot as plt
from generate_calendar import generate_calendar

parser = argparse.ArgumentParser()
parser.add_argument(
    "--user", help="mandatory - user to draw the graph for", required=True
)
parser.add_argument(
    "--until",
    help="optional - day (yyyy-mm-dd) to query until, used for gif generation",
)
parser.add_argument("--atuin_server_config", help="optional - atuin server config path")
args = parser.parse_args()

if args.atuin_server_config:
    config = args.atuin_server_config
else:
    config = os.environ["HOME"] + "/.config/atuin/server.toml"

generate_calendar(config, args.user, args.until)

if args.until:
    plt.savefig(f"atuin-{args.user}-{args.until}.png", bbox_inches="tight")
else:
    plt.savefig(f"atuin-{args.user}.png", bbox_inches="tight")
plt.close()
