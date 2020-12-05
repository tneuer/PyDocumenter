#!/home/thomas/anaconda3/bin/python

"""
    # Author : Thomas Neuer (tneuer)
    # File Name : class_diagram_frontend.py
    # Creation Date : Son 21 Okt 2018 00:38:41 CEST
    # Last Modified : Mit 24 Okt 2018 00:31:17 CEST
    # Description : Frontend with Dash for code review. As a tutorial this includes:
        - Enabling and disabling of button (Submit)
        - Dynamic creation of button fields (module-, class- and function buttons)
        - Dynamic Textwindows
        - Drag & Drop file parsing
"""
#==============================================================================

import os
import re
import dash
import time
import shutil
import base64
import datetime

import dash_core_components as dcc
import dash_html_components as html

from textwrap import indent, dedent
from dash.dependencies import Input, Output, State

from documenter_backend import FileParser, MarkdownConverter

# Used later for html column width
NUMBERS = {
    0: 'zero', 1: 'one', 2: 'two', 3: 'three', 4: 'four', 5: 'five',
    6: 'six', 7: 'seven', 8: 'eight', 9: 'nine', 10: 'ten',
    11: 'eleven', 12: 'twelve', 13: 'thirteen', 14: 'fourteen',
    15: 'fifteen', 16: 'sixteen', 17: 'seventeen', 18: 'eighteen',
    19: 'nineteen', 20: 'twenty'
}
RECENTLY_CLICKED_BUTTON = None
PREVIOUS_TABS = []
SWITCH = False

# Dynamic buttons need to be created in the beginning, 12 possible modules, 30 classes and functions per module.
buttons =  ["{}|Module".format(i) for i in range(12)]
buttons += ["{}|Class|{}".format(i, j) for i in range(12) for j in range(30)]
buttons += ["{}|Function|{}".format(i, j) for i in range(12) for j in range(30)]

# Used to bind the dynamical buttons to. They can't be bound to one Output tab, so one needs one output per button.
# These Inputs are not shown to the user but are used to trigger the tab opening process.
tab_triggers = [dcc.Input(id="trigger_"+button, value="deleted") for button in buttons]
NAME_TO_INDEX = {name: i for i, name in enumerate(buttons)}

input_filenames = []
input_filecontents = []

app = dash.Dash("ClassDiagram")

# Allow for dynamic button binding (more error prone)
app.config['suppress_callback_exceptions'] = True

Parser = FileParser()
Converter = MarkdownConverter()

app.layout = html.Div([
    html.Div([
        html.H1("Class diagram",
            style={"textAlign": "center"})
        ]),

    ####
    # Drag and Drop upload
    ####
    dcc.Upload(
            id="upload-files",
            children=html.Div([
                "Drag and Drop or ", html.A("Select Files")
                ]),
            style={
                "width": "50%",
                "height": "60px",
                'lineHeight': '60px',
                'borderWidth': '1px',
                'borderStyle': 'dashed',
                'borderRadius': '5px',
                'textAlign': 'center',
                'marginLeft': "25%",
                'marginBottom': '10px'
                },
            multiple=True
            ),

    ####
    # Dropdown menu for file selection
    ####
    html.Div([
        html.Div(id="dropdown-files", children=dcc.Dropdown(id="DropdownInput"),
            className="ten columns"),

        html.Div(
            html.Button("Submit",
                    id="submit-button",
                    style={
                        "width": "80%",
                        "padding": 0,
                    }),
            className="two columns"
            )
        ],
        className="row"
        ),

    ####
    # Code review blocks, code as text
    ####
    html.Div([
        html.Div([
            html.H6(id="title_of_chosen3", children="Very last added"),
            html.Div(id="content_of_chosen3")
            ],
            style={"marginTop": "30px"},
            className="four columns"),

        html.Div([
            html.H6(id="title_of_chosen2", children="Second last added"),
            html.Div(id="content_of_chosen2")
            ],
            style={"marginTop": "30px"},
            className="four columns"),


        html.Div([
            html.H6(id="title_of_chosen1", children="Third last added"),
            html.Div(id="content_of_chosen1")
            ],
            style={"marginTop": "30px"},
            className="four columns"),
        ], className="row"),

    ####
    # Plotable elements shown
    ####
    html.Div(
            dcc.Dropdown(id="DropdownGraphComponents",
                options=[
                    {"label": "Classes", "value": "CLASSES"},
                    {"label": "Methods", "value": "METHODS"},
                    {"label": "Attributes", "value": "ATTRIBUTES"},
                    {"label": "Functions", "value": "FUNCTIONS"},
                    {"label": "Arguments", "value": "ARGUMENTS"},
                    {"label": "General", "value": "GENERAL"}
                    ],
                value=["CLASSES", "FUNCTIONS", "GENERAL"],
                multi=True),
            style={
                "width": "80%",
                "marginLeft": "10%",
                "marginTop": "50px"
                }
            ),

    ####
    # Actual module summary
    ####
    html.Div(id="ClassDiagram",
            style={
                "marginTop": "100px"
                }),

    ####
    # Needed vor dynamic button binding but no obious reason
    ####
    html.Div(dcc.Graph(id='empty', figure={'data': []}), style={'display': 'none'}),

    ####
    # Tab open and closing menu
    ####
    html.Div(id="dd_chosen_code_div",
             children=dcc.Dropdown(id="dropdown_chosen_blocks",
                                   style={
                                    "width": "95%",
                                    "height": "20px",
                                    'lineHeight': '60px',
                                    'borderWidth': '1px',
                                    'borderRadius': '5px',
                                    'marginLeft': "20px",
                                    'marginBottom': '20px',
                                        })),

    ####
    # Save option and path
    ####
    html.Div(children=[
        html.Div([
            html.Div(children="Save options"),
            dcc.RadioItems(
                id="save_options",
                options=[
                    {'label': 'Save current tab', 'value': 'sct'},
                    {'label': 'Save all ative tabs', 'value': 'saat'},
                    {'label': 'Save all', 'value': 'sa'}
                ],
                value=['sa']
            )],
            className="two columns"
        ),

        html.Div(children=[
            html.Div(children="Path"),
            dcc.Input(id="path_sct", placeholder="Enter path...", value="./"),
            dcc.Input(id="path_saat", placeholder="Enter path...", value="./", disabled=True),
            dcc.Input(id="path_sa", placeholder="Enter path...", value="./", disabled=True),
            ],
            className="two columns"
        ),

        html.Div([
            html.Div(children="File mode"),
            dcc.Checklist(
                id="filemode",
                options=[
                    {'label': 'New .md file', 'value': 'new'},
                    {'label': 'Append to README.md', 'value': 'readme'},
                ],
                values=['new', 'readme'],
                style={
                    "marginTop": "15px",
                }
            )],
            className="two columns"
        )],
        className = "row",
        style={
            "marginTop": "60px",
            "marginLeft": "20px",
            "fontSize": "20px"
        }
    ),

    ####
    # Save buttons for the files
    ####
    html.Div([
        html.Button(id="save_md",
                         children="Save"),
        html.Div(dcc.Textarea(id="save_message", value="Not saved yet", readOnly=True, style={"width": "800px"}))
        ],
        style={
            "marginTop": "20px",
            "marginLeft": "20px"
            }),

    ####
    # Different tabs for clicked buttons
    ####
    html.Div(
            id="tabs-div",
            children=dcc.Tabs(
                id="tabs",
                children=[
                    dcc.Tab(label="Home", value="home")
                    ],
                value="home"
                ),
            style={"marginTop": "40px"}
            ),

    ####
    # Markdown content of the files
    ####
    html.Div(id="tab-content", style={"marginTop": "10px", "width": "90%", "marginLeft": "20px"}),

    ####
    # Not shown but used as trigger to activate a the opening of the tabs
    ####
    html.Div(id="tab-trigger", children=tab_triggers, style={"display": "none"}),

    html.Div(dcc.Input(id="chain1", value="Unused", style={"display": "none"}))
    ],
    style={
        "backgroundColor": "#FFFFFF", #"#b3faff"
        "height": "100%"
        }
    )


