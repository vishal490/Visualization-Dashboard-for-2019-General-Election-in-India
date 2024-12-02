## Load Libraries

import dash
import numpy as np
import pandas as pd
from dash import dcc, html
import plotly.express as px
import plotly.graph_objs as go
from dash.dependencies import Input, Output

## Load Util Code base
from Utils.Sabari.util_functions import party_stats_process, sample_dummy_processing, get_state_updated_plots_party_stats, process_cols, sample_seats_won_state_wise, sample_state_constituencies_count

from Utils.Shubham.util_functions_shubham import IndiaMap,bar_graph,Update_Bar_Graph,constituency_level_graph,NOTA_VIZ_Constituency,criminal_cases_constituency_wise,criminal_cases_india_wise

from Utils.Hemang.ab import get_pcp_default,get_pcp_state

## Read the dataset
dataset = pd.read_csv("modified_dataset.csv")
dataset.head(1)

# Execute the Processing for individual modules
## Sample Analytics
sample_dummy_processing(dataset)

# process data for radar chart
# Define age groups
age_groups = {
    '25-34': (25, 34),
    '35-44': (35, 44),
    '45-54': (45, 54),
    '55-64': (55, 64),
    '65-74': (65, 74),
    '75+': (75, float('inf'))
}

# Group ages into the specified categories
def group_age(age):
    for group, (lower, upper) in age_groups.items():
        if lower <= age <= upper:
            return group

# Apply the function to create a new column for age groups
dataset['Age_Group'] = dataset['AGE'].apply(group_age)


# process data for education pie-chart
# Remove entries with "Not Available" and "Literate" from the dataset
filtered_df = dataset[(dataset['EDUCATION'] != 'Not Available') & (dataset['EDUCATION'] != 'Literate')]
# Merge "10th Pass" and "8th Pass" entries into a single category
filtered_df['EDUCATION'] = filtered_df['EDUCATION'].replace({'8th Pass': '8th/5th Pass', '5th Pass': '8th/5th Pass'})

## Party Specific Analytics
party_stats_process(dataset)

party_bar_graph = bar_graph(dataset)
graph_bar_graph_ss = IndiaMap(dataset)
graph_constituency_map_ss = constituency_level_graph(dataset)


graph_NOTA_constituency_map_ss = NOTA_VIZ_Constituency(dataset)
graph_Criminal_constituency_map_ss = criminal_cases_constituency_wise(dataset)
graph_Criminal_india_map_ss = criminal_cases_india_wise(dataset)


## DASH Integration
app = dash.Dash(__name__, prevent_initial_callbacks='initial_duplicate')
common_style = {'box-sizing': 'border-box','border': '1px solid Violet','margin': '0','padding': '0','width': '50%', 'display': 'inline-block'}

common_style_pcp = {'box-sizing': 'border-box','border': '1px solid Violet','margin': '0','padding': '0','width': '100%', 'display': 'inline-block'}

app.layout = html.Div([
    html.H1(children='Indian Election 2019', style={'margin': '0', 
                                                    'padding': '0',
                                                    'text-align': 'center',
                                                    'background-color': '#303030', 
                                                    'color': '#FFFFFF',
                                                    'border': '1px solid Violet',
                                                    'box-sizing': 'border-box'}),
    html.Div([
        html.Div([
                dcc.Graph(id='graph_india_map_ss',figure=graph_bar_graph_ss, style=common_style),
                dcc.Graph(id='party_bar_graph1',figure=party_bar_graph, style=common_style)
            ])
    ]),
    html.Div([
        dcc.Graph(id='education-pie-chart', style=common_style),
        dcc.Graph(id='radar-chart', style=common_style)
    ]),
     html.Div([
          dcc.Graph(id='pcp_state',figure=get_pcp_default(), style=common_style_pcp)
     ]),
    html.Div([
        html.Div([
            html.Div([
                    dcc.Dropdown(
                        id='attribute-dropdown',
                        options=[{'label': col, 'value': col} for col in process_cols],
                        value="GENDER",
                    ),
                    dcc.Graph(id='graph11', figure=get_state_updated_plots_party_stats(None)["GENDER"]),
            ], style=common_style
            ),
        html.Div([
            dcc.Dropdown(
                id='zone-dropdown',
                options=[{'label': zone, 'value': zone} for zone in dataset.Zone.unique()],
                value=dataset.Zone.unique()[0] , # Default value
            ),
            dcc.Graph(id='bar-chart')
        ], style=common_style),
        ]),
    ]),
    html.Div([
            html.Div([
            dcc.Dropdown(
                id='constituency_graph_selection_dropdown',
                options=[{'label': col, 'value': col} for col in ["PARTY", "NOTA", "Criminal Cases"]],
                value="PARTY",
            ),
            dcc.Graph(id='graph_constituency_based', figure=graph_constituency_map_ss),
        ], style=common_style),
        # html.Div([
            dcc.Graph(id='graph_Criminal_india_map_ss',figure=graph_Criminal_india_map_ss, style=common_style)
    # ])
    ]),
    # html.Div([
    #     html.Div(id='state-info')
    # ])
])


