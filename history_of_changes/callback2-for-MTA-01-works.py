import dash 
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
df = pd.read_csv('_59THST_NQR456W_diff.csv')

#launch app 
app = dash.Dash()

#from https://dash.plot.ly/dash-core-components/dropdown
#Crate a dash layout that con tains a Graph component
hour_options = []
for hour in df['TIME'].unique():
    hour_options.append({'label':str(hour),'value':hour})

app.layout = html.Div([
    dcc.Graph(id='graph'),
    dcc.Dropdown(id='hour-picker', options=hour_options, value=df['TIME'].min())
])

@app.callback(Output('graph', 'figure'), [Input('hour-picker', 'value')])
def update_figure(selected_time):
    filtered_df = df[df['TIME'] == selected_time]
    traces = []
    for station_name in filtered_df['STATION'].unique():
        df_by_station = filtered_df[filtered_df['STATION'] == station_name]
        traces.append(go.Scatter(
            x = df_by_station['entries_diff'],
            y = df_by_station['WEEKDAY'],
            text = df_by_station['TIME'],
            mode = 'markers',
            opacity=0.7,
            marker={'size':10},
            name=station_name
        ))
    return {
        'data': traces,
        'layout': go.Layout(
            xaxis={'type':'log', 'title':'Entries'},
            yaxis={'title':'Weekday'},
            hovermode='closest'
        )
    }

if __name__ == '__main__':
    app.run_server(debug=True)