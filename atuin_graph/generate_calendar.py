"""
generate_calendar.py: function generating the calendar
"""
import tomllib
import matplotlib.pyplot as plt
import calplot
import numpy as np
import pandas as pd
from sqlalchemy import create_engine


def generate_calendar(config, user, from_, until):
    """get the data from pg and generate the calendar"""
    with open(config, "rb") as f:
        serverconf = tomllib.load(f)

    # for it to work db_uri in server.toml has to start with postgresql://
    # sqlalchemy will fail with the postgres:// prefix
    engine = create_engine(serverconf["db_uri"])

    params = {"user": user}
    sql_query = (
        "select h.timestamp::date as timestamp, count(h.timestamp) as activity "
        "from history h "
        "inner join users u on h.user_id=u.id "
        "where u.username = %(user)s"
    )
    if from_:
        params["from"] = from_
        sql_query += " and h.timestamp::date >= %(from)s"

    if until:
        params["until"] = until
        sql_query += " and h.timestamp::date <= %(until)s"

    sql_query += " group by timestamp::date order by timestamp"

    try:
        df = pd.read_sql_query(sql_query, con=engine, params=params)
    except Exception as e:
        print(e)
        return False

    if df.empty:
        print(f"no data found for user: {user} / from: {from_} / until: {until}")
        return False
    df["timestamp"] = pd.to_datetime(df["timestamp"])
    df.set_index("timestamp", inplace=True)

    # get longest streak
    # taken from https://stackoverflow.com/q/23514336
    df = df.resample("D").sum()  # add missing dates to df
    df.replace(0, np.nan, inplace=True)
    dfseries = (df.notnull().shift(1) != df.notnull()).cumsum()
    dfseries[df.isnull()] = np.nan
    dfseries = dfseries.dropna(axis=0, how="any")
    dfrng = pd.concat(
        (
            dfseries.apply(lambda x: x.groupby(x.values).cumcount().max()),
            dfseries.apply(lambda x: x.groupby(x.values).cumcount().idxmax()),
        ),
        axis=1,
        keys=["Length", "EndPos"],
    )
    dfrng["Length"] = dfrng.Length + 1

    # get highest activity
    highest_activity = df[df["activity"] == df["activity"].max()]
    highest_value = int(highest_activity.iloc[0].item())
    highest_date = highest_activity.index[0]

    # draw it with calplot
    calplot.calplot(
        df["activity"],
        dropzero=True,
        edgecolor=None,
        cmap="YlGn",
        colorbar=False,
        suptitle="Shell history",
        yearlabel_kws={"fontname": "sans-serif"},
        daylabels=["Mon", "", "Wed", "", "Fri", "", "Sun"],
    )
    plt.xlabel(
        "Longest Streak: %s Days \nHighest Activity: %s (%s)"
        % (
            str(dfrng["Length"][0]),
            highest_date.strftime("%a %d %B"),
            str(highest_value),
        ),
        loc="left",
        family="monospace",
    )
    return True
