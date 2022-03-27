import dash
import numpy as np
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import plotly.graph_objs as go
import pandas as pd
import folium

# get help from installed module:
# in terminal
# import dash_html_components as html
# print(help(html.Div))

# load a file
df = pd.read_csv("_59THST_midtown_timebins_sum_grater10_sort.csv")

# Объекты Dash Slider имеют дело только с int/ float,
# поэтому вам нужно сначала преобразовать даты int,
# такие как метки времени Unix / epoch, а затем
# сопоставить метки с любым strформатом даты, который вы пожелаете.
# df['epoch_dt'] = df['TIME'].astype(np.int64) // 1e9

# launch app
app = dash.Dash()

# from https://dash.plot.ly/dash-core-components/dropdown
# Crate a dash layout that con tains a Graph component
hour_options = []
for hour in df["HODBIN2"].unique():
    hour_options.append({"label": str(hour), "value": hour})


daymap = {
    "Sunday": 0,
    "Monday": 1,
    "Tuesday": 2,
    "Wednesdays": 3,
    "Thursday": 4,
    "Friday": 5,
    "Saturday": 6,
}
weekdays = list(df["WEEKDAY"])


app.layout = html.Div(
    [
        html.H1("Midtown, NYC: MTA Entries vs Exsits"),
        dcc.Slider(
            id="hour-slider2",
            min=df["HODBIN2"].min(),
            marks={
                str(time): str(time) + " o'clock" for time in df["HODBIN2"].unique()
            },
            value=df["HODBIN2"].min(),
            max=df["HODBIN2"].max(),
            step=None,
        ),
        html.Iframe(
            id="map", srcDoc=open("Map4.html", "r").read(), width="100%", height="300"
        ),
        dcc.Graph(id="graph2"),
        dcc.Graph(id="graph"),
        dcc.Slider(
            id="hour-slider",
            min=df["HODBIN2"].min(),
            max=df["HODBIN2"].max(),
            value=df["HODBIN2"].min(),
            marks={
                str(time): str(time) + " o'clock" for time in df["HODBIN2"].unique()
            },
            step=None,
        ),
    ]
)


@app.callback(Output("graph", "figure"), [Input("hour-slider", "value")])
def update_figure(selected_time):
    filtered_df = df[df["HODBIN2"] == selected_time]
    traces = []
    for station_name in filtered_df["station_id"].unique():
        df_by_station = filtered_df[filtered_df["station_id"] == station_name]
        traces.append(
            go.Scatter(
                y=df_by_station["ENTRIES_diff_sum"],
                x=df_by_station["WEEKDAY"],
                text=df_by_station["HODBIN2"],
                mode="lines+markers",
                opacity=0.8,
                marker={"size": 7, "line": {"width": 0.5, "color": "blue"}},
                name=station_name + " (ENTRIES)",
            )
        )
    for station_name in filtered_df["station_id"].unique():
        df_by_station = filtered_df[filtered_df["station_id"] == station_name]
        traces.append(
            go.Scatter(  # maybe use Bar
                y=df_by_station["EXITS_diff_sum"],
                x=df_by_station["WEEKDAY"],
                text=df_by_station["HODBIN2"],
                mode="lines",
                opacity=0.6,
                marker={"size": 9, "line": {"width": 0.5, "color": "red"}},
                name=station_name + " (EXITS)",
            )
        )

    return {
        "data": traces,
        "layout": go.Layout(
            yaxis={
                "type": "log",
                "title": "Midtown: Number of People through Entries & Exits",
            },
            xaxis={"title": "Weekday"},
            hovermode="closest",
        ),
    }


data_map = pd.read_csv("_59THST_midtown_timebins_sum_grater10_sort.csv")
lat = list(data_map["LAT"])
lon = list(data_map["LON"])
exits = list(data_map["EXITS_diff_sum"])
entries = list(data_map["ENTRIES_diff_sum"])
station = list(data_map["station_id"])


def color_producer_ex(exits):
    if exits < 1000:
        return "green"
    elif 100 <= exits < 10000:
        return "orange"
    else:
        return "red"


map = folium.Map(location=[40.762796, -73.967686], zoom_start=12, tiles="Stamen Toner")


def color_producer_ent(entries):
    if entries < 1000:
        return "blue"
    elif 100 <= entries < 10000:
        return "yellow"
    else:
        return "pink"


@app.callback(Output("graph2", "figure"), [Input("hour-slider2", "value")])
def update_figure_map(selected_time):
    filtered_df = df[df["HODBIN2"] == selected_time]
    fgv = folium.FeatureGroup(name="MTA_Exits")
    for lt, ln, ex, st in zip(lat, lon, exits, station):
        fgv.add_child(
            folium.CircleMarker(
                location=[lt, ln],
                radius=ex / 500,
                popup=str(ex) + " ppl Exit @ " + (st),
                fill_color=color_producer_ex(ex),
                fill=False,
                color="red",
                fill_opacity=0.1,
            )
        )

    fgp = folium.FeatureGroup(name="MTA_Entries")
    for lt, ln, en, st in zip(lat, lon, entries, station):
        fgp.add_child(
            folium.CircleMarker(
                location=[lt, ln],
                radius=en / 500,
                popup=str(en) + " ppl Enter @" + (st),
                fill_color=color_producer_ent(en),
                fill=False,
                color="green",
                fill_opacity=0.2,
            )
        )

    map.add_child(fgv)
    map.add_child(fgp)
    map.add_child(folium.LayerControl())

    # map.save('Map4.html')
    return map


if __name__ == "__main__":
    app.run_server(debug=True)
