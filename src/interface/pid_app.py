import re

import dash
import dash_html_components as html
import dash_core_components as dcc
from dash.dependencies import Input, Output

app = dash.Dash(__name__)

app.title = 'PID Toolkit'

app.layout = html.Div(className='page', children=[
    html.Div(className='app-header', children=[
        html.Div(className='app-header--logo', children=[
            html.Img(src='/assets/logo_nl.png', height="80")
        ]),
        html.Div(className='app-header--titlewrap', children=[
            html.Div(className='app-header--title', children=[
                html.H1('PID Generation toolkit')
            ]),
            html.Div(className='app-header--subtitle', children=[
                html.Div('''
                    PID Toolkit: Generate PIDs for museum objects
                ''')
            ])
        ])
    ]),
    html.Div(className='app-body', children=[
        html.Div(className='app-body--run', children=[
            html.H2('Core options'),
            # In/Out
            # Toggles for EI/Departments

        ]),
        html.Div(className='app-body--pidformat', children=[
            html.H2('PID format'),

            html.Div([
                html.Div(className='app-body--selections', children=[
                    html.Div([
                        html.Label('PID syntax to use:'),
                        dcc.RadioItems(
                            id='pid_type',
                            options=[
                                {'label': 'meemoo syntax', 'value': 'meemoo'},
                                {'label': 'OSLO syntax', 'value': 'oslo'},
                            ],
                            value='meemoo'
                        ),
                    ]),
                    html.Div(children=[
                        html.Label('PIDs to generate'),
                        dcc.Checklist(id='pid_generate',
                                      options=[
                                          {'label': 'Identifier', 'value': 'id'},
                                          {'label': 'Data', 'value': 'data'},
                                          {'label': 'Document', 'value': 'doc'},
                                          {'label': 'Representation', 'value': 'representation'}
                                      ],
                                      value=['id', 'data', 'representation'])
                    ])
                ]),
                html.Div(className='app-body--textfields', children=[
                    html.Div([
                        html.Label('Base URL:'),
                        html.Br(),
                        dcc.Input(id='base_url', value='https://www.museum.be/', type='text')
                    ]),
                    html.Div(children=[
                        html.Label('PID concept:'),
                        html.Br(),
                        dcc.Input(id='pid_concept', value='work', type='text')
                    ]),
                    html.Div(children=[
                        html.Label('Additional path elements:x'),
                        html.Br(),
                        dcc.Input(id='pid_pattern', value='/collection/', type='text')
                    ])
                ])
            ]),
            html.Div(className='app-body--pidexample', id='pid_example')
        ]),
        html.Div(className='app-body--file', children=[
            html.H2('File options'),

            html.Div([
                html.Div(className='app-body--filecore', children=[
                    html.Div([
                        html.Label('Column name for record numbers:'),
                        html.Br(),
                        dcc.Input(id='record_numbers', value='priref', type='text')
                    ]),
                    html.Div([
                        html.Label('Column name for object numbers: (e.g. "object_numbers")'),
                        html.Br(),
                        dcc.Input(id='object_numbers', value='object_number', type='text')
                    ])
                ]),
                html.Div(className='app-body--fileadlibei', children=[
                    html.Div([
                        html.Label('Column name for institution:'),
                        html.Br(),
                        dcc.Input(id='institution_field', value='institution.name', type='text')
                    ]),
                    html.Div([
                        html.Label('Institution name:'),
                        html.Br(),
                        dcc.Input(id='institution_name', value='Vlaamse Kunstcollectie', type='text')
                    ]),
                    html.Div([
                        html.Label('Column name for department:'),
                        html.Br(),
                        dcc.Input(id='department_field', value='administration_name', type='text')
                    ])
                ])
            ])
        ])
    ]),
    html.Footer(className='app-footer', children=[
        html.Div(className='app-footer--content', children=[
            html.Div(className='app-footer--logo', children=[
                html.Img(src='/assets/Vlaanderen verbeelding werkt_vol.png', height="80")
            ]),
            html.Div(className='app-footer--text', children=[
                'Find the source code at',
                html.A(href='https://github.com/robwyse/pidtoolkit', children='GitHub')
            ]),
        ])
    ])
])


@app.callback(
    Output(component_id='pid_example', component_property='children'),
    Input('pid_type', 'value'),
    Input('base_url', 'value'),
    Input('pid_concept', 'value'),
    Input('pid_generate', 'value'),
    Input('pid_pattern', 'value'))
def update_output_div(pid_type, base_url, pid_concept, pid_generate, pid_pattern):
    id_pid = ""
    data_pid = ""
    doc_pid = ""
    representation_pid = ""
    if pid_type == "oslo":
        if "id" in pid_generate:
            id_pid = re.sub('(?<!ttps:|http:)/{2,}', '/', base_url + "/" + "id" + "/" + pid_concept + "/12345678")
        if "data" in pid_generate:
            data_pid = re.sub('(?<!ttps:|http:)/{2,}', '/', base_url + "/" + "data" + "/" + pid_concept + "/12345678")
        if "doc" in pid_generate:
            doc_pid = re.sub('(?<!ttps:|http:)/{2,}', '/', base_url + "/" + "doc" + "/" + pid_concept + "/12345678")
        if "representation" in pid_generate:
            representation_pid = re.sub('(?<!ttps:|http:)/{2,}', '/', base_url + "/" + "representation" + "/"
                                        + pid_concept + "/12345678")
    elif pid_type == "meemoo":
        if "id" in pid_generate:
            id_pid = re.sub('(?<!ttps:|http:)/{2,}', '/', base_url + pid_pattern + pid_concept + "/"
                            + "id" + "/12345678")
        if "data" in pid_generate:
            data_pid = re.sub('(?<!ttps:|http:)/{2,}', '/', base_url + pid_pattern + pid_concept + "/"
                              + "data" + "/12345678")
        if "doc" in pid_generate:
            doc_pid = re.sub('(?<!ttps:|http:)/{2,}', '/', base_url + pid_pattern + pid_concept + "/"
                             + "doc" + "/12345678")
        if "representation" in pid_generate:
            representation_pid = re.sub('(?<!ttps:|http:)/{2,}', '/', base_url + pid_pattern + pid_concept + "/"
                                        + "representation" + "/12345678")
    else:
        id_pid = ""
        data_pid = ""
        doc_pid = ""
        representation_pid = ""

    return html.Div([
        html.H3('Example PIDs:'),
        html.P(f'{id_pid}', style={'padding-left': '25px'}),
        html.P(f'{data_pid}', style={'padding-left': '25px'}),
        html.P(f'{doc_pid}', style={'padding-left': '25px'}),
        html.P(f'{representation_pid}', style={'padding-left': '25px'})
    ])


if __name__ == '__main__':
    app.run_server(debug=True)