####
# Handle Dropdown window and save contents
####
@app.callback(Output("dropdown-files", "children"),
        [Input("upload-files", "contents")],
        [State("upload-files", "filename")]
        )
def update_dropdown(contents, filenames):
    """ Checks input in drag&drop window and adds in to the dropdown.

    Only python files are added to the dropdown menu.
    The important global variables are:
        - input_filenames : list of the module names
        - input_filecontents : list of the actual code content as a string
    To each input file an integer value is assigned as identifier for other functions. This assignment is directly saved
    in the "value" field of the Dropdown menu.

    Parameters
    ----------
    contents : str
        Code content of the file which needs to be decoded and parsed.
    filenames : str
        Module names.

    Returns
    -------
    drpdwn : dcc.Dropdown()
        Updated dropdown menu with input filenames.
    """
    global input_filenames, input_filecontents
    possible_files = []
    if contents is not None:
        for content, filename in zip(contents, filenames):
            if ".py" in filename and filename not in input_filenames:
                input_filenames.append(filename)
                content_type, content_string = content.split(',')
                decoded = base64.b64decode(content_string)
                decoded = decoded.decode("utf-8")
                input_filecontents.append(decoded)

            possible_files = [{"label": f[:-3], "value": i}
                    for i, f in enumerate(input_filenames)]

    drpdwn = dcc.Dropdown(
            id="DropdownInput",
            options=possible_files,
            value = list(range(len(input_filenames))),
            style={
                "width": "98%",
                "height": "20px",
                'lineHeight': '60px',
                'borderWidth': '1px',
                'borderRadius': '5px',
                'marginLeft': "1%",
                'marginBottom': '20px',
                'backgroundColor': "#FFFFFF" #"#90f8ff"
                },
            multi=True)
    return drpdwn

####
# Update text in textwindow 1
####

@app.callback(Output("content_of_chosen1", "children"),
        [Input("DropdownInput", "value")]
        )
def update_text_content1(selected_options):
    """ Update the code revie text block with the code of the last entered file.

    Take the code content of the last entered file and append line numbers. Then print this for the user.

    Parameters
    ----------
    selected_options : list
        List of integer values, each corresponding to a certain file as assigned by the function
        update_dropdown(*args, **kwargs). The last one of those is then chosen and line numbers are inserted.

    Returns
    -------
    textwindow : dcc.Textarea
        Contains the code including the line numbers
    """
    global input_filecontents
    if not selected_options:
        shown_text="No file entered"
    elif len(selected_options)>=1:
        latest_option = selected_options[-1]
        shown_text = input_filecontents[latest_option]
        shown_text = "".join(["{:03d} {}\n".format(i, line) for i, line in enumerate(shown_text.split("\n"))])
    textwindow = dcc.Textarea(
            value=shown_text,
            style={
                "height": "200px",
                "width": "500px",
                'lineHeight': '20px',
                'borderWidth': '1px',
                'marginLeft': '20px',
                'marginRight': '10px',
            }
            )
    return textwindow

