import json
import pandas as pd
import dash
from dash import dcc
from dash import html
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output
from waitress import serve
import requests
import time

def forecaster(tags, api_key, weather=None, production=None, jupyter_mode=None, raw=False):
    if raw is True:
        fcst_dict = {}
        for tag in tags:
            df = tags[tag]
            if weather is not None:
                lat = weather['lat']
                lon = weather['lon']
            else:
                lat = None
                lon = None
            x = requests.post('https://www.waterworks.ai/api/forecast',
                              json={'df': df.to_json(orient='records', date_format='iso'), 'api_key': api_key, 'lat': lat,
                                    'lon': lon})
            js = x.json()
            # fig = plotly.io.from_json(json.dumps(js))
            fcst = pd.read_json(json.dumps(js), orient='records')
            fcst_dict[tag] = fcst

        return fcst_dict
    else:
        app = dash.Dash(__name__,
                        title='Forecasting',
                        external_stylesheets=[dbc.themes.COSMO, dbc.icons.BOOTSTRAP],
                        meta_tags=[{"name": "viewport", "content": "width=device-width"}],
                        suppress_callback_exceptions=True)

        # the style arguments for the sidebar. We use position:fixed and a fixed width
        SIDEBAR_STYLE = {
            "position": "fixed",
            "top": 0,
            "left": 0,
            "bottom": 0,
            "width": "16rem",
            "padding": "2rem 1rem",
            # "background-color": "#f8f9fa",
        }

        # the styles for the main content position it to the right of the sidebar and
        # add some padding.
        CONTENT_STYLE = {
            "margin-left": "18rem",
            "margin-right": "2rem",
            "padding": "2rem 1rem",

        }
        LOGO = "https://raw.githubusercontent.com/waterworksai/pydata/main/wwvt323.png"

        navbar = dbc.Navbar(
            dbc.Container(
                [
                    html.A(
                        # Use row and col to control vertical alignment of logo / brand
                        dbc.Row(
                            [
                                dbc.Col(html.Img(src=LOGO, height="15px")),
                            ],
                            align="center",
                            className="g-0",
                        ),
                        href="/",
                        style={"textDecoration": "none"},
                    ),
                    dbc.NavLink(dbc.Button("API Docs", color='link', outline=True), href="https://www.api.waterworks.ai")

                ]
            ),
            color="white",
            # dark=True,
        )

        #saved_figures = [f for f in os.listdir(output_dir) if f.endswith('.json')]
        #options = [{'label': os.path.splitext(f)[0], 'value': f} for f in saved_figures]

        # initial_figure = from_json(initial_figure_path)

        content = html.Div(
            [html.Br(),
             dbc.Container(dbc.Row(html.H1('Forecasting', style={"text-align": "center", "font-weight": "bold"}))),
             html.Br(),
             # dbc.Container(buttons, style={'text-align':'center'})
             dbc.Row(html.P('Select flow series below.',
                            style={"text-align": "center"}, className='lead')),
             dbc.Container(dbc.Row(dbc.Select(id='tag-dropdown', options=[{'label': t, 'value': t} for t in tags])), style={'width':'30%'}),
             html.Br(),
             dbc.Container(dbc.Row(dcc.Graph(id='forecast-plot')))
             ])

        # if current_user.is_authenticated:
        app.layout = html.Div([dcc.Location(id="url"), navbar, content])


        @app.callback(
            Output('forecast-plot', 'figure'),
            [Input('tag-dropdown', 'value')]
        )
        def update_graph(tag):
            import plotly.graph_objs as go
            df = tags[tag]
            if weather is not None:
                lat = weather['lat']
                lon = weather['lon']
            else:
                lat = None
                lon = None
            x = requests.post('https://www.waterworks.ai/api/forecast', json={'df':df.to_json(orient='records', date_format='iso'), 'api_key':api_key, 'lat':lat, 'lon':lon})
            js = x.json()
            #fig = plotly.io.from_json(json.dumps(js))
            fcst = pd.read_json(json.dumps(js), orient='records')
            df = df.iloc[-10*fcst.shape[0]:]
            trace = go.Scatter(
                name='Past flow',
                mode='lines',
                x=list(df['ds']),
                y=list(df['y']),
                marker=dict(
                    color='grey',
                    line=dict(width=1)
                )
            )
            trace1 = go.Scatter(
                name='Forecast',
                mode='lines',
                x=list(fcst['ds']),
                y=list(fcst['yhat']),
                marker=dict(
                    color='#ed729d',
                    line=dict(width=1)
                )
            )
            upper_band = go.Scatter(
                name='Upper band',
                mode='lines',
                x=list(fcst['ds']),
                y=list(fcst['hi-90']),
                line=dict(color='#A7C7E7'),
                fill='tonexty'
            )
            lower_band = go.Scatter(
                name='Lower band',
                mode='lines',
                x=list(fcst['ds']),
                y=list(fcst['lo-90']),
                line=dict(color='#A7C7E7')
            )
            data = [trace, lower_band, upper_band, trace1]

            layout = dict(title=tag+' Forecast',
                          xaxis=dict(title='Dates'))

            fig = dict(data=data, layout=layout)
            return fig

        if production is not None:
            serve(app.server, host='0.0.0.0', port=production)
        else:
            app.run_server(debug=False, jupyter_mode=jupyter_mode)

