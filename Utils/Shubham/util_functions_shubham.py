import numpy as np
import pandas as pd
import plotly.express as px
import plotly.graph_objs as go
import json
import os

###################################################################
#Functions for Chlorepleth Maps

bar_graph_df = None
def bar_graph(df):
    global bar_graph_df
    bar_graph_df = df
    
    wins_by_party = df.groupby('PARTY')['WINNER'].sum().reset_index()
    wins_by_party = wins_by_party.sort_values(by='WINNER', ascending=False)
    top_ten_parties = wins_by_party.head(10)
    fig_2 = px.bar(top_ten_parties, 
             x='PARTY', 
             y='WINNER',
             # color='WINNER',
             title=f"INDIA : Constituencies Won per Party",
             color_continuous_scale='Viridis')
    # fig_2.update_layout(
    # xaxis=dict(title='Party', tickmode='linear'),
    # yaxis=dict(title='Wins'),
    # # title_font=dict(size=20),
    # font=dict(size=14), #,color='#FFFFFF'),#{'color': '#FFFFFF','size':'14'},
    # # paper_bgcolor ='#303030',
    # # plot_bgcolor = '#303030',
    # # margin=dict(l=0, r=0, t=0, b=0),  # Set margins to zero
    # autosize=True,
    # )
    return fig_2
def IndiaMap(dataset):
    df = dataset
    current_directory = os.path.dirname(__file__)
    geojson_filename = "states_india.geojson"
    geojson_filepath = os.path.join(current_directory, geojson_filename)
    india_states = json.load(open(geojson_filepath, "r"))
    state_id_map = {}
    for feature in india_states["features"]:
        feature["id"] = feature["properties"]["state_code"]
        state_id_map[feature["properties"]["st_nm"].lower()] = feature["id"]
    distinct_constituencies = df.groupby('STATE')['CONSTITUENCY'].nunique().reset_index()
    States_List = []
    Constituency_List = []
    for i in distinct_constituencies['STATE']:
        States_List.append(i)
    for i in distinct_constituencies['CONSTITUENCY']:
        Constituency_List.append(i)
    for i in range(len(States_List)):
        if States_List[i] == 'ANDAMAN & NICOBAR ISLANDS':
            States_List[i] = 'ANDAMAN & NICOBAR ISLAND'
        if States_List[i] == 'ARUNACHAL PRADESH':
            States_List[i] = 'ARUNANCHAL PRADESH'
        if States_List[i] == 'DADRA & NAGAR HAVELI':
            States_List[i] = 'DADARA & NAGAR HAVELLI'
    data = {
            "State": States_List,
            "Constituency": Constituency_List,
            "State_Names": States_List
    }
    df_new = pd.DataFrame(data)
    df_new['State'] = df_new['State'].str.lower()
    df_new["id"] = df_new["State"].apply(lambda x: state_id_map[x])
    df_new["SeatScale"] = np.log10(df_new["Constituency"])

    wins_by_party = df.groupby('PARTY')['WINNER'].sum().reset_index()
    wins_by_party = wins_by_party.sort_values(by='WINNER', ascending=False)
    top_ten_parties = wins_by_party.head(10)
#     print(df_new.head(5))

    custom_colors = ["#FF0000", "#FF7F00", "#FFFF00", "#7FFF00", "#00FF00"]
    fig_1 = px.choropleth_mapbox(
        df_new,
        locations="id",
        geojson=india_states,
        color="Constituency",
        hover_name="State_Names",
        hover_data=["Constituency"],
        color_continuous_scale="Viridis",  
        color_continuous_midpoint=df_new['Constituency'].median(),
        range_color=(df_new['Constituency'].min(), df_new['Constituency'].max()),
        mapbox_style="carto-positron",
        zoom = 3,
        opacity = 0.5,
        center = {"lat": 22, "lon": 77},
    )

    fig_1.update_layout(margin={"r":0,"t":0,"l":0,"b":0})
    return fig_1