@app.callback(Output("title_of_chosen1", "children"),
        [Input("DropdownInput", "value")]
        )
def update_text_header1(selected_options):
    """ Updates the header of the code rewiev block.

    Parameters
    ----------
    selected_options : list
        List of integer values, each corresponding to a certain file as assigned by the function
        update_dropdown(*args, **kwargs). The last one of those is then chosen and line numbers are inserted.

    Returns
    -------
    shown_text : str
        Name of the latest file to be printed as header for the code review field.
    """
    global input_filenames
    if not selected_options:
        shown_text="Very last added"
    elif len(selected_options)>=1:
        latest_option = selected_options[-1]
        shown_text = input_filenames[latest_option]

    return shown_text

####
# Update text in textwindow 2
####

@app.callback(Output("content_of_chosen2", "children"),
        [Input("DropdownInput", "value")]
        )
def update_text_content2(selected_options):
    """ Same as in update_text_content1(*args, **kwargs), but with second last code file.
    """
    global input_filecontents
    if not selected_options or len(selected_options)<2:
        shown_text="No file entered"
    elif len(selected_options)>=2:
        latest_option = selected_options[-2]
        shown_text = input_filecontents[latest_option]
        shown_text = "".join(["{:03d} {}\n".format(i, line) for i, line in enumerate(shown_text.split("\n"))])
    textwindow = dcc.Textarea(
            value=shown_text,
            style={
                "height": "200px",
                "width": "500px",
                'lineHeight': '20px',
                'borderWidth': '1px',
                'marginLeft': '20px',
                'marginRight': '10px',
            }
            )
    return textwindow

@app.callback(Output("title_of_chosen2", "children"),
        [Input("DropdownInput", "value")]
        )
def update_text_header2(selected_options):
    """ As in update_text_header1(*args, **kwargs)
    """
    global input_filenames
    if not selected_options or len(selected_options)<2:
        shown_text="Second last added"
    elif len(selected_options)>=2:
        latest_option = selected_options[-2]
        shown_text = input_filenames[latest_option]

    return shown_text

####
# Update text in textwindow 3
####

@app.callback(Output("content_of_chosen3", "children"),
        [Input("DropdownInput", "value")]
        )
def update_text_content3(selected_options):
    """ Same as in update_text_content1(*args, **kwargs), but with second last code file.
    """
    global input_filecontents
    if not selected_options or len(selected_options)<3:
        shown_text="No file entered"
    elif len(selected_options)>=3:
        latest_option = selected_options[-3]
        shown_text = input_filecontents[latest_option]
        shown_text = "".join(["{:03d} {}\n".format(i, line) for i, line in enumerate(shown_text.split("\n"))])
    textwindow = dcc.Textarea(
            value=shown_text,
            style={
                "height": "200px",
                "width": "500px",
                'lineHeight': '20px',
                'borderWidth': '1px',
                'marginLeft': '20px',
                'marginRight': '10px',
            }
            )
    return textwindow

@app.callback(Output("title_of_chosen3", "children"),
        [Input("DropdownInput", "value")]
        )
def update_text_header3(selected_options):
    """ As in update_text_header1(*args, **kwargs)
    """
    global input_filenames
    if not selected_options or len(selected_options)<3:
        shown_text="Third last added"
    elif len(selected_options)>=3:
        latest_option = selected_options[-3]
        shown_text = input_filenames[latest_option]

    return shown_text

####
# Submit button action
####

@app.callback(Output('submit-button', 'disabled'),
        [Input('DropdownInput', 'value')],
        )
def enable_submit_button(value):
    """ Enables the submit button if files have been added.

    Parameters
    ----------
    value : list
        List of integer values, each corresponding to a certain file as assigned by the function
        update_dropdown(*args, **kwargs).

    Returns
    -------
    bool :
        True if files have been added, else false.
    """
    if value is not None and len(value) == 0:
        return True
    else:
        return False


@app.callback(Output('ClassDiagram', 'children'),
        [Input('submit-button', 'n_clicks'),
        Input('DropdownGraphComponents', 'value')],
        [State('DropdownInput', 'value')]
        )