## Callbacks for each of the Drop downs
curr_attr_global = "GENDER"

@app.callback(
    [
        Output('graph11', 'figure', allow_duplicate=True), 
        Output('party_bar_graph1', 'figure', allow_duplicate=True), 
        Output('pcp_state', 'figure', allow_duplicate=True)
    ],
    
        [Input('graph_india_map_ss', 'clickData')],
    prevent_initial_call=True
)

def update_graph_state_selection(clickData):
#     print("State")
    # Get the sample 0 plot
    if clickData is not None:
        selected_column = clickData['points'][0]['hovertext']
#     print(selected_column)
    # seats_won_fig = sample_seats_won_state_wise(selected_column)
    # seats_count_fig = sample_state_constituencies_count()
    
    state_filtered = get_state_updated_plots_party_stats(selected_column)
    state_bar_graph = Update_Bar_Graph(selected_column)
    pcp_plot = get_pcp_state(selected_column)
    
    # if curr_attr is None:
    #     attr_plot = [list(state_filtered.values())[0]]
    # else:
    attr_plot = state_filtered[curr_attr_global]
    # return [seats_count_fig, seats_won_fig] + 
    # return list(state_filtered.values()) + 
    return [attr_plot, state_bar_graph, pcp_plot]

 # Define callback to update graphs = attribute
@app.callback(
    [Output('graph11', 'figure')],
    [Input('graph_india_map_ss', 'clickData'), Input('attribute-dropdown', 'value')],prevent_initial_call=True
)

def update_graph_attribute_selection(clickData, attribute):
#     print(curr_state, "Attr")
    curr_state = clickData
    global curr_attr_global
    curr_attr_global = attribute
    
    if clickData is not None:
        curr_state = clickData['points'][0]['hovertext']
    state_filtered = get_state_updated_plots_party_stats(curr_state)
    if curr_attr_global is None:
        return [list(state_filtered.values())[0]]
    return [state_filtered[curr_attr_global]]

# def update_graph_attribute_selection(curr_state, attribute):
# #     print(curr_state, "Attr")
#     if clickData is not None:
#         curr_state = clickData['points'][0]['hovertext']
#     state_filtered = get_state_updated_plots_party_stats(curr_state)
#     if attribute is None:
#         return [list(state_filtered.values())[0]]
#     return [state_filtered[attribute]]



# @app.callback(
#     Output('state-info', 'children'),
#     [Input('graph_india_map_ss', 'clickData')]
# )
# def update_state_info(clickData):
#     if clickData is not None:
#         selected_state = clickData['points'][0]['hovertext']
#         print(selected_state)
#         return [html.H2(f'Selected State: {selected_state}')]
#     else:
#         # If no region is clicked, display a default message or leave it empty
#         return [html.Div('Click on a state to see details')]
    
# Constituency based graph selection
@app.callback(
    [Output('graph_constituency_based', 'figure')],
    [Input('constituency_graph_selection_dropdown', 'value')],prevent_initial_call=True
)

def update_graph_attribute_selection(graph_req):
    graph_maps = {"PARTY":graph_constituency_map_ss, "NOTA":graph_NOTA_constituency_map_ss, "Criminal Cases":graph_Criminal_constituency_map_ss}
    # print(graph_maps[graph_req])
    return [graph_maps[graph_req]]
# Run the app



@app.callback(
    Output('education-pie-chart', 'figure'),
    [Input('graph_india_map_ss', 'clickData')]
)
def update_pie_chart(clickData):
    if clickData is not None:
        selected_state = clickData['points'][0]['hovertext']
        state_filtered_df = filtered_df[filtered_df['STATE'] == selected_state]
        education_counts = state_filtered_df['EDUCATION'].value_counts()
        title = f'Education Distribution in {selected_state}'
    else:
        education_counts = filtered_df['EDUCATION'].value_counts()
        title = 'Education Distribution (All States)'

    fig = px.pie(education_counts, values=education_counts.values, names=education_counts.index, title=title)
    return fig

