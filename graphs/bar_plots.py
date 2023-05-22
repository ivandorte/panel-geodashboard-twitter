import holoviews as hv
import panel as pn
from bokeh.models import HoverTool, WheelZoomTool
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

    # Verify whether x_range or y_range are None
    if (x_range, y_range) == (None, None):
        return None

    # Filter the tweet locations by bounding box
    out_data = filter_df_by_bbox(in_data, x_range, y_range)

    # Check if out_data is empty
    if out_data.shape[0] == 0:
        return None

    # Define a custom Hover tool for the bar plot
    lang_hover = HoverTool(
        tooltips=[("Language", "@index"), ("Tweets", "@tweet_lang")],
        point_policy="follow_mouse",
    )

    # Get the top 5 most common languages
    lang_df = out_data["tweet_lang"].value_counts().head(5)

    # Create the bar plot
    lang_plt = hv.Bars(lang_df)

    # Additional plot options
    lang_plt.opts(
        title="",
        xlabel="Language",
        ylabel="Tweets",
        line_width=0,
        color=BAR_COLOR,
        hooks=[hook],
        tools=[lang_hover],
        alpha=0.7,
        yformatter="%.0f",
    )
    return pn.panel(lang_plt, sizing_mode="stretch_both")
