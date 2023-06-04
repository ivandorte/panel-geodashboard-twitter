from collections import Counter
from itertools import chain

import panel as pn
from bs4 import BeautifulSoup
from pd_utils.utils import filter_df_by_bbox
from wordcloud import WordCloud


def get_top10_hashtags(in_data, x_range, y_range):
    """
    Returns an SVG pane with a wordcloud image
    showing the top 10 hashtags within the current
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

    # Get the top 10 hashtags as a dictionary
    hash_cnt = Counter(chain(out_data["tweet_hashtags"]))
    hash_cnt = dict(hash_cnt.most_common(10))

    # Generate the word cloud image from the dictionary
    wordcloud = WordCloud(
        background_color="black",
        collocations=False,
        colormap="viridis",
        mode="RGBA",
    )

    wordcloud.generate_from_frequencies(hash_cnt)
    svg = wordcloud.to_svg(embed_font=True)

    # Modify the SVG s to fit the SVG pane
    svg_soup = BeautifulSoup(svg, "xml")
    svg_width = svg_soup.find("svg")["width"]
    svg_height = svg_soup.find("svg")["height"]
    svg_soup.svg["width"] = "100%"
    svg_soup.svg["height"] = "100%"
    svg_soup.svg["viewBox"] = f"0 0 {svg_width} {svg_height}"
    svg = str(svg_soup.contents[0])

    hashtags_fig = pn.pane.SVG(svg, sizing_mode="stretch_both")

    return hashtags_fig
