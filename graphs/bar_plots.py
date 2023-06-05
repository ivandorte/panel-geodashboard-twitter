import hvplot.pandas  # noqa
from bokeh.models import HoverTool, WheelZoomTool
from graphs.no_data_utils import EMPTY_BAR_PLOT, get_no_data_msg
from pd_utils.utils import filter_df_by_bbox

BAR_COLOR = "#03DAC6"


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
        get_no_data_msg()
        return EMPTY_BAR_PLOT

    # Define a custom Hover tool for the bar plot
    lang_hover = HoverTool(
        tooltips=[("Language", "@tweet_lang"), ("Tweets", "@count")],
        point_policy="follow_mouse",
    )

    # Get the top 5 most common languages
    lang_df = out_data["tweet_lang"].value_counts().head(5).to_frame()
    lang_df = lang_df.reset_index()

    # Create the bar plot
    lang_plt = lang_df.hvplot.bar(
        title="",
        x="tweet_lang",
        y="count",
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
