import panel as pn

no_data_config = {
    "resizeit": {"disable": "true"},
    "animateIn": "jsPanelFadeIn",
    "animateOut": "jsPanelFadeOut",
    "autoclose": {
        "time": "4s",
    },
    "headerControls": {
        "maximize": "remove",
        "normalize": "remove",
        "minimize": "remove",
        "smallify": "remove",
    },
}

NO_DATA_PANE = pn.layout.FloatPanel(
    "No data to display 🙁",
    name="Warning ⚠️",
    position="center",
    theme="warning",
    contained=False,
    margin=20,
    config=no_data_config,
)
