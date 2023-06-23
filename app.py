from dash import dcc, html, Dash
from dash.dependencies import Input, Output
import pandas as pd
import plotly.graph_objs as go

# Read data and preprocess it
gapzones = pd.read_excel('gapzones.xlsx')
zones = gapzones.dropna()
zones = zones.set_index(zones['Date Time'])

dates_list = [
    'June 14, 2023',
    'May 3, 2023',
    'March 22, 2023',
    'February 1, 2023',
    'December 14, 2022',
    'November 2, 2022',
    'September 21, 2022',
    'July 27, 2022',
    'June 15, 2022',
    'May 4, 2022',
    'March 16, 2022',
    'November 5, 2020',
    'September 16, 2020',
    'August 27, 2020',
    'July 29, 2020',
    'June 10, 2020',
    'April 29, 2020',
    'March 31, 2020',
    'March 23, 2020',
    'March 19, 2020',
    'March 15, 2020',
    'March 3, 2020',
    'October 30, 2019',
    'September 18, 2019',
    'July 31, 2019',
    'December 19, 2018',
    'September 26, 2018',
    'June 13, 2018',
    'March 21, 2018',
    'December 13, 2017',
    'June 14, 2017',
    'March 15, 2017',
    'December 14, 2016',
    'December 16, 2015',
    'June 22, 2011',
    'December 16, 2008',
    'October 29, 2008',
    'October 8, 2008',
    'April 30, 2008',
    'March 18, 2008',
    'March 16, 2008',
    'January 30, 2008',
    'January 22, 2008',
    'December 11, 2007',
    'October 31, 2007',
    'September 18, 2007',
    'August 17, 2007',
    'August 7, 2007',
    'June 28, 2007',
    'May 9, 2007',
    'March 21, 2007',
    'January 31, 2007',
    'December 12, 2006',
    'October 25, 2006',
    'September 20, 2006',
    'August 8, 2006',
    'June 29, 2006',
    'May 10, 2006',
    'March 28, 2006',
    'January 31, 2006',
    'December 13, 2005',
    'November 1, 2005',
    'September 20, 2005',
    'August 9, 2005',
    'June 30, 2005',
    'May 3, 2005',
    'March 22, 2005',
    'February 2, 2005'
]


def display_zones(zones, start_date, end_date, dates_list, highlight = False):
    dates_list = pd.Series(pd.to_datetime(dates_list)).sort_values()
    dates_list = dates_list[(dates_list >= start_date) & (dates_list <= end_date)]
    print(dates_list)
    zones = zones[start_date:end_date]
    # Convert dates to Timestamp format
    start_date = pd.Timestamp(start_date)
    end_date = pd.Timestamp(end_date)
    
    # Hardcoded gap dates
    gap_start_date = pd.Timestamp('2018-07-25')
    gap_end_date = pd.Timestamp('2022-12-12')

    # Separate data
    before_gap = zones.loc[start_date:gap_start_date]
    after_gap = zones.loc[gap_end_date:end_date]

    # Create scatter plots
    scatter_before_gap = go.Scatter(
        x=before_gap['Date'],
        y=before_gap['OPEN'],
        mode='lines',
        name='ESH3 Futures',
        line=dict(color='silver')
    )
    
    scatter_after_gap = go.Scatter(
        x=after_gap['Date'],
        y=after_gap['OPEN'],
        mode='lines',
        name='ESH3 Futures',
        line=dict(color='silver'),
        showlegend=False
    )

    # Add circles where 'Gap Zone Up Filled' or 'Gap Zone Down Filled' are 1
    markers1 = go.Scatter(
        x=zones.loc[zones['Gap Zone Up Filled'] == 1, 'Date'],
        y=zones.loc[zones['Gap Zone Up Filled'] == 1, 'OPEN'],
        mode='markers',
        name='Gap Zone Up Filled',
        marker=dict(color='green', size=8)
    )

    markers2 = go.Scatter(
        x=zones.loc[zones['Gap Zone Down Filled'] == 1, 'Date'],
        y=zones.loc[zones['Gap Zone Down Filled'] == 1, 'OPEN'],
        mode='markers',
        name='Gap Zone Down Filled',
        marker=dict(color='red', size=8)
    )

    # Create layout
    layout = go.Layout(
        title='Gap Zone Analysis',
        xaxis=dict(title='Date Time'),
        yaxis=dict(title='Open'),
    )
    
    # Add red dotted vertical lines at highlight dates if highlight is True
    if highlight and not dates_list.empty:
        layout.shapes = [
            go.layout.Shape(
                type="line",
                xref="x",
                yref="paper",
                x0=date,
                y0=0,
                x1=date,
                y1=1,
                line=dict(
                    color="red",
                    width=1,
                    dash="dot"
                )
            ) for date in dates_list
        ]

    # Create figure
    fig = go.Figure(data=[scatter_before_gap, scatter_after_gap, markers1, markers2], layout=layout)

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
# Add a new dcc.Checkbox to the layout
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
        dcc.Checkbox(
            id='highlight-fomc',
            options=[{'label': 'Add FOMC dates', 'value': 'ON'}],
            value=[]
        )
    ]),
    html.Div([
        dcc.Graph(id='graph-container'),
        # Rest of your layout...
    ])
])

# Modify the callback function
@app.callback(
    [Output('graph-container', 'figure'),
     Output('filtered-down', 'children'),
     Output('filtered-up', 'children')],
    [Input('start-date-picker', 'date'),
     Input('end-date-picker', 'date'),
     Input('highlight-fomc', 'value')]
)
def update_graph(start_date, end_date):
    fig = display_zones(zones, start_date, end_date, dates_list, highlight='ON' in highlight_fomc)
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