def draw_class_diagram(n_clicks, drawComponents, inputfiles):
    """ Core functionality which combines most of the other core functions.

    Takes the selected values from the dropdown menu for the module names and converts those into a interactive diagram
    with moduleinformation like lines of code, functions and classes.
    The global variables are:
        - input_filenames : Module names ending with .py
        - buttons : filled with the buttons for the functions and classes later on
        - IDX_TO_NAME : Dictionary of identifier (see trigger_tab_opening(*args)) keys and module, function and classnames as values.

    Parameters
    ----------
    n_clicks : int
        Number of times clicked on the submit button.
    drawComponents : list
        Determines which information is shown. Possibel are:
            - "GENERAL": General information of module like LinesOfCode, LinesOfDocumentation & LinesOfNothing (empty)
            - "CLASSES": Classes of the module are shown
            - "FUNCTIONS": Functions of the module are shown
    inputfiles : list
        List of integer values, each corresponding to a certain file as assigned by the function
        update_dropdown(*args, **kwargs).

    Returns
    -------
    c_diagram : list
        List of html divisions containing the newly created buttons for the modules, functions and classes.

    """
    global input_filenames, buttons, IDX_TO_NAME
    c_diagram = []
    buttons = []
    IDX_TO_NAME = {}
    if n_clicks:
        filepaths = populate_input_folder_with_files(values=inputfiles)
        module_informations = populate_module_information(values=inputfiles, filepaths=filepaths)
        module_buttons = construct_Module_Buttons(inputfiles, module_informations, drawComponents)
        c_diagram.append(module_buttons)

        if "GENERAL" in drawComponents:
            general_elements = construct_general_elements(inputfiles, module_informations)
            c_diagram.append(general_elements)
        if "CLASSES" in drawComponents and "FUNCTIONS" not in drawComponents:
            c_buttons = construct_Buttons(inputfiles, module_informations, key="Class")
            c_diagram.append(c_buttons)
        elif "FUNCTIONS" in drawComponents and "CLASSES" not in drawComponents:
            f_buttons = construct_Buttons(inputfiles, module_informations, key="Function")
            c_diagram.append(f_buttons)
        elif "CLASSES" in drawComponents and "FUNCTIONS" in drawComponents:
            c_and_f_buttons = construct_both(inputfiles, module_informations)
            c_diagram.append(c_and_f_buttons)

        return c_diagram


def populate_input_folder_with_files(values):
    """ Saves the currently used files into a TEMPORARY folder within the working directory.
    The global variables are:
        - input_filenames : Module names ending with .py
        - input_filecontents : list of the actual code content as a string

    Parameters
    ----------
    values : list
        List of integer values, each corresponding to a certain file as assigned by the function
        update_dropdown(*args, **kwargs).

    Returns
    -------
    filepaths : list
        List of strings indicating the filepath to the file content in the TEMPORARY folder.
    """
    global input_filenames, input_filecontents
    save_input_dir = "./InputFiles/"
    if os.path.exists(save_input_dir):
        shutil.rmtree(save_input_dir)
    os.mkdir(save_input_dir)
    filepaths = []
    for value in values:
        filepath = save_input_dir+input_filenames[value]
        with open(filepath, "w") as f:
            f.write(input_filecontents[value])
        filepaths.append(filepath)

    return filepaths


def populate_module_information(values, filepaths):
    """ Interact with the backend, with the parser so to say. Get the information about the parsed code.

    The global variables are:
        - input_filenames : Module names ending with .py

    Parameters
    ----------
    values : list
        List of integer values, each corresponding to a certain file as assigned by the function
        update_dropdown(*args, **kwargs).
    filepaths : list
        List of filepaths to the selected code content in the TEMPORARY folder.

    Returns
    -------
    module_informations : dict
        Dictionary with keys of the module names (e.g. test.py) and the parsed file content. If you are interested in
        the backend and the parsing, see the documentation of class_diagram_backend.py
    """
    global input_filenames, module_informations
    module_informations = {}
    for i, value in enumerate(values):
        curr_module_name = input_filenames[value]
        curr_module_path = filepaths[i]
        module_informations[curr_module_name] = Parser.parse_file(curr_module_path)

    return module_informations


def construct_Module_Buttons(values, module_informations, drawComponents):
    """ Construct the buttons for the module names.

    This will later call the full documentation of the module with all classes and fucntions.
    The global variables are:
        - input_filenames : Module names ending with .py
        - NUMBERS : dictionary ehich translates integer number into word representation (1 -> one,...). Needed for the
        scaling of the 12 possible html columns.
        - IDX_TO_NAME : Dictionary of identifier (see trigger_tab_opening(*args)) keys and module, function and classnames as values.

    Parameters
    ----------
    values : list
        List of integer values, each corresponding to a certain file as assigned by the function
        update_dropdown(*args, **kwargs).
    module_informations : dict
        Output from "populate_module_information(values, filepaths)". Contains all the information about the parsed
        code file content.
    drawComponents : list
        Determines which information is shown. Possibel are:
            - "GENERAL": General information of module like LinesOfCode, LinesOfDocumentation & LinesOfNothing (empty)
            - "CLASSES": Classes of the module are shown
            - "FUNCTIONS": Functions of the module are shown

    Returns
    -------
    module_buttons : html.Div
        HTML division containing all buttons for the module properly scaled, side by side.
    """
    global NUMBERS, input_filenames, IDX_TO_NAME
    nr_modules = len(module_informations.keys())
    columns_per_module = "{} columns".format(NUMBERS[int(12/nr_modules)])
    module_columns = []
    for value in values:
        m = input_filenames[value]
        idx = "{}|Module".format(value)
        module_column = html.Div(
                html.Button(
                    id=idx,
                    children=m,
                    ),
                style={
                    "textAlign": "center"
                },
                className=columns_per_module
                )
        module_columns.append(module_column)
        IDX_TO_NAME[idx] = m

    module_buttons = html.Div(module_columns, className="row")
    return module_buttons