#     fig_1 = px.choropleth(
#         df_new,
#         locations="id",
#         geojson=india_states,
#         color="Constituency",
#         hover_name="State_Names",
#         hover_data=["Constituency"],
# #     title="India Constituency Seats",
#         color_continuous_scale=custom_colors,  
#         color_continuous_midpoint=df_new['Constituency'].median(),
#         range_color=(df_new['Constituency'].min(), df_new['Constituency'].max())
#     )
#     fig_1.update_layout(coloraxis_colorbar_title="Constituency", coloraxis_cmin=df_new['Constituency'].min(),      coloraxis_cmax=df_new['Constituency'].max(),
#                    font=dict(size=14,color='#FFFFFF'),
#                     paper_bgcolor ='#303030',
#                     plot_bgcolor = '#303030',
# #                     margin=dict(l=0, r=0, t=0, b=0),  # Set margins to zero
# #                     autosize=True,
#                        )
#     fig_1.update_traces(hovertemplate="<br>".join([
#     "State: %{hovertext}",
#     "Constituency: %{customdata[0]}"
#     ]))
#     fig_1.update_geos(fitbounds="locations", visible=False)
#     fig_1.show()
#     fig_2 = px.bar(top_ten_parties, 
#              x='PARTY', 
#              y='WINNER',
#              color='WINNER',
#              color_continuous_scale='Viridis')
#     fig_2.update_layout(
#     xaxis=dict(title='Party', tickmode='linear'),
#     yaxis=dict(title='Wins'),
#     title_font=dict(size=20),
#     font=dict(size=14,color='#FFFFFF'),#{'color': '#FFFFFF','size':'14'},
#     paper_bgcolor ='#303030',
#     plot_bgcolor = '#303030',
#     margin=dict(l=0, r=0, t=0, b=0),  # Set margins to zero
#     autosize=True,
#     )
    return fig_1
def constituency_level_graph(df):
    current_directory = os.path.dirname(__file__)
    geojson_filename = "india_pc_2019_simplified.geojson"
    geojson_filepath = os.path.join(current_directory, geojson_filename)
    with open(geojson_filepath, "r", encoding="utf-8") as file:
        india_constituency = json.load(file)
    constituency_id_map = {}
    for feature in india_constituency["features"]:
        feature["id"] = feature["properties"]["pc_id"]
        constituency_id_map[feature["properties"]["pc_name"].lower()] = feature["id"]
    constituency_id_map = {key.lower(): int(value) for key, value in constituency_id_map.items()}
    df_winner_1 = df[df['WINNER'] == 1]
    new_df = df_winner_1[['STATE', 'CONSTITUENCY', 'PARTY']]
    # new_df["id"] = new_df["CONSTITUENCY"].apply(get_id)
    new_dict={}
    for i in new_df["CONSTITUENCY"]:
        if i.lower() not in constituency_id_map:
            new_dict[i.lower()] = -1
        else:
            new_dict[i.lower()] = constituency_id_map[i.lower()]
    new_df['CONSTITUENCY'] = new_df['CONSTITUENCY'].str.lower()
    new_df['ID'] = new_df['CONSTITUENCY'].map(new_dict)
    new_df = new_df[new_df['ID'] != -1]
    fig_1 = px.choropleth_mapbox(
        new_df,
        locations="ID",
        geojson=india_constituency,
        mapbox_style="carto-positron",
        color="PARTY",
            color_discrete_map={
        'BJP': '#F97D09',   
        'INC': '#003E7E',  
        
    },
        hover_data={"PARTY": True},
        labels={'PARTY': 'Party'}
    )
    fig_1 = px.choropleth_mapbox(
        new_df,
        locations="ID",
        geojson=india_constituency,
        color="PARTY",
            color_discrete_map={
        'BJP': '#F97D09',   
        'INC': '#003E7E',  
        
    },
        hover_data={"PARTY": True},
        labels={'PARTY': 'Party'},
        mapbox_style="carto-positron",
        zoom = 3,
        opacity = 0.5,
        center = {"lat": 22, "lon": 77},
    )

    fig_1.update_layout(margin={"r":0,"t":0,"l":0,"b":0})
    return fig_1