def leak_detector(tags, api_key, unit, night_mode=False, production=None, jupyter_mode=None, raw=False):
    if raw is True:
        leak_list = []
        for tag in tags:
            df = tags[tag]
            x = requests.post('https://www.waterworks.ai/api/leakage',
                              json={'df': df.to_json(orient='records', date_format='iso'), 'unit': unit, 'night_mode':night_mode,
                                    'api_key': api_key})
            js = x.json()
            # fig = plotly.io.from_json(json.dumps(js))
            fcst = pd.read_json(json.dumps(js), orient='records')
            df['ds'] = pd.to_datetime(df['ds'])
            fcst['ds'] = pd.to_datetime(fcst['ds'])
            df = df.set_index('ds')
            fcst = fcst.set_index('ds')
            df['Alarm'] = fcst['anomaly']
            active = fcst.iloc[-3:]['anomaly'].sum()

            if active > 0:
                leak_list.append(tag)
            else:
                pass
            time.sleep(1)

        return leak_list
    else:
        app = dash.Dash(__name__,
                        title='Leak Detector',
                        external_stylesheets=[dbc.themes.COSMO, dbc.icons.BOOTSTRAP],
                        meta_tags=[{"name": "viewport", "content": "width=device-width"}],
                        suppress_callback_exceptions=True)

        # the style arguments for the sidebar. We use position:fixed and a fixed width
        SIDEBAR_STYLE = {
            "position": "fixed",
            "top": 0,
            "left": 0,
            "bottom": 0,
            "width": "16rem",
            "padding": "2rem 1rem",
            # "background-color": "#f8f9fa",
        }

        # the styles for the main content position it to the right of the sidebar and
        # add some padding.
        CONTENT_STYLE = {
            "margin-left": "18rem",
            "margin-right": "2rem",
            "padding": "2rem 1rem",

        }
        LOGO = "https://raw.githubusercontent.com/waterworksai/pydata/main/wwvt323.png"

        navbar = dbc.Navbar(
            dbc.Container(
                [
                    html.A(
                        # Use row and col to control vertical alignment of logo / brand
                        dbc.Row(
                            [
                                dbc.Col(html.Img(src=LOGO, height="15px")),
                            ],
                            align="center",
                            className="g-0",
                        ),
                        href="/",
                        style={"textDecoration": "none"},
                    ),
                    dbc.NavLink(dbc.Button("API Docs", color='link', outline=True), href="https://www.api.waterworks.ai")

                ]
            ),
            color="white",
            # dark=True,
        )



        content = html.Div(
            [html.Br(),
             dbc.Container(dbc.Row(html.H1('Leak Detector', style={"text-align": "center", "font-weight": "bold"}))),
             html.Br(),
             dbc.Row(html.P('Any identified leaks will be listed below.',
                            style={"text-align": "center"}, className='lead')),
             # dbc.Container(buttons, style={'text-align':'center'})
             dcc.Loading(id='loading', children=dbc.Container(dbc.Row(dbc.Select(id='tag-dropdown')), style={'width':'30%'})),
             html.Br(),
             dbc.Row(html.P('Flow & Alarm',
                            style={"text-align": "center", 'font-weight': 'bold'}, className='lead')),
             html.Br(),
             dbc.Container(dbc.Row(dcc.Graph(id='anomaly-plot')))
             ])

        # if current_user.is_authenticated:
        app.layout = html.Div([dcc.Location(id="url"), navbar, content])

        @app.callback(
            Output('tag-dropdown', 'options'),
            Input('url','pathname')
        )
        def loop(pathname):
            import plotly.graph_objs as go
            options = []
            for tag in tags:
                df = tags[tag]
                x = requests.post('https://www.waterworks.ai/api/leakage', json={'df': df.to_json(orient='records', date_format='iso'), 'unit':unit, 'night_mode':night_mode, 'api_key':api_key})
                js = x.json()
                # fig = plotly.io.from_json(json.dumps(js))
                fcst = pd.read_json(json.dumps(js), orient='records')
                df['ds'] = pd.to_datetime(df['ds'])
                fcst['ds'] = pd.to_datetime(fcst['ds'])
                df = df.set_index('ds')
                fcst = fcst.set_index('ds')
                df['Alarm'] = fcst['anomaly']
                active = fcst.iloc[-3:]['anomaly'].sum()

                df.loc[df['Alarm'] == 1, 'Alarm'] = df['y']
                df.loc[df['Alarm'] == 0, 'Alarm'] = None
                print('here', fcst['anomaly'])
                df = df.reset_index()
                if active > 0:
                    options.append({'label': tag, 'value': df.to_json(orient='records',date_format='iso')})
                else:
                    pass
                time.sleep(1)

            return options


        @app.callback(
            Output('anomaly-plot', 'figure'),
            [Input('tag-dropdown', 'value')]
        )
        def update_graph(tag):
            import plotly.graph_objs as go
            print(tag)
            df = pd.read_json(tag, orient='records')
            df = df.reset_index()


            trace = go.Scatter(
                name='Past flow',
                mode='lines',
                x=list(df['ds']),
                y=list(df['y']),
                marker=dict(
                    color='grey',
                    line=dict(width=1)
                )
            )

            anomaly = go.Scatter(
                name='Alarm',
                mode='markers',
                x=list(df['ds']),
                y=list(df['Alarm']),
                line=dict(color='red'),
            )

            data = [trace, anomaly]

            layout = dict(title='Potential Leaks',
                          xaxis=dict(title='Dates'))

            fig = dict(data=data, layout=layout)
            return fig

        if production is not None:
            serve(app.server, host='0.0.0.0', port=production)
        else:
            app.run_server(debug=False, jupyter_mode=jupyter_mode)

