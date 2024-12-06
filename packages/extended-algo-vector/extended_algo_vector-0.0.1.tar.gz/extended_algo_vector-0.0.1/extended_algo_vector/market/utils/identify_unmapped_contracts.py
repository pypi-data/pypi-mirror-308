import logging, time, os
import pathlib

import pandas as pd
import numpy as np
import datetime as dt
import dotenv
import pathlib

dotenv.load_dotenv()

pd.set_option('display.width', 1000, 'display.max_columns', 1000)


# Note: This is a utility function that looks at the unique symbols defined in the market data folder
#  and verifies if the contract has been set up extended_algo_vector


def _load_unique_symbols():
    symbols = []
    source_dir = pathlib.Path(os.getenv('MARKET_DATA_LOCAL_DIR'))
    print(source_dir)
    for folder, sub_dir, files in os.walk(source_dir):
        symbol_dir = pathlib.Path(folder)

        if symbol_dir.stem.lower() in ['yahoo_opt_chain']:
            continue
        if len(files) > 0:
            if '.zip' in files[0]:
                symbols.append([symbol_dir.stem, symbol_dir.parts[-2], len(files)])

    # TODO: I may need to exclude intermarket symbols

    df = pd.DataFrame(symbols, columns=['symbol', 'market_data_type', 'count'])
    df = df.groupby(['market_data_type', 'symbol']).sum()
    df = df.unstack('market_data_type').droplevel(0, axis=1)

    df = df.drop(['ib_seconds_data', 'ib_tick_data'], axis=1, errors='ignore')

    df_occurence = df.copy()
    df_occurence = df_occurence.div(df_occurence.abs())

    df_occurence['count'] = df_occurence.sum(axis=1)
    df_occurence = df_occurence[['count']]
    df = pd.concat([df, df_occurence], axis=1)
    df = df.sort_values('count', ascending=False)
    df = df[df['count'] > 0]

    return df


def _load_configured_contracts():
    # TODO: Ignoring ib_seconds and ib_tick_data and only focusing on iq_tick bars
    ...


if __name__ == '__main__':
    df = _load_unique_symbols()
    df = df.reset_index()
    df = df.groupby('count').agg({'symbol': set})
    print(df)

    dfs = []
    for x in df.itertuples():
       _df = pd.DataFrame(x.contract, columns=[x.Index])
       _df = _df.sort_values(x.Index, ascending=True, ignore_index=True)
       dfs.append(_df)

    dfs = pd.concat(dfs, axis=1).fillna('')
    dfs.to_clipboard()

    print(dfs)



