import plotly.express as px
import pandas as pd
def plotting(title, data, x, y, x_label, y_label):
    """General function to plot the Power data."""
    fig = px.line(data, x=data[x], y=data[y], labels={x: x_label, y: y_label})
    fig.update_layout(template="simple_white", font=dict(size=18),
                      title_text=title, width=650,
                      title_x=0.5, height=400)
    fig.show()
# Take the seasonal difference and plot it
data_external["power_Season_Diff"] = data_external["power_output_100"].diff(periods=12)
plotting(title='Power Ouput', data=data_external, x='rtc', y='power_Season_Diff',
         x_label='Date', y_label='Power Output<br>Seasonal Difference')