def construct_general_elements(values, module_informations):
    """ Construct the general information about the code file content.

    General information contains:
        - LoC (Lines of Code) : Total number of rows in code file
        - LoD (Lines of Documentaion) : Number of documentation-ONLY columns. This includes multiple line comments as
                                        well as single line comments via "#", but only if no executable code is also
                                        present on the line.
        - LoN (Lines of Nothing) : Empty lines or only white spaces. Also the empty lines within documentations are counted
    The global variables are:
        - input_filenames : Module names ending with .py
        - NUMBERS : dictionary ehich translates integer number into word representation (1 -> one,...). Needed for the
        scaling of the 12 possible html columns.

    Parameters
    ----------
    values : list
        List of integer values, each corresponding to a certain file as assigned by the function
        update_dropdown(*args, **kwargs).
    module_informations : dict
        Output from "populate_module_information(values, filepaths)". Contains all the information about the parsed
        code file content.

    Returns
    -------
    general_elements : html.Div
        HTML division containing all the general information about a module located below the module name.
    """
    global NUMBERS, input_filenames
    nr_modules = len(module_informations.keys())
    columns_per_module = "{} columns".format(NUMBERS[int(12/nr_modules)])
    general_columns = []
    for value in values:
        m = input_filenames[value]
        general_column = html.Div(
                html.Div(
                    id="general{}".format(value),
                    children=str(module_informations[m]["General"]),
                    ),
                style={
                    "textAlign": "center"
                },
                className=columns_per_module
                )
        general_columns.append(general_column)

    general_elements = html.Div(general_columns, className="row")
    return general_elements


def construct_Buttons(values, module_informations, key, mode=None):
    """ Construct the class and function buttons to trigger the tab opening.

    The global variables are:
        - input_filenames : Module names ending with .py
        - NUMBERS : dictionary ehich translates integer number into word representation (1 -> one,...). Needed for the
        scaling of the 12 possible html columns.
        - buttons : List to be filled with the available buttons for modules, classes and functions.
        - IDX_TO_NAME : Dictionary of identifier (see trigger_tab_opening(*args)) keys and module, function and classnames as values.

    Parameters
    ----------
    values : list
        List of integer values, each corresponding to a certain file as assigned by the function
        update_dropdown(*args, **kwargs).
    module_informations : dict
        Output from "populate_module_information(values, filepaths)". Contains all the information about the parsed
        code file content.
    key : "Class" or "Function"
        Indicates if a function header or class header should be used. Also responsible for button binding naming.
    mode : "both" or None [None]
        If "both" only half the width of the module width is used. One half is for class buttons, the other for function buttons.

    Returns
    -------
    buttons : html.Div
        Containing all the class or function buttons used for later interaction.
    """
    global NUMBERS, input_filenames, buttons, IDX_TO_NAME
    nr_modules = len(module_informations.keys())
    columns_per_module = "{} columns".format(NUMBERS[int(12/nr_modules)]) if mode!="both" else "six columns"
    fontsize = "{}".format(18*(1-nr_modules/12))
    columns = []
    use_type = "Classes" if key=="Class" else "Functions"
    header = html.H6(
            children=use_type,
            style={
                "bottomBorder": "1px",
                "textAlign": "center",
                "textDecoration": "underline"
                },
            )
    for value in values:
        m = input_filenames[value]
        buttons_per_module = []
        buttons_per_module.append(header)
        names = list(module_informations[m][use_type].keys())
        if names != []:
            for i, f in enumerate(names):
                idx = "{}|{}|{}".format(value, key, i)
                button = html.Div(html.Button(
                        id=idx,
                        children=f,
                        style={
                            "marginTop": "10px",
                            "marginLeft": "2%",
                            "fontSize": fontsize,
                            "width": "100%",
                            "padding": "0px",
                            }
                        ))
                buttons_per_module.append(button)
                buttons.append(idx)
                IDX_TO_NAME[idx] = f
        else:
            button = html.Div(children="No {} defined".format(key))
            buttons_per_module.append(button)

        column = html.Div(
                buttons_per_module,
                style={
                    "textAlign": "center"
                },
                className=columns_per_module
                )
        if mode == "both":
            return column
        columns.append(column)

    buttons = html.Div(columns, className="row")
    return buttons


def construct_both(values, module_informations):
    """ Construct both class and function buttons to trigger the tab opening.

    Basically a wrapper around construct_buttons twice (once with key="Class", the other with key="Function").
    The global variables are:
        - input_filenames : Module names ending with .py
        - NUMBERS : dictionary ehich translates integer number into word representation (1 -> one,...). Needed for the
        scaling of the 12 possible html columns.

    Parameters
    ----------
    values : list
        List of integer values, each corresponding to a certain file as assigned by the function
        update_dropdown(*args, **kwargs).
    module_informations : dict
        Output from "populate_module_information(values, filepaths)". Contains all the information about the parsed
        code file content.

    Returns
    -------
    class_and_function_buttons : html.Div
        HTML division containing the class and function buttons per module side by side.
    """
    global NUMBERS, input_filenames
    nr_modules = len(module_informations.keys())
    columns_per_module = "{} columns".format(NUMBERS[int(12/nr_modules)])
    fontsize = "{}".format(18*(1-nr_modules/12))
    class_and_function_columns = []
    for value in values:
        m = input_filenames[value]

        function_column = construct_Buttons([value], module_informations, key="Function", mode="both")

        class_column = construct_Buttons([value], module_informations, key="Class", mode="both")

        class_and_function_column = html.Div(
                html.Div(
                    [class_column, function_column],
                    className="row"
                    ),
                className=columns_per_module
                )

        class_and_function_columns.append(class_and_function_column)

    class_and_function_buttons = html.Div(class_and_function_columns, className="row")
    return class_and_function_buttons


