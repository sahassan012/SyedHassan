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
        # First widget - Search faculty
        html.Div([
            html.H3("Select a faculty member:", style={"margin-bottom": "20px"}),
            dcc.Dropdown(
                id="faculty-dropdown",
                options=[{"label": name, "value": name} for name in professor_names],
                value='',
                style={"width": "100%"}
            ),
            html.Div(id='output-container', children=[
                html.P(id='professor-name'),
                html.P(id='professor-position'),
                html.P(id='professor-interest'),
                html.P(id='professor-email'),
                html.P(id='professor-phone'),
                html.P(id='professor-affiliation'),
                html.Img(id='professor-photo', src='', width=200)
            ], style={"margin-top": "20px"})
        ], style={"width": "33%", "display": "inline-block", "padding": "20px", "border": "1px solid #ccc", "box-shadow": "0 4px 8px 0 rgba(0, 0, 0, 0.2), 0 6px 20px 0 rgba(0, 0, 0, 0.19)", "border-radius": "10px"}),

        # Second widget - delete
        html.Div([
                html.H3("Select a faculty member to delete:", style={"margin-bottom": "20px"}),
                dcc.Dropdown(
                    id="faculty-delete-dropdown",
                    options=[{"label": name, "value": name} for name in professor_names],
                    value='',
                    style={"width": "100%"}
                ),
                html.Button('Delete', id='delete-faculty-button', n_clicks=0),
                html.Div(id='output-container-2')
            ], style={"width": "33%", "display": "inline-block", "padding": "20px", "border": "1px solid #ccc", "box-shadow": "0 4px 8px 0 rgba(0, 0, 0, 0.2), 0 6px 20px 0 rgba(0, 0, 0, 0.19)", "border-radius": "10px"}),

        # Third widget - Add faculty
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

    # Fourth widget - Sample graph
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
    [Output(component_id="professor-name", component_property="children"),
    Output(component_id="professor-position", component_property="children"),
    Output(component_id="professor-interest", component_property="children"),
    Output(component_id="professor-email", component_property="children"),
    Output(component_id="professor-phone", component_property="children"),
    Output(component_id="professor-affiliation", component_property="children"),
    Output(component_id="professor-photo", component_property="src")],
    Input("faculty-dropdown", "value")
)
def update_faculty_details(selected_name):
    if selected_name is None or selected_name == '':
        return dash.no_update
    selected_faculty = get_professor_by_name(selected_name)[0]
    if not selected_faculty:
        return html.P("No faculty member found.")
    return f"Name: {selected_faculty['name']}", \
           f"Position: {selected_faculty['position']}", \
           f"Research Interest: {selected_faculty['researchInterest']}", \
           f"Email: {selected_faculty['email']}", \
           f"Phone: {selected_faculty['phone']}", \
           f"University: {selected_faculty['affiliation']['name']}", \
           selected_faculty['photoUrl']

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

#print(get_professor_by_name('Li,Qun'))
#print(get_top_3_professors_by_citations())
#print(get_top_3_most_cited_publications())
#print(get_all_professors())
#print(get_num_cited_publications_by_year())

#get_top_10_keywords_by_university('University of illinois at Urbana Champaign')
# add_faculty((   
#     92,                  # id: Unique identifier for the faculty member
#     'John Doe',                 # name: Full name of the faculty member
#     'Assistant Professor',      # position: Academic position, such as Assistant Professor, Associate Professor, or Professor
#     'Artificial Intelligence',  # researchInterest: Primary research interest, such as Machine Learning, Computer Vision, or Robotics
#     'john.doe@example.com',     # email: Email address of the faculty member
#     '123-456-7890',             # phone: Phone number of the faculty member
#     'https://example.com/photo_url',  # photoUrl: URL to the faculty member's photo
#     'Machine Learning, Deep Learning',  # keywords: Research keywords associated with the faculty member, separated by commas
#     json.dumps(['Paper 1, Paper 2']),         # publications: List of publications by the faculty member, separated by commas
#     '1',                        # affiliation: Affiliation ID or unique identifier for the affiliated institute
#     'Example University',       # affiliation_name: Name of the affiliated institute or university
#     'https://example.com/affiliation_photo_url'  # affiliation_photoUrl: URL to the affiliated institute's photo or logo
# ))
#remove_faculty('John Doe')
