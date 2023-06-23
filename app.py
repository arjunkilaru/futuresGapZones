from dash import dcc, html, Dash
from dash.dependencies import Input, Output
import pandas as pd
import plotly.graph_objs as go

# Read data and preprocess it
gapzones = pd.read_excel('gapzones.xlsx')
zones = gapzones.dropna()
zones = zones.set_index(zones['Date Time'])
dates_list = sorted([
    '2005-02-02',
    '2005-03-22',
    '2005-05-03',
    '2005-06-30',
    '2005-08-09',
    '2005-09-20',
    '2005-11-01',
    '2005-12-13',
    '2006-01-31',
    '2006-03-28',
    '2006-05-10',
    '2006-06-29',
    '2006-08-08',
    '2006-09-20',
    '2006-10-25',
    '2006-12-12',
    '2007-01-31',
    '2007-03-21',
    '2007-05-09',
    '2007-06-28',
    '2007-08-07',
    '2007-09-18',
    '2007-10-31',
    '2007-12-11',
    '2008-01-22',
    '2008-03-16',
    '2008-04-30',
    '2008-05-03',
    '2008-06-25',
    '2008-08-05',
    '2008-09-16',
    '2008-10-29',
    '2008-12-16',
    '2009-01-27',
    '2009-03-17',
    '2009-04-28',
    '2009-06-23',
    '2009-08-11',
    '2009-09-22',
    '2009-11-03',
    '2009-12-15',
    '2010-01-26',
    '2010-03-16',
    '2010-04-27',
    '2010-06-22',
    '2010-08-10',
    '2010-09-21',
    '2010-11-02',
    '2010-12-14',
    '2011-01-25',
    '2011-03-15',
    '2011-04-26',
    '2011-06-21',
    '2011-08-09',
    '2011-09-20',
    '2011-11-01',
    '2011-12-13',
    '2012-01-24',
    '2012-03-13',
    '2012-04-24',
    '2012-06-19',
    '2012-07-31',
    '2012-09-12',
    '2012-10-23',
    '2012-12-11',
    '2013-01-29',
    '2013-03-19',
    '2013-04-30',
    '2013-06-18',
    '2013-07-30',
    '2013-09-17',
    '2013-10-29',
    '2013-12-17',
    '2014-01-28',
    '2014-03-18',
    '2014-04-29',
    '2014-06-17',
    '2014-07-29',
    '2014-09-16',
    '2014-10-28',
    '2014-12-16',
    '2015-01-27',
    '2015-03-17',
    '2015-04-28',
    '2015-06-16',
    '2015-07-28',
    '2015-09-16',
    '2015-10-27',
    '2015-12-15',
    "2016-01-26",  # January 26-27, 2016
    "2016-03-15",  # March 15-16, 2016
    "2016-04-26",  # April 26-27, 2016
    "2016-06-14",  # June 14-15, 2016
    "2016-07-26",  # July 26-27, 2016
    "2016-09-20",  # September 20-21, 2016
    "2016-11-01",  # November 1-2, 2016
    "2016-12-13",
    '2017-03-15',
    '2017-06-14',
    '2017-12-13',
    '2018-03-21',
    '2018-06-13',
    '2022-12-14',
    '2023-02-01',
    '2023-03-22',
    '2023-05-03',
    '2023-06-14'
])


def display_zones(zones, start_date, end_date, dates_list):
    # Convert dates_list to pandas DateTime
    dates_list = pd.to_datetime(dates_list)

    # Sort dates_list and filter based on start_date and end_date
    dates_list = dates_list[(dates_list >= start_date) & (dates_list <= end_date)].sort_values()

    # Filter zones based on start_date and end_date
    zones = zones[start_date:end_date]

    # Convert start_date and end_date to pandas Timestamp
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
        x=before_gap['Date Time'],
        y=before_gap['OPEN'],
        mode='lines',
        name='ESH3 Futures',
        line=dict(color='silver')
    )

    scatter_after_gap = go.Scatter(
        x=after_gap['Date Time'],
        y=after_gap['OPEN'],
        mode='lines',
        name='ESH3 Futures',
        line=dict(color='silver'),
        showlegend=False
    )

    # Add circles where 'Gap Zone Up Filled' or 'Gap Zone Down Filled' are 1
    markers1 = go.Scatter(
        x=zones.loc[zones['Gap Zone Up Filled'] == 1, 'Date Time'],
        y=zones.loc[zones['Gap Zone Up Filled'] == 1, 'OPEN'],
        mode='markers',
        name='Gap Zone Up Filled',
        marker=dict(color='green', size=8)
    )

    markers2 = go.Scatter(
        x=zones.loc[zones['Gap Zone Down Filled'] == 1, 'Date Time'],
        y=zones.loc[zones['Gap Zone Down Filled'] == 1, 'OPEN'],
        mode='markers',
        name='Gap Zone Down Filled',
        marker=dict(color='red', size=8)
    )

    # Create layout
    layout = go.Layout(
        title='Gap Zone Analysis',
        xaxis=dict(title='Date Time'),
        yaxis=dict(title='Open Price'),
        annotations=[
            go.layout.Annotation(
                x=1.02,
                y=0.5,
                text='FOMC Meeting',
                showarrow=False,
                xref='paper',
                yref='paper',
                xanchor='left',
                yanchor='middle',
                font=dict(color='red')
            )
        ]
    )

    # Add red dotted vertical lines at highlight dates
    layout.shapes = [
        go.layout.Shape(
            name='FOMC Meeting Dates',
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



# Update the callback function
@app.callback(
    [Output('graph-container', 'figure'),
     Output('filtered-down', 'children'),
     Output('filtered-up', 'children')],
    [Input('start-date-picker', 'date'),
     Input('end-date-picker', 'date')]
)
def update_graph(start_date, end_date):
    fig = display_zones(zones, start_date, end_date, dates_list)
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
