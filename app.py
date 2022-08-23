import os
import pathlib

import holoviews as hv
import panel as pn
from holoviews import streams

from graphs.bar_plots import get_top5_langs
from graphs.hashtags_plot import get_top10_hashtags
from graphs.indicators import get_tweets_nind, get_unique_users_nind
from graphs.line_plots import get_daily_tweets, get_daily_unique_users
from graphs.tweet_map import get_tweet_map, get_tweet_points
from pd_utils.utils import get_hashtags_df, load_data

# Load the bokeh extension
hv.extension('bokeh')

# Set the sizing mode
pn.extension(sizing_mode='stretch_width')

ROOT = pathlib.Path(__file__).parent

# Twitter logo
TWITTER_LOGO = os.path.join(ROOT,
                            'assets',
                            'images',
                            'Twitter-logo.svg'
                            )


# Input Twitter data
IN_TWITTER_DATA = os.path.join(ROOT,
                               'data',
                               'rome_tweets.parquet'
                               )


def create_twitter_dashboard():
    '''
    This function creates the main Twitter dashboard
    '''

    # Inizialize the MaterialTemplate
    material_tmpl = pn.template.MaterialTemplate(title='Twitter Dashboard',
                                                 theme='dark')

    # Add the twitter logo to the header
    material_tmpl.logo = TWITTER_LOGO

    # Load tweet locations as a DataFrame
    twitter_data = load_data(IN_TWITTER_DATA)

    # Load tweet hashtags as a DataFrame
    hashtags_data = get_hashtags_df(twitter_data)

    # Get a rasterized point plot showing the tweet locations
    tweets_pts = get_tweet_points(twitter_data)

    # Define a RangeXY stream linked to the tweet locations
    rangexy = streams.RangeXY(source=tweets_pts)

    # Get the tweet map
    tweet_map = get_tweet_map(tweets_pts)

    # Top 5 languages - Connect the bar plot to the RangeXY stream
    top5_languages = pn.bind(get_top5_langs,
                             in_data=twitter_data,
                             x_range=rangexy.param.x_range,
                             y_range=rangexy.param.y_range)

    # Top 10 hashtags - Connect the wordcloud image to the RangeXY stream
    top10_hashtags = pn.bind(get_top10_hashtags,
                             in_data=hashtags_data,
                             x_range=rangexy.param.x_range,
                             y_range=rangexy.param.y_range)

    # Number of tweets (daily) - Connect the line plot to the RangeXY stream
    tweets_daily = pn.bind(get_daily_tweets,
                           in_data=twitter_data,
                           x_range=rangexy.param.x_range,
                           y_range=rangexy.param.y_range)

    # Number of unique users (daily) - Connect the line plot to the RangeXY stream
    unique_users_daily = pn.bind(get_daily_unique_users,
                                 in_data=twitter_data,
                                 x_range=rangexy.param.x_range,
                                 y_range=rangexy.param.y_range)

    # Number of tweets - Connect the indicator to the RangeXY stream
    tweets_nind = pn.bind(get_tweets_nind,
                          in_data=twitter_data,
                          x_range=rangexy.param.x_range,
                          y_range=rangexy.param.y_range)

    # Number of unique users - Connect the indicator to the RangeXY stream
    unique_users_nind = pn.bind(get_unique_users_nind,
                                in_data=twitter_data,
                                x_range=rangexy.param.x_range,
                                y_range=rangexy.param.y_range)

    # First tab - Numeric indicators (Tweets, Unique users)
    num_ind_tabs = pn.Tabs(('Tweets', tweets_nind),
                           ('Unique Users', unique_users_nind),
                           tabs_location='above')

    # Second tab - Top 5 Languages, Top 10 Hashtags
    top5_10_tabs = pn.Tabs(('Top 5 Languages', top5_languages),
                           ('Top 10 Hashtags', top10_hashtags))

    # Third tab - Daily data (Tweets, Unique users)
    daily_plots_tabs = pn.Tabs(('Tweets', tweets_daily),
                               ('Unique Users', unique_users_daily))

    # Add the tweet map tabs to a card container
    tweet_map_card = pn.Card(tweet_map,
                             num_ind_tabs,
                             hide_header=True,
                             collapsible=False
                             )

    # Add the second tabs to a card container
    top5_10_card = pn.Card(top5_10_tabs,
                           hide_header=True,
                           collapsible=False)

    # Add the third tabs to a card container
    daily_plots_card = pn.Card(daily_plots_tabs,
                               hide_header=True,
                               collapsible=False)

    # Compose the layout
    material_tmpl.main.append(pn.Row(tweet_map_card,
                                     top5_10_card))
    material_tmpl.main.append(daily_plots_card)

    return material_tmpl


if __name__.startswith('bokeh'):
    # Create the dashboard and turn into a deployable application
    twitter_geodashboad = create_twitter_dashboard()
    twitter_geodashboad.servable()
