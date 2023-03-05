import holoviews as hv
import numpy as np
from bokeh.models import HoverTool
from pd_utils.utils import filter_df_by_bbox

LINE_COLOR = "#27aeef"


def get_daily_tweets(in_data, x_range, y_range):
    """
    Returns a line plot showing the number of tweets
    per day within the current map extent.
    """

    # Verify whether x_range or y_range are None
    if (x_range, y_range) == (None, None):
        return None

    # Filter the tweet locations by bounding box
    out_data = filter_df_by_bbox(in_data, x_range, y_range)

    # Check if out_data is empty
    if out_data.shape[0] == 0:
        return None

    # Define a custom Hover tool
    tweets_hover = HoverTool(
        tooltips=[("Day", "@tweet_date{%F}"), ("Tweets", "@tweet_id")],
        formatters={"@tweet_date": "datetime"},
        point_policy="follow_mouse",
    )

    # Get the number of tweets on daily basis
    tweets_df = out_data.resample("D")["tweet_id"].count()
    tweets_df = tweets_df.replace(0, np.nan)
    tweets_df = tweets_df.reset_index()

    # Number of tweets
    total_tweets = tweets_df["tweet_id"].sum()

    # Create the line plot
    tweets_plt = hv.Curve(tweets_df)

    # Additional plot options
    tweets_plt.opts(
        title=f"Total: {int(total_tweets)}",
        color=LINE_COLOR,
        tools=[tweets_hover],
        alpha=0.7,
        xlabel="Time [Days]",
        ylabel="Tweets",
        yformatter="%.0f",
    )
    return tweets_plt


def get_daily_unique_users(in_data, x_range, y_range):
    """
    Returns a line plot showing the number of
    Unique users per day within the current
    map extent.
    """

    # Verify whether x_range or y_range are None
    if (x_range, y_range) == (None, None):
        return None

    # Filter the tweet locations by bounding box
    out_data = filter_df_by_bbox(in_data, x_range, y_range)

    # Check if out_data is empty
    if out_data.shape[0] == 0:
        return None

    # Define a custom Hover tool
    uu_hover = HoverTool(
        tooltips=[("Day", "@tweet_date{%F}"), ("Unique Users", "@user_id")],
        formatters={"@tweet_date": "datetime"},
        point_policy="follow_mouse",
    )

    # Get the number of unique users on daily basis
    uu_df = out_data.drop_duplicates(["user_id"])
    uu_df = uu_df.resample("D")["user_id"].count()
    uu_df = uu_df.replace(0, np.nan)
    uu_df = uu_df.reset_index()

    # Number of unique users
    unique_users = uu_df["user_id"].sum()

    # Create the line plot
    uu_plt = hv.Curve(uu_df)

    # Additional plot options
    uu_plt.opts(
        title=f"Total: {int(unique_users)}",
        color=LINE_COLOR,
        tools=[uu_hover],
        alpha=0.7,
        xlabel="Time [Days]",
        ylabel="Unique Users",
        yformatter="%.0f",
    )
    return uu_plt
