from collections import Counter
from itertools import chain

import hvplot.pandas
import matplotlib.pyplot as plt
import panel as pn
from matplotlib.figure import Figure
from pd_utils.utils import filter_df_by_bbox
from wordcloud import WordCloud

# Set the plot backgroud color to dark
plt.style.use('dark_background')


def get_top10_hashtags(in_data, x_range, y_range):
    '''
    Returns a matplotlib pane with a wordcloud image
    showing the top 10 hashtags within the current
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

    # Get the top 10 hashtags as a dictionary
    hash_cnt = Counter(chain(out_data['tweet_hashtags']))
    hash_cnt = dict(hash_cnt.most_common(10))

    # Generate the word cloud image from the dictionary
    wordcloud = WordCloud(background_color='black',
                          collocations=False,
                          colormap='Paired'
                          )

    wordcloud.generate_from_frequencies(hash_cnt)

    # Plot the image using matplotlib
    fig = Figure(facecolor='#3f3f3f')
    ax = fig.add_subplot(111)
    ax.imshow(wordcloud, interpolation='bilinear')
    ax.axis("off")

    # Add the image to the matplotlib pane
    hashtags_fig = pn.pane.Matplotlib(fig,
                                      height=400,
                                      width=700,
                                      tight=True,
                                      dpi=72,
                                      interactive=False
                                      )
    return hashtags_fig