for button in buttons:
    @app.callback(Output("trigger_"+button, "value"),
            [Input(button, "n_clicks")],
            [State(button, "id")])
    def trigger_tab_opening(clicks, idx):
        """ Populate the trigger inputs.

        If the trigger inputs are filled with a value, the function open_and_close_tab(*args) is called, due to the change
        in the children property of the trigger. Curiously in this version (06.11.2018) the dcc.Input value that is directed
        to the output. e.g. with this function, is NOT the same as the "value" key when looking at dcc.Input().__dict__.
        This "feature/bug" is used here to mark the newly added buttons as "added". So in this function simultaneously two
        value properties of the dcc.Inputs are set. Once via the callback output und once directly within the function body.
        But these two properties are independent.

        When I tried to let these buttons directly communicate with "tabs"->"children" it did not work, probably because
        the buttons are dynamically created and can't interact with one static output. (06.11.2018)

        Parameters
        ----------
        clicks : int
            Number of clicks on the corresponding module, class or function button. Serves as trigger.
        idx : str
            Identifier of the pressed buttons with the following format "{1}{2}{3}":
                - {1} : Module number in order of input
                - {2} : Either "Module", "Class" or "Function"
                - {3} : Class or function number within the module in order of appearance, does not exist for modules.

        Returns
        -------
        idx : same as parameter input
        """
        global RECENTLY_CLICKED_BUTTON, NAME_TO_INDEX, SWITCH
        RECENTLY_CLICKED_BUTTON = idx
        idx_of_input = NAME_TO_INDEX[idx]
        tab_triggers[idx_of_input].value = "added"
        SWITCH = True

        return idx


@app.callback(Output("dd_chosen_code_div", "children"),
              [Input("trigger_"+button, "value") for button in buttons]+[Input("chain1", "value")])
def open_and_close_tab(*args):
    """ Create a dropdown menu for clicked buttons.

    This dropwdown menu communicates with the tabs divison and tells the tabs div which tabs should currently be
    displayed.
    The global variables are:
        - IDX_TO_NAME : Dictionary of identifier (see trigger_tab_opening(*args)) keys and module, function and classnames as values.

    Parameters
    ----------
    args : list
        List of identifiers of the pressed buttons with the following format "{1}{2}{3}":
                - {1} : Module number in order of input
                - {2} : Either "Module", "Class" or "Function"
                - {3} : Class or function number within the module in order of appearance, does not exist for modules.

    Returns
    -------
    drpdwn : dxx.Dropdown
        Updated dropdown menu for code block inspection. The ones which are deleted are set to None again by the function
        switch_Tab_on_click().

    """
    global IDX_TO_NAME, PREVIOUS_TABS

    args = [arg for arg, trigger in zip(args, tab_triggers) if trigger.value == "added"]
    PREVIOUS_TABS = args
    args = [{"label": IDX_TO_NAME[arg], "value": arg} for arg in args  if arg in IDX_TO_NAME]
    values = [tab["value"] for tab in args]

    drpdwn = dcc.Dropdown(
            id="dropdown_chosen_blocks",
            options = args,
            value = values,
            style={
                "width": "95%",
                "height": "20px",
                'lineHeight': '60px',
                'borderWidth': '1px',
                'borderRadius': '5px',
                'marginLeft': "20px",
                'marginBottom': '20px',
                },
            multi=True)

    return drpdwn


@app.callback(Output("tabs", "children"),
              [Input("dropdown_chosen_blocks", "value")])
def open_and_delete_tab(available_tabs):
    """ Opens and closes tabs.

    The global variables are:
        - IDX_TO_NAME : Dictionary of identifier (see trigger_tab_opening(*args)) keys and module, function and classnames as values.
        - TABDICT : dictonary of all tabs where the identifiers are the keys and the tabs are the values.
        - PREVIOUS_TABS : The tabs previously selected. Used for filtering out the deleted tabs.

    Parameters
    ----------
    available_tabs : list
        List of identifiers of the pressed buttons with the following format "{1}{2}{3}":
                - {1} : Module number in order of input
                - {2} : Either "Module", "Class" or "Function"
                - {3} : Class or function number within the module in order of appearance, does not exist for modules.

    Returns
    -------
    tabs : list
        List of tabs available for selection

    """
    global IDX_TO_NAME, TABDICT, PREVIOUS_TABS
    for tab in PREVIOUS_TABS:
        if tab not in available_tabs:
            idx = NAME_TO_INDEX[tab]
            tab_triggers[idx].value = "deleted"

    if available_tabs is not None:
        TABDICT = {arg: dcc.Tab(label=IDX_TO_NAME[arg], value=arg) for arg in available_tabs}
    else:
        TABDICT = {}

    TABDICT["home"] = dcc.Tab(label="Home", value="home")
    tabs = list(TABDICT.values())[::-1]

    return tabs


@app.callback(Output("tabs", "value"),
              [Input("dropdown_chosen_blocks", "value")],
              [State("tabs", "value")])
def switch_Tab_on_click(available_tabs, currently_selected_tab):
    """ Deals with tab switching and updating.

    If a new ta is opened, this one should be visible to the user.
    If the current visible tab is closed, the home tab is headed for.
    If some tab is closed the system should remain in the current position.

    Parameters
    ----------
    available_tabs : list
        List of identifiers of the pressed buttons with the following format "{1}{2}{3}":
            - {1} : Module number in order of input
            - {2} : Either "Module", "Class" or "Function"
            - {3} : Class or function number within the module in order of appearance, does not exist for modules.
    currently_selected_tab : str
        Identifier of currently open tab

    Returns
    -------
    go_to_tab : str
        Identifier to the next tab
    """
    global RECENTLY_CLICKED_BUTTON, SWITCH

    if SWITCH:
        go_to_tab = RECENTLY_CLICKED_BUTTON
        SWITCH = False
    else:
        go_to_tab = currently_selected_tab

    if currently_selected_tab != "home" and currently_selected_tab not in available_tabs:
        go_to_tab = "home"

    return go_to_tab