def blockage_detector(tags, api_key, production=None, jupyter_mode=None, raw=False):
    if raw is True:
        blockage_list = []
        for tag in tags:
            df = tags[tag]
            x = requests.post('https://www.waterworks.ai/api/blockage',
                              json={'df': df.to_json(orient='records', date_format='iso'), 'api_key': api_key})
            js = x.json()
            # fig = plotly.io.from_json(json.dumps(js))
            fcst = pd.read_json(json.dumps(js), orient='records')
            df['ds'] = pd.to_datetime(df['ds'])
            fcst['ds'] = pd.to_datetime(fcst['ds'])
            df = df.set_index('ds')
            fcst = fcst.set_index('ds')
            df['Alarm'] = fcst['anomaly']
            active = fcst.iloc[-3:]['anomaly'].sum()

            if active > 0:
                blockage_list.append(tag)
            else:
                pass
            time.sleep(1)

        return blockage_list
    else:
        app = dash.Dash(__name__,
                        title='Blockage Detector',
                        external_stylesheets=[dbc.themes.COSMO, dbc.icons.BOOTSTRAP],
                        meta_tags=[{"name": "viewport", "content": "width=device-width"}],
                        suppress_callback_exceptions=True)

        # the style arguments for the sidebar. We use position:fixed and a fixed width
        SIDEBAR_STYLE = {
            "position": "fixed",
            "top": 0,
            "left": 0,
            "bottom": 0,
            "width": "16rem",
            "padding": "2rem 1rem",
            # "background-color": "#f8f9fa",
        }

        # the styles for the main content position it to the right of the sidebar and
        # add some padding.
        CONTENT_STYLE = {
            "margin-left": "18rem",
            "margin-right": "2rem",
            "padding": "2rem 1rem",

        }
        LOGO = "https://raw.githubusercontent.com/waterworksai/pydata/main/wwvt323.png"

        navbar = dbc.Navbar(
            dbc.Container(
                [
                    html.A(
                        # Use row and col to control vertical alignment of logo / brand
                        dbc.Row(
                            [
                                dbc.Col(html.Img(src=LOGO, height="15px")),
                            ],
                            align="center",
                            className="g-0",
                        ),
                        href="/",
                        style={"textDecoration": "none"},
                    ),
                    dbc.NavLink(dbc.Button("API Docs", color='link', outline=True), href="https://www.api.waterworks.ai")

                ]
            ),
            color="white",
            # dark=True,
        )

        content = html.Div(
            [html.Br(),
             dbc.Container(dbc.Row(html.H1('Blockage Detector', style={"text-align": "center", "font-weight": "bold"}))),
             html.Br(),
             dbc.Row(html.P('Any identified blockages will be listed below.',
                            style={"text-align": "center"}, className='lead')),
             dcc.Loading(id='loading',
                         children=dbc.Container(dbc.Row(dbc.Select(id='tag-dropdown')), style={'width': '30%'})),
             html.Br(),
             dbc.Row(html.P('Flow & Alarm',
                            style={"text-align": "center", 'font-weight': 'bold'}, className='lead')),
             html.Br(),
             dbc.Container(dbc.Row(dcc.Graph(id='anomaly-plot')))
             ])

        # if current_user.is_authenticated:
        app.layout = html.Div([dcc.Location(id="url"), navbar, content])

        @app.callback(
            Output('tag-dropdown', 'options'),
            Input('url', 'pathname')
        )
        def loop(pathname):
            import plotly.graph_objs as go
            options = []
            for tag in tags:
                df = tags[tag]
                x = requests.post('https://www.waterworks.ai/api/blockage',
                                  json={'df': df.to_json(orient='records', date_format='iso'), 'api_key':api_key})
                js = x.json()
                # fig = plotly.io.from_json(json.dumps(js))
                fcst = pd.read_json(json.dumps(js), orient='records')
                df['ds'] = pd.to_datetime(df['ds'])
                fcst['ds'] = pd.to_datetime(fcst['ds'])
                df = df.set_index('ds')
                fcst = fcst.set_index('ds')
                df['Alarm'] = fcst['anomaly']
                active = fcst.iloc[-3:]['anomaly'].sum()
                df.loc[df['Alarm'] == 1, 'Alarm'] = df['y']
                df.loc[df['Alarm'] == 0, 'Alarm'] = None
                print('here', fcst['anomaly'])
                df = df.reset_index()
                if active > 0:
                    options.append({'label': tag, 'value': df.to_json(orient='records', date_format='iso')})
                else:
                    pass
                time.sleep(1)

            return options

        @app.callback(
            Output('anomaly-plot', 'figure'),
            [Input('tag-dropdown', 'value')]
        )
        def update_graph(tag):
            import plotly.graph_objs as go
            print(tag)
            df = pd.read_json(tag, orient='records')
            df = df.reset_index()

            trace = go.Scatter(
                name='Past flow',
                mode='lines',
                x=list(df['ds']),
                y=list(df['y']),
                marker=dict(
                    color='grey',
                    line=dict(width=1)
                )
            )

            anomaly = go.Scatter(
                name='Alarm',
                mode='markers',
                x=list(df['ds']),
                y=list(df['Alarm']),
                line=dict(color='red'),
            )

            data = [trace, anomaly]

            layout = dict(title='Potential Blockages',
                          xaxis=dict(title='Dates'))

            fig = dict(data=data, layout=layout)
            return fig

        if production is not None:
            serve(app.server, host='0.0.0.0', port=production)
        else:
            app.run_server(debug=False, jupyter_mode=jupyter_mode)

