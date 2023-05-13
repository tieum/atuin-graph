"""
cli.py: standalone script to create a activity png for a user / optional "until" date
"""
import argparse
import os
import matplotlib.pyplot as plt
from atuin_graph.generate_calendar import generate_calendar


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--user", help="user to draw the graph for", required=True)
    parser.add_argument(
        "--from",
        dest="from_",
        metavar="FROM",
        help="day (yyyy-mm-dd) to query from",
    )

    parser.add_argument(
        "--until",
        help="day (yyyy-mm-dd) to query until",
    )

    parser.add_argument("--atuin_server_config", help="atuin server config path")
    args = parser.parse_args()

    if args.atuin_server_config:
        config = args.atuin_server_config
    else:
        config = os.environ["HOME"] + "/.config/atuin/server.toml"

    generate_calendar(config, args.user, args.from_, args.until)

    if args.until:
        plt.savefig(f"atuin-{args.user}-{args.until}.png", bbox_inches="tight")
    else:
        plt.savefig(f"atuin-{args.user}.png", bbox_inches="tight")

    plt.close()


if __name__ == "__main__":
    main()