def NOTA_VIZ_Constituency(df):
    current_directory = os.path.dirname(__file__)
    geojson_filename = "india_pc_2019_simplified.geojson"
    geojson_filepath = os.path.join(current_directory, geojson_filename)
    with open(geojson_filepath, "r", encoding="utf-8") as file:
        india_constituency = json.load(file)
    constituency_id_map = {}
    for feature in india_constituency["features"]:
        feature["id"] = feature["properties"]["pc_id"]
        constituency_id_map[feature["properties"]["pc_name"].lower()] = feature["id"]
    constituency_id_map = {key.lower(): int(value) for key, value in constituency_id_map.items()}
    df_winner_1 = df[df['WINNER'] == 1]
    new_df = df_winner_1[['STATE', 'CONSTITUENCY', 'PARTY']]
    new_dict={}
    for i in new_df["CONSTITUENCY"]:
        if i.lower() not in constituency_id_map:
            new_dict[i.lower()] = -1
        else:
            new_dict[i.lower()] = constituency_id_map[i.lower()]
    rows_with_NOTA = df[df['PARTY'] == 'NOTA']
    rows_with_NOTA = rows_with_NOTA[['CONSTITUENCY','OVER_TOTAL_ELECTORS_IN_CONSTITUENCY']]
    rows_without_NOTA = df[df['PARTY'] != 'NOTA']
    rows_without_NOTA = rows_without_NOTA[['CONSTITUENCY']]
    unique_constituencies = rows_without_NOTA['CONSTITUENCY'].unique()
    rows_without_NOTA = pd.DataFrame(unique_constituencies, columns=['CONSTITUENCY'])
    common_constituencies = set(rows_with_NOTA['CONSTITUENCY']).intersection(set(rows_without_NOTA['CONSTITUENCY']))
    rows_without_NOTA = rows_without_NOTA[~rows_without_NOTA['CONSTITUENCY'].isin(common_constituencies)]
    rows_without_NOTA['OVER_TOTAL_ELECTORS_IN_CONSTITUENCY'] = 0
    merged_df = pd.concat([rows_without_NOTA, rows_with_NOTA])
    merged_df['CONSTITUENCY'] = merged_df['CONSTITUENCY'].str.lower()
    merged_df['ID'] = merged_df['CONSTITUENCY'].map(new_dict)
    fig_2 = px.choropleth_mapbox(
        merged_df,
        locations="ID",
        geojson=india_constituency,
        color="OVER_TOTAL_ELECTORS_IN_CONSTITUENCY",
        color_continuous_scale=[(0, 'rgba(255, 0, 0, 0)'), (0.2, 'rgba(255, 0, 0, 0.2)'), (0.5, 'rgba(255, 0, 0, 0.5)'), (1, 'rgba(255, 0, 0, 1)')],  # Set the colorscale with varying opacity
        range_color=(0, merged_df["OVER_TOTAL_ELECTORS_IN_CONSTITUENCY"].max()),  # Set the color range
        mapbox_style="carto-positron",
        zoom = 3,
        opacity = 0.5,
        center = {"lat": 22, "lon": 77},
    )
    fig_2.update_layout(
        coloraxis_colorbar=dict(
        title='NOTA',
        # orientation='h'
    )
    )
    fig_2.update_layout(margin={"r":0,"t":0,"l":0,"b":0})
    return fig_2

def criminal_cases_constituency_wise(df):
    current_directory = os.path.dirname(__file__)
    geojson_filename = "india_pc_2019_simplified.geojson"
    geojson_filepath = os.path.join(current_directory, geojson_filename)
    with open(geojson_filepath, "r", encoding="utf-8") as file:
        india_constituency = json.load(file)
    constituency_id_map = {}
    for feature in india_constituency["features"]:
        feature["id"] = feature["properties"]["pc_id"]
        constituency_id_map[feature["properties"]["pc_name"].lower()] = feature["id"]
    constituency_id_map = {key.lower(): int(value) for key, value in constituency_id_map.items()}
    winners = df[df['WINNER'] == 1]
    winners = winners[['CONSTITUENCY','CRIMINAL_CASES']]
    winners['CRIMINAL_CASES_log'] = np.where(winners['CRIMINAL_CASES'] != 0, np.log(winners['CRIMINAL_CASES']), 0)
    new_dict={}
    for i in winners["CONSTITUENCY"]:
        if i.lower() not in constituency_id_map:
            new_dict[i.lower()] = -1
        else:
            new_dict[i.lower()] = constituency_id_map[i.lower()]
    winners['CONSTITUENCY'] = winners['CONSTITUENCY'].str.lower()
    winners['ID'] = winners['CONSTITUENCY'].map(new_dict)
    import plotly.express as px
    fig_1 = px.choropleth(
        winners,
        locations="ID",
        geojson=india_constituency,
        color="CRIMINAL_CASES",
        color_continuous_scale=[(0, 'rgba(255, 0, 0, 0)'), (0.2, 'rgba(255, 0, 0, 0.2)'), (0.5, 'rgba(255, 0, 0, 0.5)'), (1, 'rgba(255, 0, 0, 1)')],  # Set the colorscale with varying opacity
        range_color=(0, winners["CRIMINAL_CASES_log"].max()),  # Set the color range
    )
    fig_1 = px.choropleth_mapbox(
        winners,
        locations="ID",
        geojson=india_constituency,
        color="CRIMINAL_CASES",
        color_continuous_scale=[(0, 'rgba(255, 0, 0, 0)'), (0.2, 'rgba(255, 0, 0, 0.2)'), (0.5, 'rgba(255, 0, 0, 0.5)'), (1, 'rgba(255, 0, 0, 1)')],  # Set the colorscale with varying opacity
        range_color=(0, winners["CRIMINAL_CASES_log"].max()),  # Set the color range
        mapbox_style="carto-positron",
        zoom = 3,
        opacity = 0.5,
        center = {"lat": 22, "lon": 77},
    )
    fig_1.update_geos(fitbounds="locations", visible=False)
    log_max =winners["CRIMINAL_CASES_log"].max()
    fig_1.update_layout(
        margin={"r":0,"t":0,"l":0,"b":0},
        coloraxis_colorbar=dict(
            title='Criminal Cases',
            # orientation='h',
            tickvals=[0, log_max/4, (log_max/4)*2, (log_max/4)*3, log_max],  # Custom tick values
            ticktext=['0', '50', '100', '150', '200']  # Custom tick labels
        )
    )
    return fig_1

