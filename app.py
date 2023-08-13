from dash import Dash, dcc, html, Input, Output
import pandas as pd

# Replace this with the actual path to your spacex.csv file
data = pd.read_csv("spacex.csv")

app = Dash(__name__)

launch_sites = data['Launch Site'].unique()

app.layout = html.Div(
    children=[
        html.H1(children="SpaceX Launch Data Analytics",
                style={
                    'textAlign': 'center',
                    'color': '#3498DB',
                    'fontFamily': 'Arial',
                    'fontSize': 36,
                    'marginTop': '20px'
                }
            ),
        html.P(
            children="Interactive visual analytics on SpaceX launch data",
            style={
                    'textAlign': 'center',
                    'color': '#5D6D7E',
                    'fontFamily': 'Helvetica',
                    'fontSize': 16,
                    'marginTop': '30px'
            }
        ),
        dcc.Dropdown(
            id='launch-site-dropdown',
            options=[{'label': site, 'value': site} for site in launch_sites],
            value=launch_sites[0],  # Default value
            style={'width': '50%', 'margin': 'auto', 'marginTop': '20px'}
        ),
        dcc.Graph(id='success-pie-chart'),
        dcc.RangeSlider(
            id='payload-range-slider',
            marks={i: str(i) for i in range(0, 10000, 1000)},
            min=0,
            max=10000,
            value=[0, 10000]
        ),
        dcc.Graph(id='success-payload-scatter-chart'),
    ]
)

@app.callback(
    Output('success-pie-chart', 'figure'),
    [Input('launch-site-dropdown', 'value')]
)
def update_pie_chart(selected_launch_site):
    filtered_data = data[data['Launch Site'] == selected_launch_site]
    success_counts = filtered_data['class'].value_counts()
    
    figure = {
        'data': [
            {'labels': ['Success', 'Failure'], 'values': [success_counts.get(1, 0), success_counts.get(0, 0)], 'type': 'pie'}
        ],
        'layout': {
            'title': f'Success vs Failure for Launch Site: {selected_launch_site}',
        }
    }
    return figure

@app.callback(
    Output('success-payload-scatter-chart', 'figure'),
    [Input('launch-site-dropdown', 'value'),
     Input('payload-range-slider', 'value')]
)
def update_scatter_chart(selected_launch_site, payload_range):
    filtered_data = data[(data['Launch Site'] == selected_launch_site) & 
                         (data['Payload Mass (kg)'] >= payload_range[0]) & 
                         (data['Payload Mass (kg)'] <= payload_range[1])]
    
    figure = {
        'data': [
            {'x': filtered_data['Payload Mass (kg)'], 'y': filtered_data['class'], 'mode': 'markers', 'type': 'scatter'}
        ],
        'layout': {
            'title': f'Success vs Payload Mass for Launch Site: {selected_launch_site}',
            'xaxis': {'title': 'Payload Mass (kg)'},
            'yaxis': {'title': 'Success (1) / Failure (0)'},
        }
    }
    return figure

if __name__ == "__main__":
    app.run_server(debug=True)