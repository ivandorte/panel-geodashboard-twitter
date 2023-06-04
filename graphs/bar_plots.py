import hvplot.pandas  # noqa
import pandas as pd
import panel as pn
from bokeh.models import HoverTool, WheelZoomTool
from pd_utils.utils import filter_df_by_bbox

BAR_COLOR = "#03DAC6"

# An empty bar plot
EMPTY_DF = pd.DataFrame([[None, None]], columns=["index", "tweet_lang"])
EMPTY_BAR_PLOT = EMPTY_DF.hvplot.bar(
    title="",
    x="index",
    y="tweet_lang",
    xlabel="Language",
    ylabel="Tweets",
    min_height=300,
    min_width=300,
    responsive=True,
)


def get_top5_langs(in_data, x_range, y_range):
    """
    Returns a bar plot showing the top 5
    languages within the current map extent.
    """

    def hook(plot, element):
        """
        Custom hook for disabling zoom on axis
        """

        # Disable zoom on axis
        for tool in plot.state.toolbar.tools:
            if isinstance(tool, WheelZoomTool):
                tool.zoom_on_axis = False
                break

    # Filter the tweet locations by bounding box
    out_data = filter_df_by_bbox(in_data, x_range, y_range)

    # Check if out_data is empty
    if out_data.shape[0] == 0:
        # Show a notification if there is no data to display
        pn.state.notifications.warning("No Data to Display.", duration=2500)
        return EMPTY_BAR_PLOT

    # Define a custom Hover tool for the bar plot
    lang_hover = HoverTool(
        tooltips=[("Language", "@index"), ("Tweets", "@tweet_lang")],
        point_policy="follow_mouse",
    )

    # Get the top 5 most common languages
    lang_df = out_data["tweet_lang"].value_counts().head(5).to_frame()
    lang_df = lang_df.reset_index()

    # Create the bar plot
    lang_plt = lang_df.hvplot.bar(
        title="",
        x="index",
        y="tweet_lang",
        xlabel="Language",
        ylabel="Tweets",
        yformatter="%.0f",
        line_width=0,
        color=BAR_COLOR,
        tools=[lang_hover],
        alpha=0.7,
        min_height=300,
        min_width=300,
        responsive=True,
    ).opts(hooks=[hook])

    return lang_plt
