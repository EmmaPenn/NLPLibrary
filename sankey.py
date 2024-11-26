'''
sankey.py: a file that generates sankey diagrams

Authors: Emma Penn, Imogen Slavin, Jessica Baumann
DS 3500 Fall 2024
Professor John Rachlin
'''

import pandas as pd
import plotly.graph_objects as go

pd.set_option('future.no_silent_downcasting', True)

def _code_mapping(df, src, targ):
    """ Map labels in src and targ colums to integers """


    # Get the distinct labels
    labels = sorted(list(set(list(df[src]) + list(df[targ]))))

    # Create a label->code mapping
    codes = range(len(labels))
    lc_map = dict(zip(labels, codes))

    # Substitute codes for labels in the dataframe
    df = df.replace({src: lc_map, targ: lc_map})

    return df, labels

def _stack(df, lst, val_col = None):
    '''
    Stacks multiple columns within a dataframe with or without a values column.
    df: dataframe
    lst: list of columns you want to stack
    val_col: values column to stack (optional)
    gives back one big stacked dataframe
    '''
    position = 2

    if val_col:
        original_df = group_function(df, [lst[0], lst[1]], counts_name=val_col)
        original_df.columns = ["src", "targ", "val"]
        while position < (len(lst)):
            new_df = group_function(df, [lst[position - 1], lst[position]], counts_name=val_col)
            new_df.columns = ["src", "targ", "val"]
            original_df = pd.concat([original_df, new_df], axis=0)
            position += 1

    else:
        original_df = df[[lst[0], lst[1]]]
        original_df.columns = ["src", "targ"]
        while position < (len(lst)):
            new_df = df[[lst[position -1], lst[position]]]
            new_df.columns = ["src", "targ"]
            original_df = pd.concat([original_df, new_df], axis = 0)
            position += 1

    return original_df

def group_function(df, group_names, counts_name):
    '''
    Groups dataframes together and gives the count of each unique element in the counts_name column, used for
    multi-level sankey diagrams when dataframes have to be stacked
    '''
    new_group = df.groupby(group_names, as_index = False)[counts_name].nunique()

    return new_group

def make_sankey(df, lst, vals=None, **kwargs):
    """
    Create a sankey figure
    df - Dataframe
    lst - A list of columns that you want the nodes to be for a multi-level sankey and 2D sankey
    vals - Link values (thickness)
    """

    if len(lst) < 2:
        print("Make Sure Columns are a List and there are at least 2 for Sankey")
    else:
        if vals:
             values = df[vals]
        else:
             values = [1] * len(df)


        if len(lst) > 2:

          if vals:
              df = _stack(df,lst, vals)

              values = df["val"]
          else:
              df = _stack(df, lst)
              values = [1]*len(df)
          df, labels = _code_mapping(df, "src", "targ")
        else:

            if vals:
                values = df[vals]
            else:
                values = [1] * len(df)
            src = lst[0]
            targ = lst[1]
            df = df[[src, targ]]

            df, labels = _code_mapping(df,src,targ)

            df.columns = ["src", "targ"]


        link = {'source': df["src"], 'target': df["targ"], 'value': values}
        thickness = kwargs.get("thickness", 50)  # 50 is the presumed default value
        pad = kwargs.get("pad", 50)

        node = {'label': labels, 'thickness': thickness, 'pad': pad}

        sk = go.Sankey(link=link, node=node)
        fig = go.Figure(sk)
        fig.show()