@app.callback(Output("chain1", "value"),
              [Input("submit-button", "n_clicks")])
def wait_for_module_information(clicks):
    time.sleep(1.5)
    return "Unused"


@app.callback(Output("tab-content", "children"),
              [Input("tabs", "value"), Input("chain1", "value")])
def display_information(tab, unused_trigger):
    """ Get the necessary information for the clicked block from the backend.

    The global variables are:
        - IDX_TO_NAME : Dictionary of identifier (see trigger_tab_opening(*args)) keys and module, function and classnames as values.

    Parameters
    ----------
    tab : str
        Identifier for the selected method.
        tab[0] := module number
        tab[1:-1] := "Module", "Class" or "Function"
        tab[-1] := Class or function number

    Returns
    -------
    tab_content : dcc.Markdown
        Markdown environment containing the information about the selected tab.
    """
    global IDX_TO_NAME, module_informations

    if tab == "home":
        all_identifiers = [idx for idx in list(IDX_TO_NAME.keys()) if "Module" in idx]
        tab_mds = []
        fnames = []
        types = ["Module"] * len(all_identifiers)
        for idx in all_identifiers:
            fname, tab_md = get_md_from_ID(idx)
            tab_mds.append(tab_md + "\n\n\n")
            fnames.append(IDX_TO_NAME[idx])

        tab_mds = Converter.mash_markdown_files(tab_mds, fnames, types)
        tab_mds = indent(tab_mds, "    ")
        markdown = dcc.Markdown(tab_mds)

        return markdown

    source_module = "{}Module".format(re.search("[0-9]+\|", tab).group(0))
    source_module = IDX_TO_NAME[source_module]

    mode = re.search("\|[a-zA-Z]\w+\|*", tab).group(0)[1:-1]
    if mode != "Modul":
        name = IDX_TO_NAME[tab]
    else:
        mode = "Module"
        name = ""

    tab_md = Converter.convert_to_md(parsed_file=module_informations[source_module], mode=mode, name=name)
    tab_md = indent(tab_md, "    ")
    markdown=dcc.Markdown(tab_md)

    return markdown


@app.callback(Output("path_sct", "disabled"),
              [Input("save_options", "value")])
def enable_path_entry_sct(value):
    if "sct" == value:
        return False
    else:
        return True
@app.callback(Output("path_saat", "disabled"),
              [Input("save_options", "value")])
def enable_path_entry_saat(value):
    if "saat" == value:
        return False
    else:
        return True
@app.callback(Output("path_sa", "disabled"),
              [Input("save_options", "value")])
def enable_path_entry_sa(value):
    if "sa" == value:
        return False
    else:
        return True


@app.callback(Output("save_message", "value"),
              [Input("save_md", "n_clicks")],
              [State("save_options", "value"), State("filemode", "values"),
               State("path_sct", "value"), State("path_saat", "value"), State("path_sa", "value"),
               State("tabs", "value"), State("tabs", "children")])
def save_md_files(clicks, option, fmode, path_curr, path_active, path_all, tab_curr, tab_active):
    """

    Parameters
    ----------
    clicks : int
        Number of clicks on the save button. Serves as trigger for saving.
    options : list
        Corresponds to the save options:
            - sct : save current tab
            - saat : save all active tabs
            - sa : save all tabs
    fmode : list
        Can be "readme", "new" or both. Determines if appended to a README.md file in the current folder path or a new
        .md file is created. If README.md does not exits it is created.
    path_curr : str
        Path where the currently open tab should be saved if options contains "sct".
    path_active : str
        Path where all the active tabs should be saved if options contains "saat".
    path_all : str
        Path where all module should be saved if options contains "sa".
    tab_curr : str
        Identifier of the currently selected tab.
    tab_active : list
        List of tab objects containing among other things the identifier of the module, class or function

    Returns
    -------
    exitcode : str
        Confim message if all files could be saved, else explanatory merror message.
    """
    if clicks is None:
        return "Nothing done yet"

    exitcodes = ""
    saved_paths = ""
    # Save the ccurrent tab, only the displayed tab.
    if "sct" == option:
        if tab_curr != "home":
            fname, tab_md = get_md_from_ID(tab_curr)

            if "new" in fmode:
                exitcode, savepath = create_new_md_file(path_curr, tab_md, fname)
                exitcodes += exitcode
                saved_paths += savepath

            if "readme" in fmode:
                exitcode, savepath = append_to_readme_md(path_curr, tab_md)
                exitcodes += exitcode
                saved_paths += savepath
        else:
            option = "sa"
            path_all = "".join(re.findall("(.*/)+", path_curr))

    # Save all active tabs, except for the home tab.
    if "saat" == option:
        active_tabs = [tab["props"]["value"] for tab in tab_active]
        tab_mds = []
        fnames = []
        types = []
        for tab in active_tabs:
            if tab != "home":
                fname, tab_md = get_md_from_ID(tab)
                tab_mds.append(tab_md + "\n\n\n")
                fnames.append(IDX_TO_NAME[tab])

                typ = re.search("\|[a-zA-Z]\w+\|*", tab).group(0)[1:-1]
                if typ == "Modul":
                    typ += "e"
                types.append(typ)

                if "new" in fmode:
                    exitcode, savepath = create_new_md_file(path_active, tab_md, fname)
                    exitcodes += exitcode
                    saved_paths += savepath

        tab_mds = Converter.mash_markdown_files(tab_mds, fnames, types)
        if "readme" in fmode:
            exitcode, savepath = append_to_readme_md(path_active, tab_mds)
            exitcodes += exitcode
            saved_paths += savepath

    # Save all module included in the diagram
    if "sa" == option:
        all_identifiers = [idx for idx in list(IDX_TO_NAME.keys()) if "Module" in idx]
        tab_mds = []
        fnames = []
        types = ["Module"] * len(all_identifiers)
        for idx in all_identifiers:
            fname, tab_md = get_md_from_ID(idx)
            tab_mds.append(tab_md + "\n\n\n")
            fnames.append(IDX_TO_NAME[idx])

            if "new" in fmode:
                exitcode, savepath = create_new_md_file(path_all, tab_md, fname)
                exitcodes += exitcode
                saved_paths += savepath

        tab_mds = Converter.mash_markdown_files(tab_mds, fnames, types)
        if "readme" in fmode:
            exitcode, savepath = append_to_readme_md(path_active, tab_mds)
            exitcodes += exitcode
            saved_paths += savepath

    ret_message = exitcodes+saved_paths
    if ret_message == "":
        ret_message = "No save option chosen"
    else:
        ret_message = ret_message.strip()

    return ret_message