def criminal_cases_india_wise(df):
    current_directory = os.path.dirname(__file__)
    geojson_filename = "states_india.geojson"
    geojson_filepath = os.path.join(current_directory, geojson_filename)
    india_states = json.load(open(geojson_filepath, "r"))
    state_id_map = {}
    for feature in india_states["features"]:
        feature["id"] = feature["properties"]["state_code"]
        state_id_map[feature["properties"]["st_nm"].lower()] = feature["id"]
    corrections = {
    'ANDAMAN & NICOBAR ISLANDS': 'ANDAMAN & NICOBAR ISLAND',
    'ARUNACHAL PRADESH': 'ARUNANCHAL PRADESH',
    'DADRA & NAGAR HAVELI': 'DADARA & NAGAR HAVELLI',
    }
    df = df[df['CRIMINAL_CASES'] >= 0]
    df['STATE'] = df['STATE'].replace(corrections)
    average_cases_df = df.groupby('STATE')['CRIMINAL_CASES'].sum().reset_index()
    average_cases_df['STATE'] = average_cases_df['STATE'].str.lower()
    average_cases_df["id"] = average_cases_df["STATE"].apply(lambda x: state_id_map[x])
    #Plotly for india map
    custom_color_scale = [
    [0.0, 'rgba(255, 255, 255, 0.3)'],  # Define color for lower range with lower opacity
    [0.5, 'rgba(255, 0, 0, 0.6)'],  # Define color for middle range with medium opacity
    [1.0, 'rgba(255, 0, 0, 1.0)']  # Define color for upper range with full opacity
    ]

    fig_2 = px.choropleth_mapbox(
        average_cases_df,
        locations="id",
        geojson=india_states,
        hover_name="STATE",
        range_color=(average_cases_df['CRIMINAL_CASES'].min(), average_cases_df['CRIMINAL_CASES'].max()),
        color='CRIMINAL_CASES',
        color_continuous_scale=custom_color_scale,
        mapbox_style="carto-positron",
        zoom = 3,
        opacity = 0.5,
        center = {"lat": 22, "lon": 77},
    )
    fig_2.update_geos(fitbounds="locations", visible=False)
    fig_2.update_layout(
        margin={"r":0,"t":0,"l":0,"b":0},
    coloraxis_colorbar=dict(
        title='Criminal Cases',
        # orientation='h'
    )
    )
    return fig_2


def Update_Bar_Graph(selected_state):
    df = bar_graph_df
    # selected_state = clickData['points'][0]['hovertext']
    if selected_state == 'ANDAMAN & NICOBAR ISLAND':
        selected_state = 'ANDAMAN & NICOBAR ISLANDS'
    if selected_state == 'ARUNANCHAL PRADESH':
        selected_state = 'ARUNACHAL PRADESH'
    if selected_state == 'DADARA & NAGAR HAVELLI':
        selected_state = 'DADRA & NAGAR HAVELI'
    new_df = df[df['STATE'] == selected_state]
    wins_by_party = new_df.groupby('PARTY')['WINNER'].sum().reset_index()
    wins_by_party = wins_by_party.sort_values(by='WINNER', ascending=False)
    top_ten_parties = wins_by_party.head(10)
    fig_2 = px.bar(top_ten_parties, 
                       x='PARTY', 
                       y='WINNER',
                       # color='WINNER',
                       title=f"{selected_state} : Constituencies Won per Party",
                       color_continuous_scale='Viridis')
    # fig_2.update_layout(
    #         xaxis=dict(title='Party', tickmode='linear'),
    #         yaxis=dict(title='Wins'),
    #         # title_font=dict(size=20),
    #         # font=dict(size=14,color='#FFFFFF'),#{'color': '#FFFFFF','size':'14'},
    #         # paper_bgcolor ='#303030',
    #         # plot_bgcolor = '#303030',
    #         # margin=dict(l=0, r=0, t=0, b=0),  # Set margins to zero
    #         # autosize=True,
    #     )
    return fig_2
    
###################################################################
# df = pd.read_csv("modified_dataset.csv")
# graph_bar_graph_ss = IndiaMap(df)
# graph_bar_graph_ss.show()