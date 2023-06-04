import os

import holoviews as hv
import panel as pn
from graphs.bar_plots import get_top5_langs
from graphs.hashtags_plot import get_top10_hashtags
from graphs.line_plots import get_daily_tweets, get_daily_unique_users
from graphs.tweet_map import get_tweet_map, get_tweet_points
from holoviews import streams
from pd_utils.utils import get_hashtags_df, load_data

pn.extension(notifications=True)

# Load the bokeh extension
hv.extension("bokeh")

# Disable webgl: https://github.com/holoviz/panel/issues/4855
hv.renderer("bokeh").webgl = False  # Disable Webgl

# Twitter logo
TWITTER_LOGO = os.path.join("assets", "images", "Twitter-logo.svg")

# Input Twitter data
IN_TWITTER_DATA = os.path.join("data", "rome_tweets.parquet")


def create_twitter_dashboard():
    """
    This function creates the main Twitter dashboard
    """

    # Load tweet locations and hashtags as a DataFrame
    twitter_data = load_data(IN_TWITTER_DATA)

    # Load tweet hashtags as a DataFrame
    hashtags_data = get_hashtags_df(twitter_data)

    # Get a rasterized point plot showing the tweet locations
    tweets_pts = get_tweet_points(twitter_data)

    # Define a RangeXY stream linked to the tweet locations
    range_xy = streams.RangeXY(source=tweets_pts)

    # Get the tweet map
    tweet_map = get_tweet_map(tweets_pts)

    # Top 5 languages - Connect the bar plot to the RangeXY stream
    top5_languages = hv.DynamicMap(
        pn.bind(
            get_top5_langs,
            in_data=twitter_data,
            x_range=range_xy.param.x_range,
            y_range=range_xy.param.y_range,
        )
    )

    # Top 10 hashtags - Connect the wordcloud image to the RangeXY stream
    top10_hashtags = pn.bind(
        get_top10_hashtags,
        in_data=hashtags_data,
        x_range=range_xy.param.x_range,
        y_range=range_xy.param.y_range,
    )

    # Number of tweets (daily) - Connect the line plot to the RangeXY stream
    tweets_daily = hv.DynamicMap(
        pn.bind(
            get_daily_tweets,
            in_data=twitter_data,
            x_range=range_xy.param.x_range,
            y_range=range_xy.param.y_range,
        )
    )

    # Number of unique users (daily) - Connect the line plot to the RangeXY stream
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
    )

    # Third tab - Daily data (Tweets, Unique users)
    daily_plots_tabs = pn.Tabs(
        ("Tweets", tweets_daily),
        ("Unique Users", unique_users_daily),
    )

    # Compose the layout
    layout = pn.Column(pn.Row(tweet_map, top5_10_tabs), daily_plots_tabs)

    # Inizialize the MaterialTemplate
    tw_tmpl = pn.template.FastListTemplate(
        site="",
        title="Twitter Dashboard - Rome (2018)",
        theme="dark",
        theme_toggle=False,
        logo=TWITTER_LOGO,
        main=[layout],
    )

    return tw_tmpl


if __name__.startswith("bokeh"):
    # Create the dashboard and turn into a deployable application
    twitter_geodashboad = create_twitter_dashboard()
    twitter_geodashboad.servable()