def get_md_from_ID(idx):
    """ Get the markdown text and function name from the identifier.

    Interacts with the MarkdownConverter of the backend.

    Parameters
    ----------
    idx : str
        Identifier of the module, class or function with the following form:
            idx[0] := module number
            idx[1:-1] := "Module", "Class" or "Function"
            idx[-1] := Class or function number

    Returns
    -------
    fname : str
        Name of the module, class or function. Only used if the filepath is a directory.
    tab_md : str
        String of the markdown description of the module, class or function

    """
    global IDX_TO_NAME

    source_module = "{}Module".format(re.search("[0-9]+\|", idx).group(0))
    source_module = IDX_TO_NAME[source_module]

    mode = re.search("\|[a-zA-Z]\w+\|*", idx).group(0)[1:-1]
    if mode != "Modul":
        name = IDX_TO_NAME[idx]
        fname = mode + "_" + name
    else:
        mode = "Module"
        name = ""
        fname = mode + "_" + source_module

    tab_md = Converter.convert_to_md(parsed_file=module_informations[source_module], mode=mode, name=name)

    return fname, tab_md


def create_new_md_file(path, md_text, fname):
    """ Create the new .md file and deal with false user input.

    If the path is a directory a descriptive name is chosen, e.g for a class:
            Class_*classname*_*currentDate.
    If the given path leads into a directory but with a filename, then this name is given to the class and if needed, a
    .md extension is attached.

    Parameters
    ----------
    path :  str
        Directory or full path with filename. If it is a directory a generic name for the markdown text is given.
    md_text : str
        Description in markdown format
    fname : str
        Name of the module, class or function

    Returns
    -------
    exitcode : str
        If all good empty string "" is returned, else a descriptive errormessage is returned.
    """
    try:
        with open(path, "w") as f:
            if ".md" not in path:
                add_md = True
            else:
                add_md = False
        os.remove(path)
        if add_md:
            path += ".md"
        with open(path, "w") as f:
            f.write(md_text)

        exitcode = ""
    except FileNotFoundError:
        exitcode = "{} path does not exist.".format(path)
    except IsADirectoryError:
        now = datetime.datetime.now().strftime("%Y_%m_%d_%H_%M")
        path += fname + "_" + now + ".md"
        path = path.replace(".py", "")
        try:
            with open(path, "w") as f:
                f.write(md_text)
                exitcode = ""
        except FileNotFoundError:
            exitcode = "{} path does not exist.".format(path)

    return exitcode+"\n", path+"\n"


def append_to_readme_md(path, md_text):
    """ Append description to README.md file.

    The longest possible path to a directiory is selected from the path. There the description of the file is attached
    to the README.md or a new one is created.

    Parameters
    ----------
    path :  str
        Directory or full path with filename. If it is a directory a generic name for the markdown text is given.
    md_text : str
        Description in markdown format

    Returns
    -------
    exitcode : str
        If all good empty string "" is returned, else a descriptive errormessage is returned.
    """
    path = "".join(re.findall("(.*/)+", path)) + "README.md"
    try:
        with open(path, "a") as f:
            f.write(md_text)
        exitcode = ""
    except FileNotFoundError:
        exitcode = "\n{} not a path for README.md".format(path)

    return exitcode+"\n", path+"\n"



external_css = [
        'https://codepen.io/chriddyp/pen/bWLwgP.css',
        ]
for css in external_css:
    app.css.append_css({"external_url": css})

external_js = ['https://cdnjs.cloudflare.com/ajax/libs/materialize/0.100.2/js/materialize.min.js']
for js in external_css:
    app.scripts.append_script({'external_url': js})


if __name__ == "__main__":
    app.server.run(debug=True)

    save_input_dir = "./InputFiles/"
    if os.path.exists(save_input_dir):
        shutil.rmtree(save_input_dir)
