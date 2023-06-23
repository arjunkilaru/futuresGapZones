from dash import dcc, html, Dash
from dash.dependencies import Input, Output
import pandas as pd
import plotly.graph_objs as go

# Read data and preprocess it
gapzones = pd.read_excel('gapzones.xlsx', skiprows=9)
gapzones['New Day'] = gapzones['New Day'].fillna(0)
zones = gapzones.dropna()
zones = zones.set_index(zones['Date Time'])

def display_zones(zones, start_date, end_date):
    zones = zones.loc[start_date:end_date]

    # Sample data
    x = zones['Date Time']
    y = zones['Open']
    marker_indices = zones['Gap Zone Up Filled'] == 1
    marker_indices2 = zones['Gap Zone Down Filled'] == 1

    # Create a scatter plot
    scatter = go.Scatter(
        x=x,
        y=y,
        mode='lines',
        name='ESH3 Futures',
        line=dict(color='silver')
    )

    # Add circles at points where it's 1
    markers1 = go.Scatter(
        x=x[marker_indices],
        y=y[marker_indices],
        mode='markers',
        name='Gap Zone Up Filled',
        marker=dict(color='green', size=8)
    )

    markers2 = go.Scatter(
        x=x[marker_indices2],
        y=y[marker_indices2],
        mode='markers',
        name='Gap Zone Down Filled',
        marker=dict(color='red', size=8)
    )

    # Create layout
    layout = go.Layout(
        title='Gap Zone Analysis',
        xaxis=dict(title='Date Time'),
        yaxis=dict(title='Open')
    )

    # Create figure
    fig = go.Figure(data=[scatter, markers1, markers2], layout=layout)

    return fig

def display_df_down(zones, start_date, end_date):
    zd = zones.loc[start_date:end_date]
    zd_filtered = zd[zd['Gap Zone Down Filled'] != 0].copy()
    zd_filtered['Date Time'] = zd_filtered['Date Time'].dt.strftime('%Y-%m-%d')
    zd_filtered['Date'] = zd_filtered['Date Time']
    zd_filtered[' '] = "    |   "
    return zd_filtered[['Date', ' ', 'Gap Zone Down']]

def display_df_up(zones, start_date, end_date):
    zd = zones.loc[start_date:end_date]
    zd_filtered = zd[zd['Gap Zone Up Filled'] != 0].copy()
    zd_filtered['Date Time'] = zd_filtered['Date Time'].dt.strftime('%Y-%m-%d')
    zd_filtered['Date'] = zd_filtered['Date Time']
    zd_filtered[' '] = "    |   "
    return zd_filtered[['Date', ' ', 'Gap Zone Up']]

# Define Dash app
app = Dash(__name__)
server = app.server

app.layout = html.Div([
    html.H1('Gap Zone Analysis'),
    html.Div([
        html.Label('Start Date:'),
        dcc.DatePickerSingle(
            id='start-date-picker',
            date='2005-09-07'
        )
    ]),
    html.Div([
        html.Label('End Date:'),
        dcc.DatePickerSingle(
            id='end-date-picker',
            date='2018-07-25'
        )
    ]),
    html.Div([
        dcc.Graph(id='graph-container'),
        html.Div([
            html.Div([
                html.H3('Gap Zone Down'),
                html.Table(id='filtered-down', className='data-table')
            ], className='data-container', style={'border': '1px solid black', 'margin': '10px'}),
            html.Div([
                html.H3('Gap Zone Up'),
                html.Table(id='filtered-up', className='data-table')
            ], className='data-container', style={'border': '1px solid black', 'margin': '10px'})
        ], className='data-tables-container', style={'display': 'flex', 'justifyContent': 'space-around'})
    ])
])
# Define app callback
@app.callback(
    [Output('graph-container', 'figure'),
     Output('filtered-down', 'children'),
     Output('filtered-up', 'children')],
    [Input('start-date-picker', 'date'),
     Input('end-date-picker', 'date')]
)
def update_graph(start_date, end_date):
    fig = display_zones(zones, start_date, end_date)
    df_down = display_df_down(zones, start_date, end_date)
    df_up = display_df_up(zones, start_date, end_date)

    table_down = html.Table([
        html.Thead(html.Tr([html.Th(col) for col in df_down.columns])),
        html.Tbody([html.Tr([html.Td(data) for data in row]) for row in df_down.values])
    ], className='data-table')

    table_up = html.Table([
        html.Thead(html.Tr([html.Th(col) for col in df_up.columns])),
        html.Tbody([html.Tr([html.Td(data) for data in row]) for row in df_up.values])
    ], className='data-table')

    return fig, table_down, table_up


# Run the app
if __name__ == '__main__':
    app.run_server(debug=True)
