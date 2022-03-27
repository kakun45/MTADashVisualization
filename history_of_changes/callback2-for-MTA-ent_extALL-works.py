import dash 
import numpy as np
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import plotly.graph_objs as go
import pandas as pd
#get help from installed module: 
#in terminal
#import dash_html_components as html
#print(help(html.Div))

#Create a file
df = pd.read_csv('_59THST_ALL_diff.csv')

#Объекты Dash Slider имеют дело только с int/ float, 
# поэтому вам нужно сначала преобразовать даты int, 
# такие как метки времени Unix / epoch, а затем 
# сопоставить метки с любым strформатом даты, который вы пожелаете.
#df['epoch_dt'] = df['TIME'].astype(np.int64) // 1e9

#launch app 
app = dash.Dash()

#from https://dash.plot.ly/dash-core-components/dropdown
#Crate a dash layout that con tains a Graph component
hour_options = []
for hour in df['TIME'].unique():
    hour_options.append({'label':str(hour),'value':hour})


app.layout = html.Div([
    dcc.Graph(id='graph'),
    #dcc.Dropdown(id='hour-picker', options=hour_options, value=df['TIME'].min())
    dcc.Slider(id='hour-slider', min=df['HOD'].min(), max=df['HOD'].max(), 
    value=df['HOD'].min(),
    marks={str(time): str(time)+" o'clock" for time in df['HOD'].unique()},
    step=None
    )  
])


@app.callback(Output('graph', 'figure'), [Input('hour-slider', 'value')])
def update_figure(selected_time):
    filtered_df = df[df['HOD'] == selected_time]
    traces = []
    for station_name in filtered_df['STATION'].unique():
        df_by_station = filtered_df[filtered_df['STATION'] == station_name]
        traces.append(go.Scatter(
            x = df_by_station['ENTRIES_diff'],
            y = df_by_station['WEEKDAY'],
            text = df_by_station['TIME'],
            mode = 'markers',
            opacity=0.8,
            marker={'size':11, 'line': {'width': 0.5, 'color': 'blue'}},
            name=station_name
        ))
    for station_name in filtered_df['STATION'].unique():
        df_by_station = filtered_df[filtered_df['STATION'] == station_name]
        traces.append(go.Scatter( #maybe use Bar
            x = df_by_station['EXITS_diff'],
            y = df_by_station['WEEKDAY'],
            text = df_by_station['TIME'],
            mode = 'markers',
            opacity=0.6,
            marker={'size':9, 'line': {'width': 0.5, 'color': 'red'}},
            name=station_name
        ))
    return {
        'data': traces,
        'layout': go.Layout(
            xaxis={'type':'log', 'title':'Entries vs Exits in time stamps'},
            yaxis={'title':'Weekday'},
            hovermode='closest'
        )
    }

if __name__ == '__main__':
    app.run_server(debug=True)
