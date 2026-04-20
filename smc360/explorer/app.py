# App not optimised | Disabled Drag and Drop

import dash
import yaml
import boto3
from dash import html, dcc, Input, State, Output, ClientsideFunction
import dash_bootstrap_components as dbc
import dash_ace
from smc360 import SocialMediaConnector

def explorer():
    app = dash.Dash(__name__, external_scripts=["https://cdnjs.cloudflare.com/ajax/libs/dragula/3.7.2/dragula.min.js"], external_stylesheets=[dbc.themes.CERULEAN], suppress_callback_exceptions=True)
    app.title = 'SMC360 | EXPLORER'
    header = dbc.Navbar(
        dbc.Container([
            html.Div([dbc.NavbarBrand('SOCIAL MEDIA CONNECTOR (SMC360)', className='text-info', style={'font-weight': 'bold'})]),
            html.Div([
                dbc.Col(html.A(dbc.NavbarBrand(html.Img(src='assets/logo.png', height='40px'), className='ml-auto'), href='https://www.blend360.com/', target='_blank'), width='auto')
            ], className='d-flex align-items-center')
        ]), color='light', light=True, className='mt-3'
    )

    footer = dbc.Container([
            dbc.Col(['COPYRIGHT © 2023'])
        ], fluid=True, style={'display': 'flex', 'justify-content': 'space-between', 'align-items': 'center', 'bottom': 0})
    
    arrow_style = {
        'border-top': '10px solid transparent',
        'border-bottom': '10px solid transparent',
        'border-left': '10px solid grey',
        'margin': '10px',
    }

    indicator = dbc.Container([
        html.Div([
            html.Button("About", id='about-header', className='step-button', disabled=False, style={'background-color': 'powderblue', 'border-radius': '100px'}),
            html.Div(style=arrow_style),
            html.Button("Step 1", id='step-1-header', className='step-button', disabled=True, style={'background-color': 'powderblue', 'border-radius': '100px'}),
            html.Div(style=arrow_style),
            html.Button("Step 2", id='step-2-header', className='step-button', disabled=True, style={'background-color': 'powderblue', 'border-radius': '100px'}),
            html.Div(style=arrow_style),
            html.Button("Step 3", id='step-3-header', className='step-button', disabled=True, style={'background-color': 'powderblue', 'border-radius': '100px'}),
            html.Div(style=arrow_style),
            html.Button("Preview", id='preview-header', className='step-button', disabled=True, style={'background-color': 'powderblue', 'border-radius': '100px'})
        ], className='step-header-container d-flex justify-content-between', style={'textAlign': 'center'})
    ])

    beginer_models = {
        'YouTube': 
            [
                html.Div([
                    html.H6('CHANNELS', className='text-info', style={'font-weight': 'bold'}),
                    html.Hr(),
                    html.Div([
                            html.Div([], id='channels'),
                            html.Div([
                                html.Button('Add', id='button-channels'),
                                html.Button('Clear', id='button-clear-channels')
                            ], className='step-header-container d-flex justify-content-between mt-1', style={'textAlign': 'center'})
                        ])
                    ], style={'border': '2px solid black', "background-color": "white", "padding": "10px"}, className='mb-2'),
                html.Div([
                    html.H6('PLAYLISTS', className='text-info', style={'font-weight': 'bold'}),
                    html.Hr(),
                    html.Div([
                            html.Div([], id='playlists'),
                            html.Div([
                                html.Button('Add', id='button-playlists'),
                                html.Button('Clear', id='button-clear-playlists')
                            ], className='step-header-container d-flex justify-content-between mt-1', style={'textAlign': 'center'})
                        ])
                    ], style={'border': '2px solid black', "background-color": "white", "padding": "10px"}, className='mb-2 mt-2'),
                html.Div([
                    html.H6('VIDEOS', className='text-info', style={'font-weight': 'bold'}),
                    html.Hr(),
                    html.Div([
                            html.Div([], id='videos'),
                            html.Div([
                                html.Button('Add', id='button-videos'),
                                html.Button('Clear', id='button-clear-videos')
                            ], className='step-header-container d-flex justify-content-between mt-1', style={'textAlign': 'center'})
                        ])
                    ], style={'border': '2px solid black', "background-color": "white", "padding": "10px"}, className='mb-2 mt-2'),
                html.Div([
                    html.H6('COMMENTS', className='text-info', style={'font-weight': 'bold'}),
                    html.Hr(),
                    html.Div([
                            html.Div([], id='comments'),
                            html.Div([
                                html.Button('Add', id='button-comments'),
                                html.Button('Clear', id='button-clear-comments')
                            ], className='step-header-container d-flex justify-content-between mt-1', style={'textAlign': 'center'})
                        ])
                    ], style={'border': '2px solid black', "background-color": "white", "padding": "10px"}, className='mt-2'),
            ],
        'Instagram':
            [
                html.Div([
                    html.H6('USERS', className='text-info', style={'font-weight': 'bold'}),
                    html.Hr(),
                    html.Div([
                            html.Div([], id='users'),
                            html.Div([
                                html.Button('Add', id='button-users'),
                                html.Button('Clear', id='button-clear-users')
                            ], className='step-header-container d-flex justify-content-between mt-1', style={'textAlign': 'center'})
                        ])
                    ], style={'border': '2px solid black', "background-color": "white", "padding": "10px"}, className='mb-2'),
                html.Div([
                    html.H6('MEDIA', className='text-info', style={'font-weight': 'bold'}),
                    html.Hr(),
                    html.Div([
                            html.Div([], id='media'),
                            html.Div([
                                html.Button('Add', id='button-media'),
                                html.Button('Clear', id='button-clear-media')
                            ], className='step-header-container d-flex justify-content-between mt-1', style={'textAlign': 'center'})
                        ])
                    ], style={'border': '2px solid black', "background-color": "white", "padding": "10px"}),
            ],
        'Reddit':
            [
                html.Div([
                    html.H6('POSTS', className='text-info', style={'font-weight': 'bold'}),
                    html.Hr(),
                    html.Div([
                            html.Div([], id='posts'),
                            html.Div([
                                html.Button('Add', id='button-posts'),
                                html.Button('Clear', id='button-clear-posts')
                            ], className='step-header-container d-flex justify-content-between mt-1', style={'textAlign': 'center'})
                        ])
                    ], style={'border': '2px solid black', "background-color": "white", "padding": "10px"})
            ]
    }

    beginer_input = {
        'YouTube': [
            html.Div([], className="container", id='youtube', style={"width": "70%", "background-color": "lightgrey"}),
            html.Div(
                style={"width": "30%", "display": "flex", "flex-direction": "column", "border":"2px black solid", "padding": "10px"},
                children=[
                    html.P('DATAPOINTS', className='text-info', style={'font-weight': 'bold', 'textAlign': 'center', 'margin': '0', 'padding': '0'}),
                    html.Button("channels", id='button-input-channels'),
                    html.Button("videos", id='button-input-videos'),
                    html.Button("playlists", id='button-input-playlists'),
                    html.Button("comments", id='button-input-comments'),
                    html.Button("search", id='button-input-search'),
                    html.Hr(style={"width": "100%"}),
                    html.P('ATTRIBUTES', className='text-info', style={'font-weight': 'bold', 'textAlign': 'center', 'margin': '0', 'padding': '0'}),
                    html.Button("default_limit", id='button-input-youtube-limit'),
                    html.Button("get_comments", id='button-input-youtube-get-comments'),
                    html.Button("follow_up_on_search", id='button-input-youtube-followup-search'),
                    html.Hr(style={"width": "100%"}),
                    html.Button("Clear", id='button-youtube-clear'),
                ]
            )
        ],
        'Instagram': [
            html.Div([
                html.Div([
                    dcc.Input(type='text', value='default_limit', style={'font-weight': 'bold', 'border-radius': 5, 'border-style': 'solid black', 'border-width': '2px'}, disabled=True),
                    dcc.Input(type='number', value=5000, style={'border-radius': 5, 'border-style': 'solid black', 'border-width': '2px', 'width': '100%'})
                    ], style={'display': 'flex', 'flexDirection': 'row', 'border': '2px solid black', "background-color": "white", "padding": "10px"}, className='mb-2'),
                html.Div([
                    html.H6('USERS', className='text-info', style={'font-weight': 'bold'}),
                    html.Hr(),
                    ], style={'border': '2px solid black', "background-color": "white", "padding": "10px"}, className='mb-2'),
                html.Div([
                    html.H6('MEDIA', className='text-info', style={'font-weight': 'bold'}),
                    html.Hr(),
                    ], style={'border': '2px solid black', "background-color": "white", "padding": "10px"}, className='mb-2')
            ], id='instagram', className="container", style={"width": "70%", "background-color": "lightgrey", "padding": "10px"}),
            html.Div(
                style={"width": "30%", "display": "flex", "flex-direction": "column", "border":"2px black solid", "padding": "10px"},
                children=[
                    html.P('DATAPOINTS', className='text-info', style={'font-weight': 'bold', 'textAlign': 'center', 'margin': '0', 'padding': '0'}),
                    html.Button("users", id='button-input-user', disabled=True),
                    html.Button("media", id='button-input-media', disabled=True),
                    html.Hr(style={"width": "100%"}),
                    html.P('ATTRIBUTES', className='text-info', style={'font-weight': 'bold', 'textAlign': 'center', 'margin': '0', 'padding': '0'}),
                    html.Button("default_limit", id='button-input-instagram-limit', disabled=True),
                    html.Hr(style={"width": "100%"}),
                    html.Button("Clear", id='button-instagram-clear'),
                ]
            )
        ],
        'Reddit': [
            html.Div([], id='reddit', className="container", style={"width": "70%", "background-color": "lightgrey", "padding": "10px"}),
            html.Div(
                style={"width": "30%", "display": "flex", "flex-direction": "column", "border":"2px black solid", "padding": "10px"},
                children=[
                    html.P('DATAPOINTS', className='text-info', style={'font-weight': 'bold', 'textAlign': 'center', 'margin': '0', 'padding': '0'}),
                    html.Button("posts", id='button-input-posts'),
                    html.Hr(style={"width": "100%"}),
                    html.P('ATTRIBUTES', className='text-info', style={'font-weight': 'bold', 'textAlign': 'center', 'margin': '0', 'padding': '0'}),
                    html.Button("default_limit", id='button-input-reddit-limit'),
                    html.Hr(style={"width": "100%"}),
                    html.Button("Clear", id='button-reddit-clear'),
                ]
            )
        ]
    }

    platforms = ['YouTube', 'Instagram', 'Reddit']
    database = ['PostgreSQL', 'Snowflake']
    object_storage = ['S3']

    platform_help_bgn = {
        'YouTube': [
            html.Div(style={'display': 'flex', 'flexDirection': 'row', "background-color": "white"}, 
                children=[
                    dcc.Input(type='text', value='service_name', style={'font-weight': 'bold', 'border-radius': 5, 'border-style': 'solid black', 'border-width': '2px'}, disabled=True),
                    dcc.Input(type='text', value='youtube', style={'border-radius': 5, 'border-style': 'solid black', 'border-width': '2px', 'width': '100%'}, disabled=True)
                    ], className='mb-1'),
            html.Div(style={'display': 'flex', 'flexDirection': 'row', "background-color": "white"}, 
                children=[
                    dcc.Input(type='text', value='key', style={'font-weight': 'bold', 'border-radius': 5, 'border-style': 'solid black', 'border-width': '2px'}, disabled=True),
                    dcc.Input(type='password', style={'border-radius': 5, 'border-style': 'solid black', 'border-width': '2px', 'width': '100%'})
                    ]),
        ],
        'Instagram': [
            html.Div(style={'display': 'flex', 'flexDirection': 'row', "background-color": "white"}, 
                children=[
                    dcc.Input(type='text', value='service_name', style={'font-weight': 'bold', 'border-radius': 5, 'border-style': 'solid black', 'border-width': '2px'}, disabled=True),
                    dcc.Input(type='text', value='instagram', style={'border-radius': 5, 'border-style': 'solid black', 'border-width': '2px', 'width': '100%'}, disabled=True)
                    ], className='mb-1'),
            html.Div(style={'display': 'flex', 'flexDirection': 'row', "background-color": "white"}, 
                children=[
                    dcc.Input(type='text', value='key', style={'font-weight': 'bold', 'border-radius': 5, 'border-style': 'solid black', 'border-width': '2px'}, disabled=True),
                    dcc.Input(type='text', style={'border-radius': 5, 'border-style': 'solid black', 'border-width': '2px', 'width': '100%'})
                    ]),
        ],
        'Reddit': [
            html.Div(style={'display': 'flex', 'flexDirection': 'row', "background-color": "white"}, 
                children=[
                    dcc.Input(type='text', value='service_name', style={'font-weight': 'bold', 'border-radius': 5, 'border-style': 'solid black', 'border-width': '2px'}, disabled=True),
                    dcc.Input(type='text', value='reddit', style={'border-radius': 5, 'border-style': 'solid black', 'border-width': '2px', 'width': '100%'}, disabled=True)
                    ], className='mb-1'),
        ]
    }

    database_help_bgn = {
        'PostgreSQL': [
            html.Div(style={'display': 'flex', 'flexDirection': 'row', "background-color": "white"}, 
                children=[
                    dcc.Input(type='text', value='service_name', style={'font-weight': 'bold', 'border-radius': 5, 'border-style': 'solid black', 'border-width': '2px'}, disabled=True),
                    dcc.Input(type='text', value='postgresql', style={'border-radius': 5, 'border-style': 'solid black', 'border-width': '2px', 'width': '100%'}, disabled=True)
                    ], className='mb-1'),
            html.Div(style={'display': 'flex', 'flexDirection': 'row', "background-color": "white"}, 
                children=[
                    dcc.Input(type='text', value='user', style={'font-weight': 'bold', 'border-radius': 5, 'border-style': 'solid black', 'border-width': '2px'}, disabled=True),
                    dcc.Input(type='text', style={'border-radius': 5, 'border-style': 'solid black', 'border-width': '2px', 'width': '100%'})
                    ], className='mb-1'),
            html.Div(style={'display': 'flex', 'flexDirection': 'row', "background-color": "white"}, 
                children=[
                    dcc.Input(type='text', value='password', style={'font-weight': 'bold', 'border-radius': 5, 'border-style': 'solid black', 'border-width': '2px'}, disabled=True),
                    dcc.Input(type='password', style={'border-radius': 5, 'border-style': 'solid black', 'border-width': '2px', 'width': '100%'})
                    ], className='mb-1'),
            html.Div(style={'display': 'flex', 'flexDirection': 'row', "background-color": "white"}, 
                children=[
                    dcc.Input(type='text', value='host', style={'font-weight': 'bold', 'border-radius': 5, 'border-style': 'solid black', 'border-width': '2px'}, disabled=True),
                    dcc.Input(type='text', style={'border-radius': 5, 'border-style': 'solid black', 'border-width': '2px', 'width': '100%'})
                    ], className='mb-1'),
            html.Div(style={'display': 'flex', 'flexDirection': 'row', "background-color": "white"}, 
                children=[
                    dcc.Input(type='text', value='port', style={'font-weight': 'bold', 'border-radius': 5, 'border-style': 'solid black', 'border-width': '2px'}, disabled=True),
                    dcc.Input(type='number', style={'border-radius': 5, 'border-style': 'solid black', 'border-width': '2px', 'width': '100%'})
                    ], className='mb-1'),
            html.Div(style={'display': 'flex', 'flexDirection': 'row', "background-color": "white"}, 
                children=[
                    dcc.Input(type='text', value='database', style={'font-weight': 'bold', 'border-radius': 5, 'border-style': 'solid black', 'border-width': '2px'}, disabled=True),
                    dcc.Input(type='text', style={'border-radius': 5, 'border-style': 'solid black', 'border-width': '2px', 'width': '100%'})
                    ], className='mb-1'),
            html.Div(style={'display': 'flex', 'flexDirection': 'row', "background-color": "white"}, 
                children=[
                    dcc.Input(type='text', value='schema', style={'font-weight': 'bold', 'border-radius': 5, 'border-style': 'solid black', 'border-width': '2px'}, disabled=True),
                    dcc.Input(type='text', style={'border-radius': 5, 'border-style': 'solid black', 'border-width': '2px', 'width': '100%'})
                    ])
        ],
        'Snowflake': [
            html.Div(style={'display': 'flex', 'flexDirection': 'row', "background-color": "white"}, 
                children=[
                    dcc.Input(type='text', value='service_name', style={'font-weight': 'bold', 'border-radius': 5, 'border-style': 'solid black', 'border-width': '2px'}, disabled=True),
                    dcc.Input(type='text', value='snowflake', style={'border-radius': 5, 'border-style': 'solid black', 'border-width': '2px', 'width': '100%'}, disabled=True)
                    ], className='mb-1'),
            html.Div(style={'display': 'flex', 'flexDirection': 'row', "background-color": "white"}, 
                children=[
                    dcc.Input(type='text', value='user', style={'font-weight': 'bold', 'border-radius': 5, 'border-style': 'solid black', 'border-width': '2px'}, disabled=True),
                    dcc.Input(type='text', style={'border-radius': 5, 'border-style': 'solid black', 'border-width': '2px', 'width': '100%'})
                    ], className='mb-1'),
            html.Div(style={'display': 'flex', 'flexDirection': 'row', "background-color": "white"}, 
                children=[
                    dcc.Input(type='text', value='password', style={'font-weight': 'bold', 'border-radius': 5, 'border-style': 'solid black', 'border-width': '2px'}, disabled=True),
                    dcc.Input(type='password', style={'border-radius': 5, 'border-style': 'solid black', 'border-width': '2px', 'width': '100%'})
                    ], className='mb-1'),
            html.Div(style={'display': 'flex', 'flexDirection': 'row', "background-color": "white"}, 
                children=[
                    dcc.Input(type='text', value='account', style={'font-weight': 'bold', 'border-radius': 5, 'border-style': 'solid black', 'border-width': '2px'}, disabled=True),
                    dcc.Input(type='text', style={'border-radius': 5, 'border-style': 'solid black', 'border-width': '2px', 'width': '100%'})
                    ], className='mb-1'),
            html.Div(style={'display': 'flex', 'flexDirection': 'row', "background-color": "white"}, 
                children=[
                    dcc.Input(type='text', value='warehouse', style={'font-weight': 'bold', 'border-radius': 5, 'border-style': 'solid black', 'border-width': '2px'}, disabled=True),
                    dcc.Input(type='text', style={'border-radius': 5, 'border-style': 'solid black', 'border-width': '2px', 'width': '100%'})
                    ], className='mb-1'),
            html.Div(style={'display': 'flex', 'flexDirection': 'row', "background-color": "white"}, 
                children=[
                    dcc.Input(type='text', value='database', style={'font-weight': 'bold', 'border-radius': 5, 'border-style': 'solid black', 'border-width': '2px'}, disabled=True),
                    dcc.Input(type='text', style={'border-radius': 5, 'border-style': 'solid black', 'border-width': '2px', 'width': '100%'})
                    ], className='mb-1'),
            html.Div(style={'display': 'flex', 'flexDirection': 'row', "background-color": "white"}, 
                children=[
                    dcc.Input(type='text', value='schema', style={'font-weight': 'bold', 'border-radius': 5, 'border-style': 'solid black', 'border-width': '2px'}, disabled=True),
                    dcc.Input(type='text', style={'border-radius': 5, 'border-style': 'solid black', 'border-width': '2px', 'width': '100%'})
                    ])
        ]
    }

    object_storage_help_bgn = {
        'S3': [
            html.Div(style={'display': 'flex', 'flexDirection': 'row', "background-color": "white"}, 
                children=[
                    dcc.Input(type='text', value='service_name', style={'font-weight': 'bold', 'border-radius': 5, 'border-style': 'solid black', 'border-width': '2px'}, disabled=True),
                    dcc.Input(type='text', value='s3', style={'border-radius': 5, 'border-style': 'solid black', 'border-width': '2px', 'width': '100%'}, disabled=True)
                    ], className='mb-1'),
            html.Div(style={'display': 'flex', 'flexDirection': 'row', "background-color": "white"}, 
                children=[
                    dcc.Input(type='text', value='endpoint_url', style={'font-weight': 'bold', 'border-radius': 5, 'border-style': 'solid black', 'border-width': '2px'}, disabled=True),
                    dcc.Input(type='text', style={'border-radius': 5, 'border-style': 'solid black', 'border-width': '2px', 'width': '100%'})
                    ], className='mb-1'),
            html.Div(style={'display': 'flex', 'flexDirection': 'row', "background-color": "white"}, 
                children=[
                    dcc.Input(type='text', value='aws_access_key_id', style={'font-weight': 'bold', 'border-radius': 5, 'border-style': 'solid black', 'border-width': '2px'}, disabled=True),
                    dcc.Input(type='text', style={'border-radius': 5, 'border-style': 'solid black', 'border-width': '2px', 'width': '100%'})
                    ], className='mb-1'),
            html.Div(style={'display': 'flex', 'flexDirection': 'row', "background-color": "white"}, 
                children=[
                    dcc.Input(type='text', value='aws_secret_access_key', style={'font-weight': 'bold', 'border-radius': 5, 'border-style': 'solid black', 'border-width': '2px'}, disabled=True),
                    dcc.Input(type='password', style={'border-radius': 5, 'border-style': 'solid black', 'border-width': '2px', 'width': '100%'})
                    ], className='mb-1'),
            html.Div(style={'display': 'flex', 'flexDirection': 'row', "background-color": "white"}, 
                children=[
                    dcc.Input(type='text', value='bucket_name', style={'font-weight': 'bold', 'border-radius': 5, 'border-style': 'solid black', 'border-width': '2px'}, disabled=True),
                    dcc.Input(type='text', style={'border-radius': 5, 'border-style': 'solid black', 'border-width': '2px', 'width': '100%'})
                    ], className='mb-1')
        ]
    }

    input_help = {'YouTube': "default_limit: 5000\nget_comments: False\nfollow_up_on_search: False\n\nchannels: {}\nvideos: {} \nplaylists: {}\ncomments: {}\nsearch: {}", 'Instagram':'default_limit: 5000\n\nusers: {}\nmedia: {}', 'Reddit':'default_limit: 5000\n\nposts: {}'}
    models_help = {'YouTube': "channels: {}\nplaylists: {}\nvideos: {}\ncomments: {}", 'Instagram': "users: {}\nmedia: {}", 'Reddit': "posts: {}"}
    models_users = ['id', 'account_type', 'media_count', 'username']
    models_media = ['id' , 'caption', 'media_type', 'media_url', 'permalink', 'timestamp', 'username']
    models_channels = ['id', 'snippet.title', 'snippet.description', 'snippet.customUrl', 'snippet.publishedAt', 'contentDetails.relatedPlaylists.uploads', 'statistics.viewCount', 'statistics.subscriberCount', 'statistics.videoCount', 'snippet.country']
    models_playlists = ['id', 'snippet.title', 'snippet.description', 'snippet.publishedAt', 'contentDetails.itemCount']
    models_videos = ['id', 'snippet.title', 'snippet.description', 'snippet.publishedAt', 'statistics.viewCount', 'statistics.likeCount', 'statistics.commentCount']
    models_comments = ['id', 'snippet.videoId', 'snippet.textOriginal', 'snippet.authorChannelId.value', 'snippet.likeCount', 'snippet.publishedAt', 'snippet.updatedAt']
    models_posts = ['subreddit_name_prefixed', 'author_fullname', 'title', 'num_comments', 'score', 'ups', 'upvote_ratio']
    
    about = html.Div([
        html.H1('SMC360', className='text-info', style={'font-weight': 'bold', 'textAlign': 'center'}),
        html.P('''
        smc360 is a command-line utility that helps extract social media data easily. 
        It works by utilizing APIs to extract social media data and stores the raw JSON responses in a bucket. 
        It then parses the data and loads it into a database.
        '''),
        html.P(['The program supports the following services:', html.Br(),
        '- Platform: `YouTube(Youtube Data API)`, `Instagram(Basic Display API)`', html.Br(),
        '- Database: `PostgreSQL`, `Snowflake`', html.Br(),
        '- Object Storage: `S3`']),
        html.Mark('Run: `smc360 -h` to get started.'),
        html.Div([
            html.Button(html.A('Documentation', href='https://blend360.atlassian.net/wiki/spaces/~64114c920e6828ab20248d9f/pages/252051622/SOCIAL+MEDIA+CONNECTOR?atlOrigin=eyJpIjoiMDlmM2NmNzA0M2RhNDM4MGEyNGFkNWI4YTgxOWZjN2EiLCJwIjoiYyJ9', style={'textDecoration': 'none'}, target='_blank'), id='button-confluence'),
            html.Button('Build configuration files', id='button-config')
        ], className='step-header-container d-flex justify-content-between mt-3', style={'textAlign': 'center'})
    ], id='about')

    step_01 = html.Div([
        html.Div([
            html.H4('1. CREDENTIALS CONFIGURATION', className='text-info', style={'font-weight': 'bold', 'textAlign': 'center', 'margin': '0', 'padding': '0'}),
            html.Button('Learn more', id='button-system-offcanvas'),
        ], className='step-header-container d-flex justify-content-between align-items-center mb-1', style={'textAlign': 'center'}),
        html.Div([
            html.Div([
                html.P('Select a social media platform and fill required credentials', className="mb-1"),
                dcc.Dropdown(id='platform', options=platforms, clearable=False, value=platforms[0], persistence=True, style={'border-width': '2px', 'border-color': 'black'}, className="mb-1"),
                html.Hr(),
                html.Div(id='platform-cred')
            ], style={'border': '2px solid black', "background-color": "white", "padding": "10px"}, className='mb-2'),
            html.Div([
                html.P('Select a database provider and fill required credentials', className="mb-1"),
                dcc.Dropdown(id='database', options=database, clearable=False, value=database[0], persistence=True, style={'border-width': '2px', 'border-color': 'black'}, className="mb-1"),
                html.Hr(),
                html.Div(id='database-cred')
            ], style={'border': '2px solid black', "background-color": "white", "padding": "10px"}, className='mb-2 mt-2'),
            html.Div([
                html.P('Select an object storage provider and fill required credentials', className="mb-1"),
                dcc.Dropdown(id='object_storage', options=object_storage, clearable=False, value=object_storage[0], persistence=True, style={'border-width': '2px', 'border-color': 'black'}, className="mb-1"),
                html.Hr(),
                html.Div(id='object_storage-cred')
            ], style={'border': '2px solid black', "background-color": "white", "padding": "10px"}, className='mt-2')
        ], style={"background-color": "lightgrey", 'padding': '10px'}),
        html.Div([
            html.Button('About', id='button-about'),
            html.Button('Next', id='button-next-step-1')
        ], className='step-header-container d-flex justify-content-between mt-3', style={'textAlign': 'center'})
    ], id='step-1', style={'display': 'none'})

    step_02 = html.Div([
        html.Div([
            html.P('SWITCH BETWEEN `YAML EDITOR` & `PLAYGROUND`', className='text-info', style={'font-weight': 'bold', 'textAlign': 'center', 'margin': '0', 'padding': '0'}),
            html.Button('Switch', id='button-input-playground'),
        ], className='step-header-container d-flex justify-content-between align-items-center mb-1', style={'textAlign': 'center', 'border': '2px solid black', 'padding': '5px'}),
        html.Hr(),
        html.Div([
            html.H4('2. EXTRACTION CONFIGURATION', className='text-info', style={'font-weight': 'bold', 'textAlign': 'center', 'margin': '0', 'padding': '0'}),
            html.Button('Learn more', id='button-input-offcanvas'),
        ], className='step-header-container d-flex justify-content-between align-items-center mb-1', style={'textAlign': 'center'}),
        dash_ace.DashAceEditor(id='input-configuration', mode='yaml', theme='github', fontSize=14, height='200px', width='100%', className="mb-3", style={'border': '2px solid black', 'display': 'block'}),
        html.Div(id='input-configuration-beginer', style={'display':'none'}),
        html.Div([
            html.Button('Previous', id='button-prev-step-2', title='⚠️ Changes made will not be saved'),
            html.Button('Next', id='button-next-step-2')
        ], className='step-header-container d-flex justify-content-between mt-3', style={'textAlign': 'center'})
    ], id='step-2', style={'display': 'none'})

    step_03 = html.Div([
        html.Div([
            html.P('SWITCH BETWEEN `YAML EDITOR` & `PLAYGROUND`', className='text-info', style={'font-weight': 'bold', 'textAlign': 'center', 'margin': '0', 'padding': '0'}),
            html.Button('Switch', id='button-models-playground'),
        ], className='step-header-container d-flex justify-content-between align-items-center mb-1', style={'textAlign': 'center', 'border': '2px solid black', 'padding': '5px'}),
        html.Hr(),
        html.Div([
            html.H4('3. DATABASE CONFIGURATION', className='text-info', style={'font-weight': 'bold', 'textAlign': 'center', 'margin': '0', 'padding': '0'}),
            html.Button('Learn more', id='button-models-offcanvas'),
        ], className='step-header-container d-flex justify-content-between align-items-center mb-1', style={'textAlign': 'center'}),
        dash_ace.DashAceEditor(id='models-configuration', mode='yaml', theme='github', fontSize=14, height='200px', width='100%', style={'border': '2px solid black', 'display': 'block'}),
        html.Div(id='models-configuration-beginer', style={'display':'none', "background-color": "lightgrey", 'padding': '10px'}),
        html.Div([
            html.Button('Previous', id='button-prev-step-3', title='⚠️ Changes made will not be saved'),
            html.Button('Submit', id='button-submit')
        ], className='step-header-container d-flex justify-content-between mt-3', style={'textAlign': 'center'})
    ], id='step-3', style={'display': 'none'})

    preview = html.Div([
        dcc.Loading(
            id="extracting",
            type="default",
            children=[
                html.Div([
                    html.H4('REQUIRED DATA HAS BEEN EXTRACTED', className='text-info', style={'font-weight': 'bold', 'textAlign': 'center'}),
                    # dcc.Dropdown(id='tables-dropdown', clearable=False, persistence=True, style={'border-width': '2px', 'border-color': 'black'}, className="mb-1"),
                    # html.Table(id='table')
                ], id='tables-div')
            ]
        )
    ], id='preview', style={'display': 'none'})

    success = dbc.Toast(
        "Configuration files have been created",
        id="success",
        header="SMC360 | EXPLORER",
        is_open=False,
        icon='success',
        duration=5000,
        style={"position": "fixed", "top": 10, "right": 10, "width": 350}
    )

    error = dbc.Toast(
        id="error",
        header="SMC360 | EXPLORER",
        is_open=False,
        icon='danger',
        duration=5000,
        style={"position": "fixed", "top": 10, "right": 10, "width": 350}
    )

    system_offcanvas = dbc.Offcanvas(
    [
        html.P([
            "The system configuration file contains the details of the platform, database, and object storage credentials that the application needs to run. This file will be created in the current working directory (the directory where you're running the application) with the name config.yaml.",
            html.Br(), html.Br(),
            "To use environment variables in the configuration file, you can reference them by prefixing the variable name with a $ sign, like $MY_VAR. For example, if you want to include a database password that's stored in an environment variable called DB_PASSWORD, you would add the following line to the configuration file:",
            html.Br(),
            html.Mark('db_password: $DB_PASSWORD'),
            html.Br(), html.Br(),
            "To make sure the environment variables are available to the application, you need to define them in a separate .env file located in the current working directory. The .env file should contain one variable per line in the format VAR_NAME=VALUE. For example:",
            html.Br(),
            html.Mark('DB_PASSWORD=mysecretpassword'),
            html.Br(), html.Br(),
            "When the application starts up, it will read the config.yaml file and use the values in it to connect to the platform, database, and object storage. If any of the required environment variables are missing, the application will fail to start.",
        ])
    ],
        id="system-offcanvas",
        scrollable=True,
        title=[html.H4('SYSTEM CONFIGURATION [HELP]', className='text-info', style={'font-weight': 'bold'})],
        is_open=False,
    )

    models_offcanvas = dbc.Offcanvas(
    [
        html.P([
            "The models configuration file contains details of which data to parse from the raw JSON.",
            html.Br(), html.Br(),
            "Only the mentioned metadata table are supported",
            html.Br(), html.Br(), 'Visit ', 
            html.A('YouTube Data API documentation', href='https://developers.google.com/youtube/v3/docs', target='_blank'),
            " to build meta data table model for youtube.",
            html.Br(), html.Br(), "Visit ",
            html.A('Instagram Basic Display API documentation', href='https://developers.facebook.com/docs/instagram-basic-display-api', target='_blank'),
            " to build meta data table model for instagram.",
            html.Br(), html.Br(), "Visit ",
            "⚠️ Reddit `smc` is under development"
        ])
    ],
        id="models-offcanvas",
        scrollable=True,
        title=[html.H4('MODELS CONFIGURATION [HELP]', className='text-info', style={'font-weight': 'bold'})],
        is_open=False,
    )

    input_offcanvas = dbc.Offcanvas(
    [
        html.P([
            "The input configuration file contains details of what data needs to be extracted.",
            html.Br(), html.Br(), 'Visit ', 
            html.A('YouTube Data API documentation', href='https://developers.google.com/youtube/v3/docs', target='_blank'),
            " to build parameters dictionary for youtube.",
            html.Br(), html.Br(),
            "Incase of Instagram parameters are not supported as you will already pass access_token, so leave the dictionaries empty",
            html.Br(), html.Br(),
            "⚠️ Reddit `smc` is under development"
        ])
    ],
        id="input-offcanvas",
        scrollable=True,
        title=[html.H4('INPUT CONFIGURATION [HELP]', className='text-info', style={'font-weight': 'bold'})],
        is_open=False,
    )

    app.layout = dbc.Container([
        header, html.Hr(),
        indicator, html.Hr(),
        system_offcanvas, models_offcanvas, input_offcanvas,
        about, step_01, step_02, step_03,preview,
        success, error, html.Hr(),
        footer
    ], className='container', style={'width': '50%'})

    @app.callback(
        Output('system-offcanvas', 'is_open'),
        Input('button-system-offcanvas', 'n_clicks'),
        prevent_initial_call=True
    )
    def system_help_offcanvas(n_clicks):
        if n_clicks:
            return True
        else:
            return False
        
    @app.callback(
        Output('models-offcanvas', 'is_open'),
        Input('button-models-offcanvas', 'n_clicks'),
        prevent_initial_call=True
    )
    def models_help_offcanvas(n_clicks):
        if n_clicks:
            return True
        else:
            return False
        
    @app.callback(
        Output('input-offcanvas', 'is_open'),
        Input('button-input-offcanvas', 'n_clicks'),
        prevent_initial_call=True
    )
    def input_help_offcanvas(n_clicks):
        if n_clicks:
            return True
        else:
            return False

    @app.callback(
        [Output('about', 'style', allow_duplicate=True),
        Output('step-1', 'style', allow_duplicate=True),
        Output('about-header', 'disabled', allow_duplicate=True),
        Output('step-1-header', 'disabled', allow_duplicate=True)],
        [Input('button-config', 'n_clicks')],
        prevent_initial_call=True    
    )
    def build_config(n_clicks):
        if n_clicks:
            return {'display': 'none'}, {'display': 'block'}, True, False
        else:
            return {'display': 'block'}, {'display': 'none'}, False, True
        
    @app.callback(
        [Output('about', 'style', allow_duplicate=True),
        Output('step-1', 'style', allow_duplicate=True),
        Output('about-header', 'disabled', allow_duplicate=True),
        Output('step-1-header', 'disabled', allow_duplicate=True)],
        [Input('button-about', 'n_clicks')],
        prevent_initial_call=True    
    )
    def build_config(n_clicks):
        if n_clicks:
            return {'display': 'block'}, {'display': 'none'}, False, True
        else:
            return {'display': 'none'}, {'display': 'block'}, True, False
        
    @app.callback(
        Output('platform-cred', 'children'),
        Input('platform', 'value'),
    )
    def platform_fill(value):
        return platform_help_bgn[value]
    
    @app.callback(
        Output('database-cred', 'children'),
        Input('database', 'value'),
    )
    def database_fill(value):
        return database_help_bgn[value]
    
    @app.callback(
        Output('object_storage-cred', 'children'),
        Input('object_storage', 'value'),
    )
    def object_storage_fill(value):
        return object_storage_help_bgn[value]
    
    @app.callback(
        [Output('step-1', 'style'),
        Output('step-2', 'style', allow_duplicate=True),
        Output('step-1-header', 'disabled'),
        Output('step-2-header', 'disabled', allow_duplicate=True),
        Output('input-configuration', 'value')],
        Output('input-configuration-beginer', 'children'),
        [Input('button-next-step-1', 'n_clicks')],
        [State('platform', 'value')],
        prevent_initial_call=True
    )
    def handle_next_step_1(n_clicks, platform):
        if n_clicks:
            return {'display': 'none'}, {'display': 'block'}, True, False, input_help[platform], beginer_input[platform]
        else:
            return {'display': 'block'}, {'display': 'none'}, False, True, '', []

    @app.callback(
        [Output('step-1', 'style', allow_duplicate=True),
        Output('step-2', 'style', allow_duplicate=True)],
        Output('step-1-header', 'disabled', allow_duplicate=True),
        Output('step-2-header', 'disabled', allow_duplicate=True),
        [Input('button-prev-step-2', 'n_clicks')],
        prevent_initial_call=True
    )
    def handle_prev_step_2(n_clicks):
        if n_clicks:
            return {'display': 'block'}, {'display': 'none'}, False, True
        else:
            return {'display': 'none'}, {'display': 'block'}, True, False
        
    @app.callback(
        [Output('input-configuration', 'style'),
        Output('input-configuration-beginer', 'style')],
        [Input('button-input-playground', 'n_clicks')],
        [State('input-configuration', 'style'),
        State('input-configuration-beginer', 'style')],
        prevent_initial_call=True
    )
    def enable_input_switch(n_clicks, adv_style, bgn_style):
        if n_clicks:
            adv_style['display'] = 'none' if adv_style['display'] == 'block' else 'block'
            bgn_style['display'] = 'none' if bgn_style['display'] == 'flex' else 'flex'
        return adv_style, bgn_style
        
    @app.callback(
        [Output('step-2', 'style', allow_duplicate=True),
        Output('step-3', 'style', allow_duplicate=True),
        Output('step-2-header', 'disabled', allow_duplicate=True),
        Output('step-3-header', 'disabled', allow_duplicate=True),
        Output('models-configuration', 'value'),
        Output('models-configuration-beginer', 'children')],
        [Input('button-next-step-2', 'n_clicks')],
        [State('platform', 'value')],
        prevent_initial_call=True
    )
    def handle_next_step_2(n_clicks, platform):
        if n_clicks:
            return {'display': 'none'}, {'display': 'block'}, True, False, models_help[platform], beginer_models[platform]
        else:
            return {'display': 'block'}, {'display': 'none'}, False, True, '', []
        
    @app.callback(
        [Output('step-2', 'style'),
        Output('step-3', 'style', allow_duplicate=True)],
        Output('step-2-header', 'disabled'),
        Output('step-3-header', 'disabled', allow_duplicate=True),
        [Input('button-prev-step-3', 'n_clicks')],
        prevent_initial_call=True
    )
    def handle_prev_step_3(n_clicks):
        if n_clicks:
            return {'display': 'block'}, {'display': 'none'}, False, True
        else:
            return {'display': 'none'}, {'display': 'block'}, True, False

    @app.callback(
        [Output('models-configuration', 'style'),
        Output('models-configuration-beginer', 'style')],
        [Input('button-models-playground', 'n_clicks')],
        [State('models-configuration', 'style'),
        State('models-configuration-beginer', 'style')],
        prevent_initial_call=True
    )
    def enable_model_switch(n_clicks, adv_style, bgn_style):
        if n_clicks:
            adv_style['display'] = 'none' if adv_style['display'] == 'block' else 'block'
            bgn_style['display'] = 'none' if bgn_style['display'] == 'block' else 'block'
        return adv_style, bgn_style

    @app.callback(
        [Output('success', 'is_open'),
        Output('error', 'children'),
        Output('error', 'is_open'),
        Output('step-3', 'style'),
        Output('preview', 'style', allow_duplicate=True),
        Output('step-3-header', 'disabled'),
        Output('preview-header', 'disabled', allow_duplicate=True)],
        [Input('button-submit', 'n_clicks')],
        [State('platform', 'value'),
        State('object_storage-cred', 'children'),
        State('platform-cred', 'children'),
        State('database-cred', 'children'),
        State('models-configuration', 'value'),
        State('models-configuration', 'style'),
        State('models-configuration-beginer', 'children'),
        State('input-configuration', 'value'),
        State('input-configuration', 'style'),
        State('input-configuration-beginer', 'children')],
        prevent_initial_call=True
    )
    def handle_submit(n_clicks, ptf, obj_stg_cred, ptf_cred, dtb_cred, mdl_conf, mdl_conf_stl, mdl_conf_bgn, ipt_conf, ipt_conf_stl, ipt_conf_bgn):
        if n_clicks:
            system_configuration = {'platform': {}, 'database': {}, 'object_storage': {}}
            for entry in ptf_cred:
                entry = entry['props']['children']
                system_configuration['platform'][entry[0]['props']['value']] = entry[1]['props'].get('value')
            for entry in obj_stg_cred:
                entry = entry['props']['children']
                system_configuration['object_storage'][entry[0]['props']['value']] = entry[1]['props'].get('value')
            for entry in dtb_cred:
                entry = entry['props']['children']
                system_configuration['database'][entry[0]['props']['value']] = entry[1]['props'].get('value')
            if any(value is None for sub_dict in system_configuration.values() for value in sub_dict.values()):
                return False, f"Configuration files were not created: 'MISSING VALUES IN SYSTEM CONFIGURATION'", True, {'display': 'block'}, {'display': 'none'}, False, True
            if mdl_conf_stl['display'] == 'block':
                models_configuration = yaml.dump(yaml.safe_load(mdl_conf), sort_keys=False)
            else:
                models_configuration = {}
                for type in mdl_conf_bgn:
                    dict_name = type['props']['children'][0]['props']['children'].lower()
                    models_configuration[dict_name] = {}
                    for div in type['props']['children'][2]['props']['children'][0]['props']['children']:
                        entry = div['props']['children']
                        dict_value = entry[0]['props']['value']
                        dict_key = dict_value.split('.')[-1]
                        if entry[1]['props'].get('value') is not None:
                            dict_key = entry[0]['props']['value']
                        models_configuration[dict_name][dict_key] = dict_value
                models_configuration = yaml.dump(models_configuration, sort_keys=False)
            if ipt_conf_stl['display'] == 'block':
                input_configuration = yaml.dump(yaml.safe_load(ipt_conf), sort_keys=False)
            else:
                input_configuration = {}
                for div in ipt_conf_bgn[0]['props']['children']:
                    div = div['props']['children']
                    if div[0]['type'] == 'H6':
                        input_configuration[div[0]['props']['children'].lower()] = {}
                        if len(div)>2:
                            input_configuration[div[0]['props']['children'].lower()] = {}
                            for ele_num in range(2, len(div)):
                                if div[ele_num]['props']['children'][1]['props'].get('value') is not None:
                                    input_configuration[div[0]['props']['children'].lower()][div[ele_num]['props']['children'][0]['props']['value']] = div[ele_num]['props']['children'][1]['props']['value']
                    if div[0]['type'] == 'Input':
                        if div[1]['props'].get('value') is not None:
                            input_configuration[div[0]['props']['value']] = div[1]['props']['value']
                input_configuration = yaml.dump(input_configuration, sort_keys=False)
            s3 = boto3.resource('s3', endpoint_url="http://"+system_configuration.get('object_storage', {}).get('endpoint_url') if system_configuration.get('object_storage', {}).get('endpoint_url') is not None else None, aws_access_key_id=system_configuration.get('object_storage', {}).get('aws_access_key_id'), aws_secret_access_key=system_configuration.get('object_storage', {}).get('aws_secret_access_key'))
            try:
                obj = s3.Object(system_configuration.get('object_storage', {}).get('bucket_name'), f'{ptf.lower()}/input_configuration.yaml')
                obj.put(Body=input_configuration)
                obj = s3.Object(system_configuration.get('object_storage', {}).get('bucket_name'), f'{ptf.lower()}/models_configuration.yaml')
                obj.put(Body=models_configuration)
                with open('config.yaml', 'w') as f:
                    yaml.dump(system_configuration, f, sort_keys=False)
            except Exception as e:
                return False, f"Configuration files were not created: '{str(e).upper()}'", True, {'display': 'block'}, {'display': 'none'}, False, True
            return True, '', False, {'display': 'none'}, {'display': 'block'}, True, False

    @app.callback(
        Output("extracting", "style"),
        # Output('tables-dropdown', 'options'),
        # Output('tables-dropdown', 'value'),
        [Input("preview-header", "disabled")],
        prevent_initial_call = True
    )
    def extract(disabled):
        if not disabled: 
            SocialMediaConnector('config.yaml').run()
            # with open('config.yaml', 'r') as f:
            #     config = yaml.safe_load(f)
            # if config['database']['service_name'] == 'postgresql':
            #     conn = psycopg2.connect(
            #         host=config['database']['host'],
            #         port=config['database']['port'],
            #         database=config['database']['database'],
            #         user=config['database']['user'],
            #         password=config['database']['password']
            #     )
            #     cursor = conn.cursor()
            #     try:
            #         query = f"SELECT table_name FROM information_schema.tables WHERE table_schema = '{config['database']['schema']}'"
            #         cursor.execute(query)
            #         table_names = [row[0] for row in cursor.fetchall()]
            #     except:
            #         table_names = ['Error: unable to load table names']
            #     cursor.close()
            #     conn.close()
            # elif config['database']['service_name'] == 'snowflake':
            #     conn = snowflake.connector.connect(
            #         user=config['database']['user'],
            #         password=config['database']['password'],
            #         account=config['database']['account'],
            #         warehouse=config['database']['warehouse'],
            #         database=config['database']['database'],
            #         schema=config['database']['schema']
            #     )
            #     cursor = conn.cursor()
            #     try:
            #         query = f"SHOW TABLES IN {config['database']['schema']}"
            #         cursor.execute(query)
            #         table_names = [row[1] for row in cursor.fetchall()]  
            #     except:
            #         table_names = ['Error: unable to load table names']
            #     cursor.close()
            #     conn.close()
            return {'display': 'none'}
        
    # @app.callback(
    #     Output('table', 'children'),
    #     Input('tables-dropdown', 'value'),
    #     prevent_initial_call = True
    # )
    # def update_table(table_name):
    #     with open('config.yaml', 'r') as f:
    #         config = yaml.safe_load(f)
    #     if config['database']['service_name'] == 'postgresql':
    #         conn = psycopg2.connect(
    #             host=config['database']['host'],
    #             port=config['database']['port'],
    #             database=config['database']['database'],
    #             user=config['database']['user'],
    #             password=config['database']['password']
    #         )
    #         cursor = conn.cursor()
    #         try:
    #             query = f"SELECT * FROM {table_name} ORDER BY timestamp DESC LIMIT 100;"
    #             cursor.execute(query)
    #             rows = cursor.fetchall()
    #             table_header = [html.Th(col[0], style=header_style) for col in cursor.description]
    #             table_rows = []
    #             for row in rows:
    #                 table_row = [html.Td(str(val), style=cell_style) for val in row]
    #                 table_rows.append(html.Tr(table_row))
    #             table = [
    #                 html.Thead(html.Tr(table_header)),
    #                 html.Tbody(table_rows)
    #             ]
    #         except:
    #             table = ['Error: unable to load table']
    #         cursor.close()
    #         conn.close()
    #     elif config['database']['service_name'] == 'snowflake':
    #         conn = snowflake.connector.connect(
    #             user=config['database']['user'],
    #             password=config['database']['password'],
    #             account=config['database']['account'],
    #             warehouse=config['database']['warehouse'],
    #             database=config['database']['database'],
    #             schema=config['database']['schema']
    #         )
    #         cursor = conn.cursor()
    #         try:
    #             query = f"SELECT * FROM {table_name} ORDER BY timestamp DESC LIMIT 100;"
    #             cursor.execute(query)
    #             rows = cursor.fetchall()
    #             table_header = [html.Th(col[0], style=header_style) for col in cursor.description]
    #             table_rows = []
    #             for row in rows:
    #                 table_row = [html.Td(str(val), style=cell_style) for val in row]
    #                 table_rows.append(html.Tr(table_row))
    #             table = [
    #                 html.Thead(html.Tr(table_header)),
    #                 html.Tbody(table_rows)
    #             ] 
    #         except:
    #             table = ['Error: unable to load table']
    #         cursor.close()
    #         conn.close()
    #     return table

    @app.callback(
        Output("channels", "children"),
        [Input("button-channels", "n_clicks"),
        Input("button-clear-channels", "n_clicks")],
        [State("channels", "children")]
    )
    def modify_channels(add_clicks, clear_clicks, children):
        ctx = dash.callback_context
        trigger_id = ctx.triggered[0]['prop_id'].split('.')[0]

        if trigger_id == 'button-channels' and add_clicks > 0:
            new_input = html.Div(
                style={'display': 'flex', 'flexDirection': 'row'}, className='mb-1',
                children=[
                    dcc.Dropdown(clearable=False, options=models_channels, value=models_channels[0], persistence=True, style={'border-width': '2px', 'border-color': 'black', 'width': '100%'}),
                    dcc.Input(type='text', placeholder="alias (optional)", style={'border-radius': 5, 'border-style': 'solid black', 'border-width': '2px'})
                    ])
            children.append(new_input)
        elif trigger_id == 'button-clear-channels' and clear_clicks > 0:
            children = []

        return children
    
    @app.callback(
        Output("playlists", "children"),
        [Input("button-playlists", "n_clicks"),
        Input("button-clear-playlists", "n_clicks")],
        [State("playlists", "children")]
    )
    def modify_playlists(add_clicks, clear_clicks, children):
        ctx = dash.callback_context
        trigger_id = ctx.triggered[0]['prop_id'].split('.')[0]

        if trigger_id == 'button-playlists' and add_clicks > 0:
            new_input = html.Div(
                style={'display': 'flex', 'flexDirection': 'row'}, className='mb-1',
                children=[
                    dcc.Dropdown(clearable=False, options=models_playlists, value=models_playlists[0], persistence=True, style={'border-width': '2px', 'border-color': 'black', 'width': '100%'}),
                    dcc.Input(type='text', placeholder="alias (optional)", style={'border-radius': 5, 'border-style': 'solid black', 'border-width': '2px'})
                    ])
            children.append(new_input)
        elif trigger_id == 'button-clear-playlists' and clear_clicks > 0:
            children = []

        return children
    
    @app.callback(
        Output("videos", "children"),
        [Input("button-videos", "n_clicks"),
        Input("button-clear-videos", "n_clicks")],
        [State("videos", "children")]
    )
    def modify_videos(add_clicks, clear_clicks, children):
        ctx = dash.callback_context
        trigger_id = ctx.triggered[0]['prop_id'].split('.')[0]

        if trigger_id == 'button-videos' and add_clicks > 0:
            new_input = html.Div(
                style={'display': 'flex', 'flexDirection': 'row'}, className='mb-1',
                children=[
                    dcc.Dropdown(clearable=False, options=models_videos, value=models_videos[0], persistence=True, style={'border-width': '2px', 'border-color': 'black', 'width': '100%'}),
                    dcc.Input(type='text', placeholder="alias (optional)", style={'border-radius': 5, 'border-style': 'solid black', 'border-width': '2px'})
                    ])
            children.append(new_input)
        elif trigger_id == 'button-clear-videos' and clear_clicks > 0:
            children = []

        return children
    
    @app.callback(
        Output("comments", "children"),
        [Input("button-comments", "n_clicks"),
        Input("button-clear-comments", "n_clicks")],
        [State("comments", "children")]
    )
    def modify_comments(add_clicks, clear_clicks, children):
        ctx = dash.callback_context
        trigger_id = ctx.triggered[0]['prop_id'].split('.')[0]

        if trigger_id == 'button-comments' and add_clicks > 0:
            new_input = html.Div(
                style={'display': 'flex', 'flexDirection': 'row'}, className='mb-1',
                children=[
                    dcc.Dropdown(clearable=False, options=models_comments, value=models_comments[0], persistence=True, style={'border-width': '2px', 'border-color': 'black', 'width': '100%'}),
                    dcc.Input(type='text', placeholder="alias (optional)", style={'border-radius': 5, 'border-style': 'solid black', 'border-width': '2px'})
                    ])
            children.append(new_input)
        elif trigger_id == 'button-clear-comments' and clear_clicks > 0:
            children = []

        return children
    
    @app.callback(
        Output("users", "children"),
        [Input("button-users", "n_clicks"),
        Input("button-clear-users", "n_clicks")],
        [State("users", "children")]
    )
    def modify_users(add_clicks, clear_clicks, children):
        ctx = dash.callback_context
        trigger_id = ctx.triggered[0]['prop_id'].split('.')[0]

        if trigger_id == 'button-users' and add_clicks > 0:
            new_input = html.Div(
                style={'display': 'flex', 'flexDirection': 'row'}, className='mb-1',
                children=[
                    dcc.Dropdown(clearable=False, options=models_users, value=models_users[0], persistence=True, style={'border-width': '2px', 'border-color': 'black', 'width': '100%'}),
                    dcc.Input(type='text', placeholder="alias (optional)", style={'border-radius': 5, 'border-style': 'solid black', 'border-width': '2px'})
                    ])
            children.append(new_input)
        elif trigger_id == 'button-clear-users' and clear_clicks > 0:
            children = []

        return children
    
    @app.callback(
        Output("media", "children"),
        [Input("button-media", "n_clicks"),
        Input("button-clear-media", "n_clicks")],
        [State("media", "children")]
    )
    def modify_media(add_clicks, clear_clicks, children):
        ctx = dash.callback_context
        trigger_id = ctx.triggered[0]['prop_id'].split('.')[0]

        if trigger_id == 'button-media' and add_clicks > 0:
            new_input = html.Div(
                style={'display': 'flex', 'flexDirection': 'row'}, className='mb-1',
                children=[
                    dcc.Dropdown(clearable=False, options=models_media, value=models_media[0], persistence=True, style={'border-width': '2px', 'border-color': 'black', 'width': '100%'}),
                    dcc.Input(type='text', placeholder="alias (optional)", style={'border-radius': 5, 'border-style': 'solid black', 'border-width': '2px'})
                    ])
            children.append(new_input)
        elif trigger_id == 'button-clear-media' and clear_clicks > 0:
            children = []

        return children
    
    @app.callback(
        Output("posts", "children"),
        [Input("button-posts", "n_clicks"),
        Input("button-clear-posts", "n_clicks")],
        [State("posts", "children")]
    )
    def modify_posts(add_clicks, clear_clicks, children):
        ctx = dash.callback_context
        trigger_id = ctx.triggered[0]['prop_id'].split('.')[0]

        if trigger_id == 'button-posts' and add_clicks > 0:
            new_input = html.Div(
                style={'display': 'flex', 'flexDirection': 'row'}, className='mb-1',
                children=[
                    dcc.Dropdown(clearable=False, options=models_posts, value=models_posts[0], persistence=True, style={'border-width': '2px', 'border-color': 'black', 'width': '100%'}),
                    dcc.Input(type='text', placeholder="alias (optional)", style={'border-radius': 5, 'border-style': 'solid black', 'border-width': '2px'})
                    ])
            children.append(new_input)
        elif trigger_id == 'button-clear-posts' and clear_clicks > 0:
            children = []

        return children
    
    @app.callback(
        Output("instagram", "children"),
        [Input("button-instagram-clear", "n_clicks")],
        State("instagram", "children"),
        prevent_initial_callback=True
    )
    def modify_instagram(clear_n_clicks, children):
        ctx = dash.callback_context
        # if ctx.triggered_id == 'button-input-instagram-limit':
        #     update_child = html.Div(
        #         style={'display': 'flex', 'flexDirection': 'row', 'border': '2px solid black', "background-color": "white", "padding": "10px"}, className='mb-2',
        #         children=[
        #             dcc.Input(type='text', value='default_limit', style={'font-weight': 'bold', 'border-radius': 5, 'border-style': 'solid black', 'border-width': '2px'}, disabled=True),
        #             dcc.Input(type='number', value=5000, style={'border-radius': 5, 'border-style': 'solid black', 'border-width': '2px', 'width': '100%'})
        #             ])
        #     children.append(update_child)
        if ctx.triggered_id == 'button-instagram-clear':
            children = [
                html.Div([
                    dcc.Input(type='text', value='default_limit', style={'font-weight': 'bold', 'border-radius': 5, 'border-style': 'solid black', 'border-width': '2px'}, disabled=True),
                    dcc.Input(type='number', value=5000, style={'border-radius': 5, 'border-style': 'solid black', 'border-width': '2px', 'width': '100%'})
                    ], style={'display': 'flex', 'flexDirection': 'row', 'border': '2px solid black', "background-color": "white", "padding": "10px"}, className='mb-2'),
                html.Div([
                    html.H6('USERS', className='text-info', style={'font-weight': 'bold'}),
                    html.Hr(),
                    ], style={'border': '2px solid black', "background-color": "white", "padding": "10px"}, className='mb-2'),
                html.Div([
                    html.H6('MEDIA', className='text-info', style={'font-weight': 'bold'}),
                    html.Hr(),
                    ], style={'border': '2px solid black', "background-color": "white", "padding": "10px"}, className='mb-2')
            ]
        return children
    
    @app.callback(
        Output("reddit", "children"),
        [Input("button-input-posts", "n_clicks"),
        Input("button-input-reddit-limit", "n_clicks"),
        Input("button-reddit-clear", "n_clicks")],
        State("reddit", "children"),
        prevent_initial_callback=True
    )
    def modify_reddit(posts_n_clicks, limit_n_clicks, clear_n_clicks, children):
        ctx = dash.callback_context
        if ctx.triggered_id == 'button-input-posts':
            update_child = html.Div([
                    html.H6('POSTS', className='text-info', style={'font-weight': 'bold'}),
                    html.Hr(),
                    html.Div(
                    style={'display': 'flex', 'flexDirection': 'row', "background-color": "white"}, 
                    children=[
                        dcc.Input(type='text', value='subreddit', style={'font-weight': 'bold', 'border-radius': 5, 'border-style': 'solid black', 'border-width': '2px'}, disabled=True),
                        dcc.Input(type='text', style={'border-radius': 5, 'border-style': 'solid black', 'border-width': '2px', 'width': '100%'})
                        ]),
                    html.Div(
                    style={'display': 'flex', 'flexDirection': 'row', "background-color": "white"}, 
                    children=[
                        dcc.Input(type='text', value='type', style={'font-weight': 'bold', 'border-radius': 5, 'border-style': 'solid black', 'border-width': '2px'}, disabled=True),
                        dcc.Input(type='text', style={'border-radius': 5, 'border-style': 'solid black', 'border-width': '2px', 'width': '100%'})
                        ])
                    ], style={'border': '2px solid black', "background-color": "white", "padding": "10px"}, className='mb-2 mt-2')
            children.append(update_child)
        elif ctx.triggered_id == 'button-input-reddit-limit':
            update_child = html.Div(
                style={'display': 'flex', 'flexDirection': 'row', 'border': '2px solid black', "background-color": "white", "padding": "10px"}, className='mb-2',
                children=[
                    dcc.Input(type='text', value='default_limit', style={'font-weight': 'bold', 'border-radius': 5, 'border-style': 'solid black', 'border-width': '2px'}, disabled=True),
                    dcc.Input(type='number', value=5000, style={'border-radius': 5, 'border-style': 'solid black', 'border-width': '2px', 'width': '100%'})
                    ])
            children.append(update_child)
        elif ctx.triggered_id == 'button-reddit-clear':
            children = []
        return children
    
    @app.callback(
        Output("youtube", "children"),
        [Input("button-input-channels", "n_clicks"),
        Input("button-input-videos", "n_clicks"),
        Input("button-input-playlists", "n_clicks"),
        Input("button-input-comments", "n_clicks"),
        Input("button-input-search", "n_clicks"),
        Input("button-input-youtube-limit", "n_clicks"),
        Input("button-input-youtube-get-comments", 'n_clicks'),
        Input("button-input-youtube-followup-search", "n_clicks"),
        Input("button-youtube-clear", "n_clicks")],
        State("youtube", "children"),
        prevent_initial_callback=True
    )
    def modify_youtube(channels_n_clicks, videos_n_clicks, playlists_n_clicks, comments_n_clicks, search_n_clicks, limit_n_clicks, get_comments_n_clicks, followup_n_clicks, clear_n_clicks, children):
        ctx = dash.callback_context
        if ctx.triggered_id == 'button-input-channels':
            update_child = html.Div([
                    html.H6('CHANNELS', className='text-info', style={'font-weight': 'bold'}),
                    html.Hr(),
                    html.Div(
                    style={'display': 'flex', 'flexDirection': 'row', "background-color": "white"}, 
                    children=[
                        dcc.Input(type='text', value='id', style={'font-weight': 'bold', 'border-radius': 5, 'border-style': 'solid black', 'border-width': '2px'}, disabled=True),
                        dcc.Input(type='text', style={'border-radius': 5, 'border-style': 'solid black', 'border-width': '2px', 'width': '100%'})
                        ])
                    ], style={'border': '2px solid black', "background-color": "white", "padding": "10px"}, className='mb-2 mt-2')
            children.append(update_child)
        elif ctx.triggered_id == 'button-input-videos':
            update_child = html.Div([
                    html.H6('VIDEOS', className='text-info', style={'font-weight': 'bold'}),
                    html.Hr(),
                    html.Div(
                    style={'display': 'flex', 'flexDirection': 'row', "background-color": "white"}, 
                    children=[
                        dcc.Input(type='text', value='id', style={'font-weight': 'bold', 'border-radius': 5, 'border-style': 'solid black', 'border-width': '2px'}, disabled=True),
                        dcc.Input(type='text', style={'border-radius': 5, 'border-style': 'solid black', 'border-width': '2px', 'width': '100%'})
                        ])
                    ], style={'border': '2px solid black', "background-color": "white", "padding": "10px"}, className='mb-2 mt-2')
            children.append(update_child)
        elif ctx.triggered_id == 'button-input-playlists':
            update_child = html.Div([
                    html.H6('PLAYLISTS', className='text-info', style={'font-weight': 'bold'}),
                    html.Hr(),
                    html.Div(
                    style={'display': 'flex', 'flexDirection': 'row', "background-color": "white"}, 
                    children=[
                        dcc.Input(type='text', value='id', style={'font-weight': 'bold', 'border-radius': 5, 'border-style': 'solid black', 'border-width': '2px'}, disabled=True),
                        dcc.Input(type='text', style={'border-radius': 5, 'border-style': 'solid black', 'border-width': '2px', 'width': '100%'})
                        ])
                    ], style={'border': '2px solid black', "background-color": "white", "padding": "10px"}, className='mb-2 mt-2')
            children.append(update_child)
        elif ctx.triggered_id == 'button-input-comments':
            update_child = html.Div([
                    html.H6('COMMENTS', className='text-info', style={'font-weight': 'bold'}),
                    html.Hr(),
                    html.Div(
                    style={'display': 'flex', 'flexDirection': 'row', "background-color": "white"}, 
                    children=[
                        dcc.Input(type='text', value='videoId', style={'font-weight': 'bold', 'border-radius': 5, 'border-style': 'solid black', 'border-width': '2px'}, disabled=True),
                        dcc.Input(type='text', style={'border-radius': 5, 'border-style': 'solid black', 'border-width': '2px', 'width': '100%'})
                        ])
                    ], style={'border': '2px solid black', "background-color": "white", "padding": "10px"}, className='mb-2 mt-2')
            children.append(update_child)
        elif ctx.triggered_id == 'button-input-search':
            update_child = html.Div([
                    html.H6('SEARCH', className='text-info', style={'font-weight': 'bold'}),
                    html.Hr(),
                    html.Div(
                    style={'display': 'flex', 'flexDirection': 'row', "background-color": "white"}, 
                    children=[
                        dcc.Input(type='text', value='q', style={'font-weight': 'bold', 'border-radius': 5, 'border-style': 'solid black', 'border-width': '2px'}, disabled=True),
                        dcc.Input(type='text', style={'border-radius': 5, 'border-style': 'solid black', 'border-width': '2px', 'width': '100%'})
                        ])
                    ], style={'border': '2px solid black', "background-color": "white", "padding": "10px"}, className='mb-2 mt-2')
            children.append(update_child)
        elif ctx.triggered_id == 'button-input-youtube-limit':
            update_child = html.Div(
                style={'display': 'flex', 'flexDirection': 'row', 'border': '2px solid black', "background-color": "white", "padding": "10px"}, className='mb-2 mt-2', 
                children=[
                    dcc.Input(type='text', value='default_limit', style={'font-weight': 'bold', 'border-radius': 5, 'border-style': 'solid black', 'border-width': '2px'}, disabled=True),
                    dcc.Input(type='number', value=5000, style={'border-radius': 5, 'border-style': 'solid black', 'border-width': '2px', 'width': '100%'})
                    ])
            children.append(update_child)
        elif ctx.triggered_id == 'button-input-youtube-get-comments':
            update_child = html.Div(
                style={'display': 'flex', 'flexDirection': 'row', 'border': '2px solid black', "background-color": "white", "padding": "10px"}, className='step-header-container d-flex justify-content-between mb-2 mt-2', 
                children=[
                    dcc.Input(type='text', value='get_comments', style={'font-weight': 'bold', 'border-radius': 5, 'border-style': 'solid black', 'border-width': '2px'}, disabled=True),
                    dbc.RadioItems(options=[{"label": "False", "value": False}, {"label": "True", "value": True}], value=False, inline=True),
                    ])
            children.append(update_child)
        elif ctx.triggered_id == 'button-input-youtube-followup-search':
            update_child = html.Div(
                style={'display': 'flex', 'flexDirection': 'row', 'border': '2px solid black', "background-color": "white", "padding": "10px"}, className='step-header-container d-flex justify-content-between mb-2 mt-2', 
                children=[
                    dcc.Input(type='text', value='follow_up_on_search', style={'font-weight': 'bold', 'border-radius': 5, 'border-style': 'solid black', 'border-width': '2px'}, disabled=True),
                    dbc.RadioItems(options=[{"label": "False", "value": False}, {"label": "True", "value": True}], value=False, inline=True),
                    ])
            children.append(update_child)
        elif ctx.triggered_id == 'button-youtube-clear':
            children = []
        return children
    
    # app.clientside_callback(
    #     ClientsideFunction(namespace="clientside", function_name="make_draggable"),
    #     Output("instagram", "data-drag"),
    #     [Input("instagram", "id")]
    # )
    # app.clientside_callback(
    #     ClientsideFunction(namespace="clientside", function_name="make_draggable"),
    #     Output("youtube", "data-drag"),
    #     [Input("youtube", "id")]
    # )
    
    app.run(debug=True)