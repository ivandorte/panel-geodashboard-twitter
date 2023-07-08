import os

import holoviews as hv
import panel as pn
from dialogs.alert_panes import NO_DATA_PANE
from graphs.bar_plots import get_top5_langs
from graphs.hashtags_plot import get_top10_hashtags
from graphs.line_plots import get_daily_tweets, get_daily_unique_users
from graphs.sentiment_plots import get_overall_sentiment
from graphs.tweet_map import get_tweet_map, get_tweet_points
from holoviews import streams
from pd_utils.utils import filter_df_by_bbox, get_hashtags_df, load_data

# Load the bokeh extension
hv.extension("bokeh")

# Disable webgl: https://github.com/holoviz/panel/issues/4855
hv.renderer("bokeh").webgl = False  # Disable Webgl

pn.extension("echarts", "floatpanel", notifications=True)


def show_nodata_message(x_range, y_range):
    """
    Displays a notification if no data is found
    """

    out_data = filter_df_by_bbox(twitter_data, x_range, y_range)
    if len(out_data) == 0:
        # FIXME: Notifications are not working
        # pn.state.notifications.warning("No data to display 🙁", duration=4000)

        twitter_geodashboad.modal[0].clear()
        twitter_geodashboad.modal[0].append(NO_DATA_PANE)
        twitter_geodashboad.open_modal()
        twitter_geodashboad.close_modal()  # Hack


# Twitter logo
TWITTER_LOGO = os.path.join("assets", "images", "Twitter-logo.svg")

# Input Twitter data
IN_TWITTER_DATA = os.path.join("data", "rome_tweets.parquet")


# Load tweet locations and hashtags as a DataFrame
twitter_data = load_data(IN_TWITTER_DATA)

# Load tweet hashtags as a DataFrame
hashtags_data = get_hashtags_df(twitter_data)

# Get a rasterized point plot showing the tweet locations
tweets_pts = get_tweet_points(twitter_data)

# Define a RangeXY stream linked to the tweet locations
range_xy = streams.RangeXY(source=tweets_pts)
range_xy.add_subscriber(show_nodata_message)

# Get the tweet map
tweet_map = get_tweet_map(tweets_pts)

# Top 5 languages
top5_languages = hv.DynamicMap(
    pn.bind(
        get_top5_langs,
        in_data=twitter_data,
        x_range=range_xy.param.x_range,
        y_range=range_xy.param.y_range,
    )
)

# Overall Sentiment
overall_sentiment = pn.bind(
    get_overall_sentiment,
    in_data=twitter_data,
    x_range=range_xy.param.x_range,
    y_range=range_xy.param.y_range,
)

# Top 10 hashtags - wordcloud image
top10_hashtags = pn.bind(
    get_top10_hashtags,
    in_data=hashtags_data,
    x_range=range_xy.param.x_range,
    y_range=range_xy.param.y_range,
)

# Number of tweets (daily)
tweets_daily = hv.DynamicMap(
    pn.bind(
        get_daily_tweets,
        in_data=twitter_data,
        x_range=range_xy.param.x_range,
        y_range=range_xy.param.y_range,
    )
)

# Number of unique users (daily)
unique_users_daily = hv.DynamicMap(
    pn.bind(
        get_daily_unique_users,
        in_data=twitter_data,
        x_range=range_xy.param.x_range,
        y_range=range_xy.param.y_range,
    )
)

# Second tab - Top 5 Languages, Top 10 Hashtags
top5_10_tabs = pn.Tabs(
    ("Top 5 Languages", top5_languages),
    ("Top 10 Hashtags", top10_hashtags),
    ("Overall sentiment", overall_sentiment),
)

# Third tab - Daily data (Tweets, Unique users)
daily_plots_tabs = pn.Tabs(
    ("Tweets", tweets_daily),
    ("Unique Users", unique_users_daily),
)

# Compose the layout
layout = pn.Column(pn.Row(tweet_map, top5_10_tabs), daily_plots_tabs)

# Create the dashboard and turn into a deployable application
twitter_geodashboad = pn.template.FastListTemplate(
    site="",
    title="Twitter Dashboard - Rome (2018)",
    theme="dark",
    theme_toggle=False,
    logo=TWITTER_LOGO,
    main=[layout],
    modal=[pn.Row()],
).servable()
