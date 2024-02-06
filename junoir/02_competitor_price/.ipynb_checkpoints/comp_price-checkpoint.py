import pandas as pd

def agg_comp_price(X: pd.DataFrame) -> pd.DataFrame:
    '''
    Function calculate and new_price acording data was gave.
    return: new dataframe
    '''
    grouped_df = X.groupby('sku')
    result_df = pd.DataFrame(columns=['sku', 'agg', 'base_price', 'comp_price', 'new_price'])

    for sku, group in grouped_df:
        if group['agg'].iloc[0] == 'min':
            agg_price = group['comp_price'].min()

        elif group['agg'].iloc[0] == 'max':
            agg_price = group['comp_price'].max()

        elif group['agg'].iloc[0] == 'med':
            agg_price = group['comp_price'].median()

        elif group['agg'].iloc[0] == 'avg':
            agg_price = group['comp_price'].mean()

        elif group['agg'].iloc[0] == 'rnk':
            agg_price = group.loc[group['rank'].idxmin(), 'comp_price']

        if 0.8 * group['base_price'].iloc[0] <= agg_price <= 1.2 * group['base_price'].iloc[0]:
            new_price = agg_price
        else:
            new_price =group['base_price'].iloc[0]

        result_df.loc[sku] = (sku, group['agg'].iloc[0],
                              group['base_price'].iloc[0],
                              agg_price, new_price)
    return result_df.infer_objects()
    