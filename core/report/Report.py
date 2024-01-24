import core.config as cfg
import core.utils as utils

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
    df.to_excel(_f+'.xlsx', index=True)

    with open(fname, 'w') as file:
        file.write(html_document)