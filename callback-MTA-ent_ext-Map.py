import dash 
import numpy as np
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import plotly.graph_objs as go
import pandas as pd
import folium
#get help from installed module: 
#in terminal
#import dash_html_components as html
#print(help(html.Div))

#load a file
#df = pd.read_csv('_59THST_midtown_diff.csv') #works
#df = pd.read_csv('_59THST_midtown_timebins.csv') #works
#df = pd.read_csv('_59THST_midtown_timebins_sum.csv') #works
#df = pd.read_csv('_59THST_midtown_timebins_sum_grater10.csv') #works
df = pd.read_csv('_midtown_timebins_sum_grater16_sort.csv') # final works


#launch app 
app = dash.Dash()

#from https://dash.plot.ly/dash-core-components/dropdown
#Crate a dash layout that con tains a Graph component
hour_options = []
for hour in df['HODBIN2'].unique():
    hour_options.append({'label':str(hour),'value':hour})


daymap = { "Sunday": 0, "Monday": 1, "Tuesday": 2, "Wednesdays": 3, "Thursday": 4, "Friday": 5, "Saturday": 6}
weekdays = list(df['WEEKDAY'])


app.layout = html.Div([
    html.H1('Midtown, NYC: MTA Entries vs Exsits 10/12/2019 - 10/18/2019'),
    dcc.Slider(id='hour-slider2', min=df['HODBIN2'].min(),
        marks={str(time): str(time)+" o'clock" for time in df['HODBIN2'].unique()},
        value=df['HODBIN2'].min(),
        max = df['HODBIN2'].max(), step=None
    ),
    html.Iframe(id='map', srcDoc=open('Map5.html', 'r').read(), width = '100%', height='300', style={'border':'none'}),
    dcc.Graph(id='graph'),
    dcc.Slider(id='hour-slider', min=df['HODBIN2'].min(), max=df['HODBIN2'].max(), 
    value=df['HODBIN2'].min(),
    marks={str(time): str(time)+" o'clock" for time in df['HODBIN2'].unique()},
    step=None
    )  
])


@app.callback(Output('graph', 'figure'), [Input('hour-slider', 'value')])
def update_figure(selected_time):
    filtered_df = df[df['HODBIN2'] == selected_time]
    traces = []
    for station_name in filtered_df['station_id'].unique():
        df_by_station = filtered_df[filtered_df['station_id'] == station_name]
        traces.append(go.Scatter(
            y = df_by_station['ENTRIES_diff_sum'],
            x = df_by_station['WEEKDAY'],
            text = df_by_station['HODBIN2'],
            mode = 'lines+markers',
            opacity=0.8,
            marker={'size':7, 'line': {'width': 0.5, 'color': 'blue'}},
            name=station_name + ' (ENTRIES)'
        ))
    for station_name in filtered_df['station_id'].unique():
        df_by_station = filtered_df[filtered_df['station_id'] == station_name]
        traces.append(go.Scatter( #maybe use Bar
            y = df_by_station['EXITS_diff_sum'],
            x = df_by_station['WEEKDAY'],
            text = df_by_station['HODBIN2'],
            mode = 'lines',
            opacity=0.6,
            marker={'size':9, 'line': {'width': 0.5, 'color': 'red'}},
            name=station_name + ' (EXITS)'
        ))



    return {
        'data': traces,
        'layout': go.Layout(
            yaxis={'type':'log', 'title':'Midtown: Number of People through Entries & Exits'},
            xaxis={'title':'Weekday'},
            hovermode='closest'
        )
    }

if __name__ == '__main__':
    app.run_server(host='127.0.0.1', port=8080, debug=True)

    #why did i pick the station -> Midtown is my main Focus of my interest (ex.Photography)
    #what is it there for me -> my stations where I mostly go to (faster, closer)
    #what it means for me? - The fastest time to travel - lo/ for Booked shoots - hi/ for random shootings & Quick instant photo sales
    
    #why so many ppl are in there at given time? - visualization shows 47th st Rock (ex. pic)
    #a coffee shop or a mobile food/drink tracks: where to cell coffee around the station - time?
    
    #the visual part: I used Dash and Folium in a different files and I put them together to visualize
    
    #my plans: to transform project into flask to rander the different htmls to get control over the zizes of the bubles in different times
    #   and maybe add a several weeks into a project to compare and a year build the expectencies