import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.graph_objects as go
import streamlit as st
from typing import List, Dict


def pixels_chart(
          df_emotion: pd.DataFrame,
          df_intensity: pd.DataFrame = None,
          color_dictionary: Dict[str, str] = None
) -> st.plotly_chart:

    """
    Display a heatmap of daily emotions (and optionally intensities) as a pixel chart using seaborn.

    Args:
        df_emotion (pd.DataFrame): DataFrame of emotion codes (numeric or categorical), indexed by day, columns as months.
        df_intensity (pd.DataFrame, optional): DataFrame of emotion intensities, same shape as df_emotion. If provided, values are annotated on the heatmap.
        color_dictionary (Dict[str, str], optional): Dictionary mapping emotion names or codes to color hex values. Used for the heatmap colormap.

    Returns:
        st.plotly_chart: The rendered Streamlit chart object (actually a matplotlib heatmap rendered via st.pyplot).
    """
    fig, ax = plt.subplots(figsize=(10, 10))
    annot = None
    if df_intensity is not None:
        annot = (
            df_intensity.transpose()
            .replace('0', '')
            .replace('Missing', '')
            .replace(':|', '')
        )
    ax = sns.heatmap(
        df_emotion.transpose(),
        cmap=list(color_dictionary.values()),
        cbar=False,
        linewidths=1.4,
        linecolor='white',
        square=True,
        vmin=0,
        vmax=len(color_dictionary),
        xticklabels=1,
        annot=annot,
        fmt='',
        ax=ax
    )
    ax.set_yticklabels(
        labels=['J', 'F', 'M', 'A', 'M', 'J', 'J', 'A', 'S', 'O', 'N', 'D'],
        rotation=0, fontsize=8
    )
    ax.set_xticklabels(labels=list(df_emotion.index), rotation=0, fontsize=8)
    ax.set_xlabel('')
    ax.tick_params(axis='x', colors="#444")
    ax.tick_params(axis='y', colors="#444")
    # Hide figure background
    for item in [fig, ax]:
        item.patch.set_visible(False)
    return st.pyplot(fig, dpi=1000, use_container_width=True)

def days_emotion_chart(
        df_days_counts: pd.DataFrame,
        perc_feature: str,
        days_list: List[str],
        emotions_list: List[str],
        config_modebar: Dict[str, bool]
) -> st.plotly_chart:
    """
    Creates a scatter plot that visualizes the distribution of emotions across different weekdays using plotly.

    This function uses Plotly to generate a chart where each marker represents a specific combination
    of emotion and weekday. The size of each marker is determined by the percentage feature from the
    provided DataFrame. The plot is customized for clarity and ease of interpretation, with specific
    focus on the relative frequency of emotions.

    Args:
        df_days_counts (pd.DataFrame): A DataFrame containing the following columns:
            - `weekday`: The day of the week (e.g., Monday, Tuesday, etc.).
            - `emotion`: The emotion corresponding to each day (e.g., Happy, Sad).
            - `emotion_color`: The color assigned to each emotion.
            - `count`: The number of occurrences of each emotion on the given weekday.
        perc_feature (str): The name of the column used to determine the size of each marker based on percentage.
        days_list (List[str]): A sorted list of weekdays (e.g., ["Monday", "Tuesday", ...]).
        emotions_list (List[str]): A sorted list of emotions (e.g., ["Happy", "Sad", ...]).
        config_modebar (Dict[str, bool]): A dictionary specifying the visibility of the plot's modebar tools.
            Example: `{"zoom": True, "pan": False}`.

    Returns:
        st.plotly_chart: A Plotly figure object representing the scatter plot, rendered in Streamlit.
    """

    fig = go.Figure()

    # Add the scatter trace for emotions on different weekdays
    fig.add_trace(
        go.Scatter(
            x=df_days_counts.weekday,
            y=df_days_counts.emotion,
            mode='markers',
            marker=dict(
                symbol='square',
                color=df_days_counts.emotion_color,
                size=df_days_counts[perc_feature],
                sizemode='area',
                sizeref=2.0 * max(df_days_counts[perc_feature]) / (40.0 ** 2),
                sizemin=4
            ),
            text=df_days_counts['count'],  # Hover text: the number of occurrences of each emotion
            hovertemplate=(
                "weekday=%{x}<br>"
                "emotion=%{y}<br>"
                "count=%{text}<br>"  # Absolute count
                "percentage=%{marker.size:.2f}%"  # Size as percentage
            )
        )
    )

    # Set the layout for the plot
    fig.update_layout(
        xaxis=dict(
            categoryorder="array",
            categoryarray=days_list,  # Specify the weekday order
        ),
        yaxis=dict(
            categoryorder="array",
            categoryarray=emotions_list,  # Specify the emotion order
        ),
        autosize=False,
        width=300,  # Fixed width
        height=400,  # Fixed height
        margin=dict(l=0, r=0, t=0, b=60),
        template="plotly_white",  # Clean and minimal design
        scene=dict(aspectmode="cube")  # Equal scaling for both axes
    )

    # Return the plot for rendering in Streamlit
    return st.plotly_chart(fig, config=config_modebar, dpi=500, use_container_width=True)
