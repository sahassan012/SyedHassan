import json
import dash
import dash_table
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, State
import pandas as pd
from mysql_utils import *
from mongodb_utils import *
from neo4j_utils import *
app = dash.Dash(__name__)

professors = get_all_professors()
professor_names = [prof["name"] for prof in professors]

app.layout = html.Div([
    html.Div([
        html.Div([
            html.H3("Select a faculty member:", style={"margin-bottom": "20px"}),
            dcc.Dropdown(
                id="faculty-dropdown",
                options=[{"label": name, "value": name} for name in professor_names],
                value='',
                style={"width": "50%"}
            ),
            html.Div(id='output-container-1', children=[], style={"margin-top": "20px"})
        ], style={"width": "33%", "display": "inline-block", "padding": "20px", "border": "1px solid #ccc", "box-shadow": "0 4px 8px 0 rgba(0, 0, 0, 0.2), 0 6px 20px 0 rgba(0, 0, 0, 0.19)", "border-radius": "10px"}),
        html.Div([
                html.H3("Select a faculty member to delete:", style={"margin-bottom": "20px"}),
                dcc.Dropdown(
                    id="faculty-delete-dropdown",
                    options=[{"label": name, "value": name} for name in professor_names],
                    value='',
                    style={"width": "100%"}
                ),
                html.Button('Delete', id='delete-faculty-button', n_clicks=0),
                html.Div(id='output-container')
            ], style={"width": "33%", "display": "inline-block", "padding": "20px", "border": "1px solid #ccc", "box-shadow": "0 4px 8px 0 rgba(0, 0, 0, 0.2), 0 6px 20px 0 rgba(0, 0, 0, 0.19)", "border-radius": "10px"}),
        html.Div([
            html.H3("Add New Faculty"),
            html.Label('Name:'),
            dcc.Input(id='name-input', type='text', value='', style={"width": "100%"}),
            html.Label('Position:'),
            dcc.Input(id='position-input', type='text', value='', style={"width": "100%"}),
            html.Label('Research Interest:'),
            dcc.Input(id='research-input', type='text', value='', style={"width": "100%"}),
            html.Label('Email:'),
            dcc.Input(id='email-input', type='email', value='', style={"width": "100%"}),
            html.Label('Phone:'),
            dcc.Input(id='phone-input', type='tel', value='', style={"width": "100%"}),
            html.Label('University:'),
            dcc.Input(id='university-input', type='text', value='', style={"width": "100%"}),
            html.Button('Add Faculty', id='add-faculty-button', n_clicks=0),
            html.Div(id='output-container-3')
        ], style={"width": "33%", "display": "inline-block", "padding": "20px", "border": "1px solid #ccc", "box-shadow": "0 4px 8px 0 rgba(0, 0, 0, 0.2), 0 6px 20px 0 rgba(0, 0, 0, 0.19)", "border-radius": "10px"}) 

    ], style={"display": "flex", "justify-content": "center"}),
    html.Div([
        html.H3("Faculty Data Graph"),
        dcc.Graph(
            id="sample-faculty-data-graph",
            figure={
                'data': [
                    {'x': [1, 2, 3], 'y': [4, 1, 2], 'type': 'bar', 'name': 'Data 1'},
                    {'x': [1, 2, 3], 'y': [2, 4, 5], 'type': 'bar', 'name': 'Data 2'},
                ],
                'layout': {
                    'title': 'Sample Faculty Data'
                }
            }
        )
    ], style={"width": "33%", "display": "inline-block", "padding": "20px", "border": "1px solid #ccc", "box-shadow": "0 4px 8px 0 rgba(0, 0, 0, 0.2), 0 6px 20px 0 rgba(0, 0, 0, 0.19)", "border-radius": "10px"}),
])

@app.callback(
    Output(component_id="output-container-1", component_property="children"),
    Input("faculty-dropdown", "value")
)
def update_faculty_details(selected_name):
    if selected_name is None or selected_name == '':
        return []
    
    selected_faculty = get_professor_by_name(selected_name)[0]

    if not selected_faculty:
        return [html.P("No faculty member found.")]
    
    return [
        html.P(f"Name: {selected_faculty['name']}"),
        html.P(f"Position: {selected_faculty['position']}"),
        html.P(f"Research Interest: {selected_faculty['researchInterest']}"),
        html.P(f"Email: {selected_faculty['email']}"),
        html.P(f"Phone: {selected_faculty['phone']}"),
        html.P(f"University: {selected_faculty['affiliation']['name']}"),
        html.Img(src=selected_faculty['photoUrl'], width=200)
    ]

@app.callback(
    Output('output-container', 'children'),
    [Input('delete-faculty-button', 'n_clicks')],
    [dash.dependencies.State('faculty-delete-dropdown', 'value')]
)
def update_remove_faculty_widget(n_clicks, name):
    if n_clicks > 0:
        remove_faculty(name)
        return f'Faculty member {name} has been deleted.'
    return ''


faculty_data = []
@app.callback(
    Output('output-container-3', 'children'),
    [Input('add-faculty-button', 'n_clicks')],
    [
        State('name-input', 'value'),
        State('position-input', 'value'),
        State('research-input', 'value'),
        State('email-input', 'value'),
        State('phone-input', 'value'),
        State('university-input', 'value'),
    ]
)
def update_output(n_clicks, name, position, research, email, phone, university):
    if n_clicks > 0:
        faculty_tuple = (name, position, research, email, phone, university)
        add_faculty(faculty_tuple)
        return f'Faculty member {name} has been added.'
    return ''


if __name__ == '__main__':
    app.run_server(debug=True)
