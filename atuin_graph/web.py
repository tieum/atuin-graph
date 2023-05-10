"""
Flask app to serve dynamically the png
"""
import os
from io import BytesIO
from flask import Flask, send_file
import matplotlib.pyplot as plt
from atuin_graph.generate_calendar import generate_calendar

app = Flask(__name__)
config = os.environ["HOME"] + "/.config/atuin/server.toml"


@app.route("/<user>", defaults={"date": None})
@app.route("/<user>/<date>")
def serve_png(user, date=None):
    """return a png for a user and an optional date"""
    if generate_calendar(config, user, date):
        img = BytesIO()
        plt.savefig(img, format="png", bbox_inches="tight")
        plt.close()
        img.seek(0)
        return send_file(img, download_name=f"{user}.png", mimetype="image/png")

    return ""


if __name__ == "__main__":
    app.run(host="127.0.0.1", port="8889")
