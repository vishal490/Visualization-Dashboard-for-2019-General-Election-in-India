import numpy as np
import pandas as pd
import plotly.express as px
import plotly.graph_objs as go
import json

# Required column mappings
base_col = ["STATE", "CONSTITUENCY", "PARTY"]
process_cols = ["GENDER", "AGE", "CATEGORY", "EDUCATION"] #, "ASSETS", "LIABILITIES", "CRIMINAL_CASES"]
numerical_cols =  ["AGE", "ASSETS", "LIABILITIES", "CRIMINAL_CASES"]
numerical_col_bins = {"CRIMINAL_CASES":2, "AGE":3, "ASSETS":5, "LIABILITIES":3}
use_case_columns = base_col + process_cols

MAX_BARS = 10

DATASET = None
col_dataframe_dict = {}
seats_won_dataset_for_sample_plot = None
state_constituencies_sample_df = None

def get_party_count(parties):
    count = [check_df[check_df.PARTY==party]["Count"].tolist() for party in parties]
    return [ele[0] if len(ele) > 0 else 0 for ele in count]

def get_party_record_count_and_filter(df):
    added_df = pd.merge(df, pd.DataFrame([{"PARTY":key, "Total_Count":value} for key, value in df.groupby("PARTY")["Count"].sum().to_dict().items()])).sort_values("Total_Count", ascending=False)
    filtered_totals = added_df.Total_Count.unique()[:MAX_BARS]
    return added_df[added_df.Total_Count.isin(filtered_totals)]

def sample_dummy_processing(dataset):
    global seats_won_dataset_for_sample_plot
    global state_constituencies_sample_df
    seats_won_dataset_for_sample_plot = pd.DataFrame([{"STATE":ele[0], "PARTY":ele[1], "NUM_SEATS_WON":ele[2]} for ele in dataset[dataset.WINNER == 1][["STATE", "CONSTITUENCY", "PARTY"]].groupby(["STATE", "PARTY"]).count().to_records()]).sort_values(["STATE", "NUM_SEATS_WON"], ascending=False)
    seats_won_dataset_for_sample_plot.head(1)

    state_constituencies_sample_df = pd.DataFrame([{"STATE":ele[0], "NUM_CONSTITUENCY":ele[1]} for ele in dataset[["STATE", "CONSTITUENCY"]].drop_duplicates().groupby("STATE").count().to_records()]).sort_values("NUM_CONSTITUENCY", ascending=False)
    state_constituencies_sample_df.head(1)


def party_stats_process(dataset):
    """
    Process the incoming dataset based on the current use case
    """
    
    r_df = dataset[use_case_columns]
    r_df = r_df[r_df.PARTY != "NOTA"].reset_index()
    r_df = r_df.replace(to_replace=-1, value=np.nan)
    
    global DATASET
    DATASET = r_df
    
    global col_dataframe_dict
    for col in process_cols:
    
        req_col_df = r_df[~r_df[base_col+[col]].isna().any(axis=1)][base_col+[col]]

        # From each of these col specific datasets, remove nan columnns and if numerical then perform the binning
        if col in numerical_cols:
            req_col_df[col] = pd.qcut(req_col_df[col], q=numerical_col_bins[col]).astype(str)

        col_dataframe_dict[col] = req_col_df

def get_state_updated_plots_party_stats(state):
    
    global col_dataframe_dict
    
    if state is None:
        # Just return empty figs
#         figs = {}
#         for col, _ in col_dataframe_dict.items():
#             empty_fig = {
#                     'data': [],
#                     'layout': go.Layout(title=f"{str(state)} : Party vs {col}")
#                 }
#             figs[col] = empty_fig
        
#         return figs
        state_col_dataframe_dict = {col: df.groupby(['PARTY', col]).size().reset_index(name='Count') for col, df in col_dataframe_dict.items()}
        figs = {}
        for col, col_df in state_col_dataframe_dict.items():
            state_col_dataframe_dict[col] = get_party_record_count_and_filter(col_df)
            figs[col] = px.bar(state_col_dataframe_dict[col], x="PARTY", y="Count", color=col, title=f"India : {col} DISTRIBUTION OF CANDIDATES PER POLITICAL PARTY", )
        return figs
        
    # print(col_dataframe_dict)
    state_col_dataframe_dict = {col: df[df.STATE==state].groupby(['PARTY', col]).size().reset_index(name='Count') for col, df in col_dataframe_dict.items()}
    figs = {}
    for col, col_df in state_col_dataframe_dict.items():
        state_col_dataframe_dict[col] = get_party_record_count_and_filter(col_df)
        figs[col] = px.bar(state_col_dataframe_dict[col], x="PARTY", y="Count", color=col, title=f"{state} : {col} DISTRIBUTION OF CANDIDATES PER POLITICAL PARTY", )
        # figs[col].update_layout(plot_bgcolor='#303030', paper_bgcolor='#303030', font=dict(size=14,color='#FFFFFF'))
        
    return figs

def sample_seats_won_state_wise(selected_column):
    
    if selected_column is None:
        return {
                'data': [],
                'layout': go.Layout(title=f'Sample : {str(selected_column)} : NUM of Constituencies Won per Party')
            }
    
    global seats_won_dataset_for_sample_plot
    filtered_df = seats_won_dataset_for_sample_plot[seats_won_dataset_for_sample_plot.STATE == selected_column]
    figure={
    'data': [go.Bar(x=filtered_df['PARTY'], y=filtered_df['NUM_SEATS_WON'])],
    'layout': go.Layout(title=f'Sample : {selected_column} : NUM of Constituencies Won per Party')
    }
    return figure

def sample_state_constituencies_count():
    global state_constituencies_sample_df
    figure={
        'data': [go.Bar(x=state_constituencies_sample_df['STATE'], y=state_constituencies_sample_df['NUM_CONSTITUENCY'])],
        'layout': go.Layout(title='Sample : NUM of Constituencies per State')
    }
    return figure