@app.callback(
    Output('radar-chart', 'figure'),
    [Input('graph_india_map_ss', 'clickData')]
)
def update_radar_chart(clickData):
    if clickData is not None:
        state = clickData['points'][0]['hovertext']
    else:
        state = "All India"
    
    try:
        if state == 'All India':
            filtered_df = dataset
            title = "Average Asset Holding Percentage (All India)"
        else:
            filtered_df = dataset[dataset['STATE'] == state]
            title = f"Average Asset Holding Percentage in {state}"

        if filtered_df.empty:
            raise ValueError(f"No data available for the selected state: {state}")

        # Separate asset holdings by gender
        male_df = filtered_df[filtered_df['GENDER'] == 'MALE']
        female_df = filtered_df[filtered_df['GENDER'] == 'FEMALE']

        # Aggregate data by age group for each gender
        male_asset_by_age_group = male_df.groupby('Age_Group')['ASSETS'].sum()
        female_asset_by_age_group = female_df.groupby('Age_Group')['ASSETS'].sum()

        # Calculate total assets for each gender
        total_male_assets = male_asset_by_age_group.sum()
        total_female_assets = female_asset_by_age_group.sum()

        # Calculate the percentage of assets for each gender and age group
        male_asset_percentage_by_age_group = (male_asset_by_age_group / total_male_assets) * 100
        female_asset_percentage_by_age_group = (female_asset_by_age_group / total_female_assets) * 100

        # Define categories (age groups)
        categories_male = male_asset_percentage_by_age_group.index
        categories_female = female_asset_percentage_by_age_group.index
        # Create radar charts for male and female
        fig = go.Figure()

        # Add trace for male
        fig.add_trace(
            go.Scatterpolar(
                r=male_asset_percentage_by_age_group.values,
                theta=categories_male,
                fill='toself',
                fillcolor='rgba(31, 119, 180, 0.5)',  # Light blue for male
                name='Male'
            )
        )

        # Add trace for female
        fig.add_trace(
            go.Scatterpolar(
                r=female_asset_percentage_by_age_group.values,
                theta=categories_female,
                fill='toself',
                fillcolor='rgba(255, 127, 14, 0.5)',  # Light orange for female
                name='Female'
            )
        )

        # Update layout
        fig.update_layout(
            polar=dict(
                radialaxis=dict(
                    visible=True,
                    range=[0, 100],  # Set range for radial axis (percentage)
                    tickvals=[i * 10 for i in range(11)],  # Set tick values for radial axis (0%, 10%, 20%, ..., 100%)
                    ticktext=[f"{i * 10}%" for i in range(11)],  # Set tick labels for radial axis
                )
            ),
            title=title,
            # width=800,  # Adjust width of the figure
            # height=600,  # Adjust height of the figure
            # margin=dict(l=50, r=50, t=50, b=50)  # Adjust margins
        )

        return fig
    except Exception as e:
        print("Error:", e)
        return go.Figure()

@app.callback(
    Output('bar-chart', 'figure'),
    [Input('zone-dropdown', 'value')]
)
def update_bar_chart(selected_zone):
    # Filter dataset based on selected zone
    filtered_data = dataset[dataset['Zone'] == selected_zone]
    
    # Group by state and zone, and calculate sum of total votes and total electors
    grouped = filtered_data.groupby(['STATE', 'Zone', 'CONSTITUENCY']).agg({'TOTAL_VOTES': 'sum', 'TOTAL_ELECTORS': 'first'}).reset_index()
    grouped_state = grouped.groupby(['STATE', 'Zone']).agg({'TOTAL_VOTES': 'sum', 'TOTAL_ELECTORS': 'sum'}).reset_index()

    # Calculate percentage of total votes for each state
    grouped_state['PERCENTAGE_TOTAL_VOTES'] = (grouped_state['TOTAL_VOTES'] / grouped_state['TOTAL_ELECTORS'])*100

    fig = px.bar(
        grouped_state[grouped_state['Zone'] == selected_zone],
        x='STATE',
        y='PERCENTAGE_TOTAL_VOTES',
        title=f'Total Percentage of Voters by State in {selected_zone} Zone',
        labels={'STATE': 'State', 'PERCENTAGE_TOTAL_VOTES': 'Percentage of Voters'}
    )

    fig.update_layout(xaxis_title='State', yaxis_title='Percentage of Voters', yaxis_range=[0, 100])
    return fig

if __name__ == '__main__':
    app.run_server(debug=False, port=8088)