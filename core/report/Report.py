import core.config as cfg
import core.utils as utils
import pandas as pd

def save_optimization_report(name, df, inputfile, executiontime):
    df['cfg'] = '' # add empty column for file download
    html_table = df.to_html(classes="dataframe display compact hover", index=True, escape=False)

    lastupdate = cfg.OUTPUT_FILENAME

    html_document = utils.load_from_file(cfg.OPTIMIZATION_REPORT_TEMPLATE)
    html_document = html_document.replace("{html_table}", html_table)
    html_document = html_document.replace("{name}", name)
    html_document = html_document.replace("{input-file}", inputfile)
    html_document = html_document.replace("{lastupdate}", lastupdate)
    html_document = html_document.replace("{executiontime}", executiontime)

    _f = cfg.OPTIMIZATION_REPORT_PATH+'/optimization_report_'+name+'_'+lastupdate
    fname = str(_f+'.html')

    # also save in xlsx file
    df.to_excel(_f+'.xlsx', index=True)

    with open(fname, 'w') as file:
        file.write(html_document)


def save_strategy_equity(df, _name):
    _df = pd.DataFrame()
    _df['date'] = df['market_date']
    _df['pnl'] = df['pnl']

    _df['date'] = pd.to_datetime(_df['date'])
    date_complete = pd.date_range(start=_df['date'].min(), end=_df['date'].max(), freq='B')
    _df = _df.set_index('date').reindex(date_complete).reset_index()

    # fill the gap with zero values
    #_df['pnl'] = _df['pnl'].fillna()

    lastupdate = cfg.OUTPUT_FILENAME
    _f = cfg.EQUITY_OUTPUT+'/'+_name+'_'+lastupdate+"_eq.csv"
    _df.to_csv(_f, sep=cfg.CSV_SEPARATOR, header=False, index=False)



def save_strategy_report(df, _name):
    return