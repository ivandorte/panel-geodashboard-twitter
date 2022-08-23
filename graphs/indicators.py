import hvplot.pandas
import panel as pn
from pd_utils.utils import filter_df_by_bbox


def get_tweets_nind(in_data, x_range, y_range):
    '''
    Returns a numeric indicator showing
    the number of tweets within the current
    map extent.
    '''

    # Verify whether x_range or y_range are None
    if (x_range, y_range) == (None, None):
        return None

    # Filter the tweet locations by bounding box
    out_data = filter_df_by_bbox(in_data,
                                 x_range,
                                 y_range
                                 )

    # Check if 'out_data' is empty
    if out_data.shape[0] == 0:
        return None

    # Get the number of tweets
    tweets_cnt = out_data.shape[0]

    # Create the numeric indicator
    tweets_nind = pn.indicators.Number(name='Tweets',
                                       value=tweets_cnt,
                                       default_color='white',
                                       title_size='0pt',
                                       font_size='22pt'
                                       )
    return tweets_nind


def get_unique_users_nind(in_data, x_range, y_range):
    '''
    Returns a numeric indicator showing
    the number of Unique Users within the
    current map extent.
    '''

    # Verify whether x_range or y_range are None
    if (x_range, y_range) == (None, None):
        return None

    # Filter the tweet locations by bounding box
    out_data = filter_df_by_bbox(in_data,
                                 x_range,
                                 y_range
                                 )

    # Check if 'out_data' is empty
    if out_data.shape[0] == 0:
        return None

    # Get the number of Unique users
    uu_df = out_data.drop_duplicates(['user_id'])
    uu_cnt = uu_df['user_id'].count()

    # Create the numeric indicator
    uu_nind = pn.indicators.Number(name='Unique Users',
                                   value=uu_cnt,
                                   default_color='white',
                                   title_size='0pt',
                                   font_size='22pt'
                                   )
    return uu_nind
