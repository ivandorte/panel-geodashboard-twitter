import pandas as pd


def load_data(data_path):
    '''
    This function read the Twitter data (parquet file format)
    from the file path and returns a DataFrame.
    '''

    # Required columns
    columns = ['user_id',
               'tweet_id',
               'tweet_hashtags',
               'tweet_lang',
               'tweet_date',
               'x',
               'y']

    # Read the parquet dataset
    out_data = pd.read_parquet(data_path,
                               columns=columns)
    return out_data


def get_hashtags_df(in_data):
    '''
    This function returns an exploded DataFrame
    containing the hashtags with their x/y coordinates.
    '''

    # Select the required columns
    columns = ['x', 'y', 'tweet_hashtags']
    out_data = in_data[columns]

    # Remove rows with empty strings
    out_data = out_data[out_data['tweet_hashtags'].astype(bool)]

    # Convert the hashtag strings to lower
    out_data.loc[:, 'tweet_hashtags'] =\
        out_data['tweet_hashtags'].str.lower()

    # Split the hashtag strings by comma
    out_data.loc[:, 'tweet_hashtags'] =\
        out_data['tweet_hashtags'].str.split(',')

    # Explode list-like elements into rows
    out_data = out_data.explode('tweet_hashtags')
    return out_data


def filter_df_by_bbox(in_data, x_range, y_range):
    '''
    This function filters the rows of the DataFrame
    within a bounding box.
    '''

    out_data = in_data[
        (in_data['x'] > x_range[0]) &
        (in_data['x'] < x_range[1]) &
        (in_data['y'] > y_range[0]) &
        (in_data['y'] < y_range[1])
        ]
    return out_data