def inflow_infiltration(tags, api_key, person_equivalents=None, snowmelt=False, production=None, jupyter_mode=None, raw=False):
    if raw is True:
        inflow_infil_dict = {}
        for tag in tags:
            df = tags[tag]
            x = requests.post('https://www.waterworks.ai/api/inflow',
                              json={'df': df.to_json(orient='records', date_format='iso'), 'api_key': api_key})
            js = x.json()
            fcst = pd.read_json(json.dumps(js), orient='records')

            if person_equivalents is not None:
                unit = person_equivalents[tag]['unit']
                population = person_equivalents[tag]['population']
                personal_daily_volume = person_equivalents[tag]['personal_daily_volume']
                u = unit.split('/')[-1]
                if u == 's':
                    vol = (population * personal_daily_volume) / 86400
                elif u == 'h':
                    vol = (population * personal_daily_volume) / 24
                elif u == 'd':
                    vol = population * personal_daily_volume
                share = vol / fcst['DWF'].mean()

                fcst['Usage'] = share * fcst['DWF']
                fcst['BF'] = fcst['DWF'] - fcst['Usage']

                inflow_infil_dict[tag] = {'total':fcst['y'].sum(),'inflow':fcst['y'].sum() - fcst['DWF'].sum(),'sewage':fcst['DWF'].sum() - fcst['BF'].sum(),
                                          'infiltration':fcst['BF'].sum()}

            else:
                inflow_infil_dict[tag] = {'total': fcst['y'].sum(), 'inflow': fcst['y'].sum() - fcst['DWF'].sum(),
                                          'dwf': fcst['DWF'].sum()}
            if snowmelt is True:
                fcst['ds'] = pd.to_datetime(fcst['ds'])
                fcst['month'] = fcst.ds.dt.month
                fcst_summer = fcst.loc[fcst['month'].isin([5, 6, 7, 8, 9, 10])]
                fcst_winter = fcst.loc[fcst['month'].isin([11, 12, 1, 2, 3, 4])]
                inflow_infil_dict['inflow_rainfall'] = fcst_summer['y'].sum() - fcst_summer['DWF'].sum()
                inflow_infil_dict['inflow_snowmelt'] = fcst_winter['y'].sum() - fcst_winter['DWF'].sum()

        return inflow_infil_dict
    else:
        app = dash.Dash(__name__,
                        title='Inflow & Infiltration',
                        external_stylesheets=[dbc.themes.COSMO, dbc.icons.BOOTSTRAP],
                        meta_tags=[{"name": "viewport", "content": "width=device-width"}],
                        suppress_callback_exceptions=True)

        # the style arguments for the sidebar. We use position:fixed and a fixed width
        SIDEBAR_STYLE = {
            "position": "fixed",
            "top": 0,
            "left": 0,
            "bottom": 0,
            "width": "16rem",
            "padding": "2rem 1rem",
            # "background-color": "#f8f9fa",
        }

        # the styles for the main content position it to the right of the sidebar and
        # add some padding.
        CONTENT_STYLE = {
            "margin-left": "18rem",
            "margin-right": "2rem",
            "padding": "2rem 1rem",

        }
        LOGO = "https://raw.githubusercontent.com/waterworksai/pydata/main/wwvt323.png"

        navbar = dbc.Navbar(
            dbc.Container(
                [
                    html.A(
                        # Use row and col to control vertical alignment of logo / brand
                        dbc.Row(
                            [
                                dbc.Col(html.Img(src=LOGO, height="15px")),
                            ],
                            align="center",
                            className="g-0",
                        ),
                        href="/",
                        style={"textDecoration": "none"},
                    ),
                    dbc.NavLink(dbc.Button("API Docs", color='link', outline=True), href="https://www.api.waterworks.ai")

                ]
            ),
            color="white",
            # dark=True,
        )


        content = html.Div(
            [html.Br(),
             dbc.Container(dbc.Row(html.H1('Inflow & Infiltration', style={"text-align": "center", "font-weight": "bold"}))),
             html.Br(),
             # dbc.Container(buttons, style={'text-align':'center'})
             dbc.Row(html.P('Select flow series below.',
                            style={"text-align": "center"}, className='lead')),
             dbc.Container(dbc.Row(dbc.Select(id='tag-dropdown', options=[{'label': t, 'value': t} for t in tags])), style={'width':'30%'}),
             html.Br(),
             dbc.Row(html.P('Flow composition over time',
                            style={"text-align": "center", 'font-weight':'bold'}, className='lead')),
             html.Br(),
             dbc.Container(dbc.Row(dcc.Graph(id='anomaly-plot'))),
             html.Br(),
             dbc.Row(html.P('Flow totals',
                            style={"text-align": "center", 'font-weight':'bold'}, className='lead')),
             html.Br(),
             dbc.Container(dbc.Row(dcc.Graph(id='volume-plot'))),
             html.Div(id='snowmelt-div')

             ])

        # if current_user.is_authenticated:
        app.layout = html.Div([dcc.Location(id="url"), navbar, content])


        @app.callback(
            [Output('anomaly-plot', 'figure'), Output('volume-plot','figure'), Output('snowmelt-div', 'children')],
            [Input('tag-dropdown', 'value')]
        )
        def update_graph(tag):
            import plotly.graph_objs as go
            import plotly.express as px
            df = tags[tag]
            x = requests.post('https://www.waterworks.ai/api/inflow', json={'df':df.to_json(orient='records', date_format='iso'), 'api_key':api_key})
            js = x.json()
            fcst = pd.read_json(json.dumps(js), orient='records')

            if person_equivalents is not None:
                unit = person_equivalents[tag]['unit']
                population = person_equivalents[tag]['population']
                personal_daily_volume = person_equivalents[tag]['personal_daily_volume']
                u = unit.split('/')[-1]
                if u == 's':
                    vol = (population * personal_daily_volume) / 86400
                elif u == 'h':
                    vol = (population * personal_daily_volume) / 24
                elif u == 'd':
                    vol = population * personal_daily_volume
                share = vol / fcst['DWF'].mean()

                fcst['Usage'] = share * fcst['DWF']
                fcst['BF'] = fcst['DWF'] - fcst['Usage']

                inflow = go.Scatter(
                    name='Inflow',
                    mode='lines',
                    x=list(fcst['ds']),
                    y=list(fcst['y']),
                    marker=dict(
                        color='#4C78A8',
                        # line=dict(width=1)
                    ),
                    fill='tonexty'

                )
                sewage = go.Scatter(
                    name='Sewage',
                    mode='lines',
                    x=list(fcst['ds']),
                    y=list(fcst['DWF']),
                    line=dict(color='#E45756'),
                    fill='tonexty'

                )
                infiltration = go.Scatter(
                name='Infiltration',
                mode='lines',
                x=list(fcst['ds']),
                y=list(fcst['BF']),
                line=dict(color='#9D755D'),
                fill='tozeroy'

            )


                vol = pd.DataFrame()
                vol['Type'] = ['Inflow', 'Sewage', 'Infiltration']
                vol['Volume'] = [fcst['y'].sum() - fcst['DWF'].sum(), fcst['DWF'].sum()-fcst['BF'].sum(), fcst['BF'].sum()]
                data = [infiltration, sewage, inflow]
            else:
                inflow = go.Scatter(
                    name='Inflow',
                    mode='lines',
                    x=list(fcst['ds']),
                    y=list(fcst['y']),
                    line=dict(color='#4C78A8'),

                    fill='tonexty'

                )

                dwf = go.Scatter(
                    name='Sewage',
                    mode='lines',
                    x=list(fcst['ds']),
                    y=list(fcst['DWF']),
                    line=dict(color='#E45756'),
                    fill='tozeroy'

                )
                vol = pd.DataFrame()
                vol['Type'] = ['Inflow', 'Sewage']
                vol['Volume'] = [fcst['y'].sum() - fcst['DWF'].sum(), fcst['DWF'].sum()]

                data = [dwf, inflow]


            layout = dict(title='Inflow',
                          xaxis=dict(title='Dates'))

            fig = dict(data=data, layout=layout)


            vol_fig = px.pie(vol, values='Volume', names='Type', color='Type', color_discrete_map={'Inflow':'#4C78A8',
                                     'Sewage':'#E45756',
                                     'Infiltration':'#9D755D'})
            if snowmelt is True:
                fcst['ds'] = pd.to_datetime(fcst['ds'])
                fcst['month'] = fcst.ds.dt.month
                fcst_summer = fcst.loc[fcst['month'].isin([5, 6, 7, 8, 9, 10])]
                fcst_winter = fcst.loc[fcst['month'].isin([11, 12, 1, 2, 3, 4])]

                season = pd.DataFrame()
                season['Inflow Type'] = ['Rainfall', 'Snowmelt']
                season['Volume'] = [fcst_summer['y'].sum() - fcst_summer['DWF'].sum(),
                                    fcst_winter['y'].sum() - fcst_winter['DWF'].sum()]

                season_fig = px.bar(season, x='Inflow Type', y='Volume', color='Inflow Type',
                                    color_discrete_map={'Rainfall': '#4C78A8',
                                                        'Snowmelt': '#4C78A8'})
                season_fig.update_layout(
                    plot_bgcolor='white'
                )

                snowmelt_div = [html.Br(),
                                dbc.Row(html.P('Rainfall vs Snowmelt',
                                               style={"text-align": "center", 'font-weight': 'bold'},
                                               className='lead')),
                                html.Br(),
                                dbc.Container(dbc.Row(dcc.Graph(figure=season_fig)))]
            else:
                snowmelt_div = []

            return fig, vol_fig, snowmelt_div

        if production is not None:
            serve(app.server, host='0.0.0.0', port=production)
        else:
            app.run_server(debug=False, jupyter_mode=jupyter_mode)