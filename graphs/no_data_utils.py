import hvplot.pandas  # noqa
import pandas as pd
import panel as pn

# An empty bar plot
EMPTY_DF = pd.DataFrame([["", 0]], columns=["tweet_lang", "count"])
EMPTY_BAR_PLOT = EMPTY_DF.hvplot.bar(
    title="",
    x="tweet_lang",
    y="count",
    xlabel="Language",
    ylabel="Tweets",
    min_height=300,
    min_width=300,
    responsive=True,
)

# An empty line plot - Daily tweets
EMPTY_DF_DTWS = pd.DataFrame(
    [[pd.to_datetime("01/01/1971"), 0]], columns=["tweet_date", "tweet_id"]
)

EMPTY_LINE_PLOT_DTWS = EMPTY_DF_DTWS.hvplot.line(
    title="Total: 0",
    x="tweet_date",
    y="tweet_id",
    xlabel="Time [Days]",
    ylabel="Tweets",
    min_height=300,
    min_width=300,
    responsive=True,
)

# An empty line plot - Daily Unique users
EMPTY_DF_DUU = pd.DataFrame(
    [[pd.to_datetime("01/01/1971"), 0]], columns=["tweet_date", "user_id"]
)
EMPTY_LINE_PLOT_DUU = EMPTY_DF_DUU.hvplot.line(
    title="Total: 0",
    x="tweet_date",
    y="user_id",
    xlabel="Time [Days]",
    ylabel="Unique Users [UU]",
    min_height=300,
    min_width=300,
    responsive=True,
)


def get_no_data_msg():
    return pn.state.notifications.warning("No Data to Display.", duration=2500)
