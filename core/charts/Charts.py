# =======================================================================================================================
# QStudio - Yields.py class
# (c) Alberto Sfolcini <a.sfolcini@gmail.com>
# www.surprisalx.com
# =======================================================================================================================
import math
import matplotlib.pyplot as plt
import pandas as pd

from core.Datahub import Datahub
import core.config as cfg
import numpy as np
import plotly.graph_objects as go
import plotly.express as px

class Charts:
    """
    CHARTS CLASS.
    call the generate() method
    """
    overlay = False
    s = Datahub()
    show_chart = True
    """
    INIT
    """

    def __init__(self, _s, show=True, overlay=False):
        self.s = _s
        self.show_chart = show
        self.overlay = overlay

    def generate(self, periods=9999):
        """
        GENERATE CANDLESTICK CHART
        """
        for s in self.s.get_symbols():
            r = self.s.load_data(s, periods)
            fig = go.Figure(data=[go.Candlestick(x=r['Date'],
                                                 open=r['Open'],
                                                 high=r['High'],
                                                 low=r['Low'],
                                                 close=r['Close']
                                                 )])
            fig.update_layout(title=str(s)+" (last "+str(periods)+" periods)", xaxis_rangeslider_visible=False)
            if self.show_chart:
                fig.show()
            else:
                fig.write_image(cfg.OUTPUT_REPOSITORY+"chartcandles_"+str(s).replace("." ,"")+"_"+cfg.OUTPUT_FILENAME+".png")



    def generate_line(self, periods):
        for s in self.s.get_symbols():
            r = self.s.load_data(s, periods)
            fig = px.line(r, x='Date', y='Close', title=str(s)+" (last "+str(periods)+" periods)")

            fig.update_xaxes(
                rangeslider_visible=False,
                rangeselector=dict(
                    buttons=list([
                        dict(count=1, label="1m", step="month", stepmode="backward"),
                        dict(count=6, label="6m", step="month", stepmode="backward"),
                        dict(count=1, label="YTD", step="year", stepmode="todate"),
                        dict(count=1, label="1y", step="year", stepmode="backward"),
                        dict(step="all")
                    ])
                )
            )

            if self.show_chart:
                fig.show()
            else:
                fig.write_image(cfg.OUTPUT_REPOSITORY+"chart_"+str(s).replace("." ,"")+"_"+cfg.OUTPUT_FILENAME+".png")
