import panel as pn
from pd_utils.utils import filter_df_by_bbox


def get_overall_sentiment(in_data, x_range, y_range):
    """
    Returns the overall sentiment (Positive vs Negative)
    within the current map extent.
    """

    # Verify whether x_range or y_range are None
    if (x_range, y_range) == (None, None):
        return None

    # Filter the tweet locations by bounding box
    out_data = filter_df_by_bbox(in_data, x_range, y_range)

    # Check if out_data is empty
    if out_data.shape[0] == 0:
        return None

    # Get the overall sentiment - Positive vs Negative
    sent_df = out_data[out_data["tweet_sentiment"].isin(["positive", "negative"])]

    sent_df = sent_df["tweet_sentiment"].value_counts().reset_index()
    sent_df["pct"] = round((sent_df["count"] / sent_df["count"].sum()) * 100, 2)
    sent_df = sent_df.set_index("tweet_sentiment")

    positive_value = sent_df.loc["positive", "pct"]
    negative_value = sent_df.loc["negative", "pct"]

    sent_plot = {
        "dataset": [
            {
                "source": [
                    ["sentiment", "count", "text", "emoji"],
                    ["Positive", positive_value, f"{positive_value}%", "😄"],
                    ["Negative", negative_value, f"{negative_value}%", "🙁"],
                ]
            }
        ],
        "tooltip": {"trigger": "item"},
        "legend": {
            "bottom": "5%",
            "left": "center",
            "selectedMode": "false",
            "textStyle": {"color": "#ccc"},
        },
        "series": [
            {
                "name": "Sentiment",
                "type": "pie",
                "radius": ["40%", "70%"],
                "color": ["#009988", "#EECC66"],
                "avoidLabelOverlap": "false",
                "label": {
                    "show": "false",
                    "fontSize": "40",
                    "position": "center",
                    "formatter": "{@emoji}",
                },
                "encode": {
                    "value": "count",
                    "itemName": "sentiment",
                    "tooltip": ["text"],
                },
            }
        ],
    }

    return pn.pane.ECharts(dict(sent_plot, responsive=True))
