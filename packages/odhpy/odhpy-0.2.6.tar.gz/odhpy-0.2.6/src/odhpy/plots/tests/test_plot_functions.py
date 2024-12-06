import unittest
import random
import pandas as pd
from odhpy import plots, utils, io
import matplotlib.pyplot as plt
from datetime import datetime

class Tests(unittest.TestCase):
    
    def test_flow_plot(self):
        df = pd.DataFrame()
        df["a"] = [random.normalvariate(40,5) for _ in range(200)]
        df["b"] = [random.normalvariate(50,5) for _ in range(200)]
        df["c"] = [random.normalvariate(60,5) for _ in range(200)]
        df = utils.set_index_dt(df, start_dt=datetime(2000, 1, 1))
        plots.plot_flow(df)
        #plt.show()       
    
    def test_exceedence_plot(self):
        df = pd.DataFrame()
        df["a"] = [random.normalvariate(40,5) for _ in range(200)]
        df["b"] = [random.normalvariate(50,5) for _ in range(200)]
        df["c"] = [random.normalvariate(60,5) for _ in range(200)]
        plots.plot_exceedence(df)
        #plt.show()

    def test_flow_plotx(self):
        df = pd.DataFrame()
        df["a"] = [random.normalvariate(40,5) for _ in range(200)]
        df["b"] = [random.normalvariate(50,5) for _ in range(200)]
        df["c"] = [random.normalvariate(60,5) for _ in range(200)]
        df = utils.set_index_dt(df, start_dt=datetime(2000, 1, 1))
        fig = plots.plot_flowx(df)
        #fig.write_html("c:/temp/blarg.html")
        #fig.show()

    def test_exceedence_plot(self):
        start_dt=datetime(1889, 1, 1)
        df = pd.DataFrame()
        df["a"] = [random.normalvariate(40,5) for _ in range(3650)]
        df["b"] = [random.normalvariate(50,5) for _ in range(3650)]
        df["c"] = [random.normalvariate(60,5) for _ in range(3650)]
        df.index = utils.get_dates(start_dt, days=3650,str_format=r'%Y-%m-%d')
        df.index.name = "Date"
        plots.exceedence_plot(df)

    def test_daily_plot(self):
        start_dt=datetime(1889, 1, 1)
        df = pd.DataFrame()
        df["a"] = [random.normalvariate(40,5) for _ in range(3650)]
        df["b"] = [random.normalvariate(50,5) for _ in range(3650)]
        df["c"] = [random.normalvariate(60,5) for _ in range(3650)]
        df.index = utils.get_dates(start_dt, days=3650,str_format=r'%Y-%m-%d')
        df.index.name = "Date"
        plots.daily_plot(df)

    def test_annual_plot(self):
        start_dt=datetime(1889, 1, 1)
        df = pd.DataFrame()
        df["a"] = [random.normalvariate(40,5) for _ in range(3650)]
        df["b"] = [random.normalvariate(50,5) for _ in range(3650)]
        df["c"] = [random.normalvariate(60,5) for _ in range(3650)]
        df.index = utils.get_dates(start_dt, days=3650,str_format=r'%Y-%m-%d')
        df.index.name = "Date"
        plots.annual_plot(df)

    def test_residual_mass_curve(self):
        start_dt=datetime(1889, 1, 1)
        df = pd.DataFrame()
        df["a"] = [random.normalvariate(40,5) for _ in range(3650)]
        df["b"] = [random.normalvariate(50,5) for _ in range(3650)]
        df["c"] = [random.normalvariate(60,5) for _ in range(3650)]
        df.index = utils.get_dates(start_dt, days=3650,str_format=r'%Y-%m-%d')
        df.index.name = "Date"
        plots.residual_mass_curve(df)

    def test_storage_plot(self):
        start_dt=datetime(1889, 1, 1)
        df = pd.DataFrame()
        df["a"] = [random.normalvariate(40,5) for _ in range(3650)]
        df["b"] = [random.normalvariate(50,5) for _ in range(3650)]
        df["c"] = [random.normalvariate(60,5) for _ in range(3650)]
        triggers={"L1": 40, "L2": 50, "L3": 60}
        df.index = utils.get_dates(start_dt, days=3650,str_format=r'%Y-%m-%d')
        df.index.name = "Date"
        plots.storage_plot(df,triggers)

    def test_annual_demand_supply_plot(self):
        start_dt=datetime(1889, 1, 1)
        df = pd.DataFrame()
        df["a"] = [random.normalvariate(40,5) for _ in range(3650)]
        df["b"] = [random.normalvariate(50,5) for _ in range(3650)]
        df.index = utils.get_dates(start_dt, days=3650,str_format=r'%Y-%m-%d')
        df.index.name = "Date"
        plots.annual_demand_supply_plot(df["b"],df["a"])
    
    def test_pyblo(self):
        pathlist=['./src/odhpy/examples/Pyblo/919001C.csv','./src/odhpy/examples/Pyblo/919001B.csv','./src/odhpy/examples/Pyblo/919001A.csv','./src/odhpy/examples/Pyblo/919003A.csv','./src/odhpy/examples/Pyblo/919009B.csv','./src/odhpy/examples/Pyblo/919009A.csv']
        df_list=[]
        for i in range(len(pathlist)):
            df_list.append(io.read_ts_csv(pathlist[i])["Total"])
        sites=["919001C","919001B","919001A","919003A","919009B","919009A"]
        series=["Gauge data","Gauge data","Gauge data","Gauge data","Gauge data","Gauge data"]
        plots.pyblo(df_list,sites,series)

    def test_wy_event_heatmap(self):
        start_dt=datetime(1889, 1, 1)
        df = pd.DataFrame()
        df["a"] = [random.binomialvariate(p=0.001) for _ in range(3650)]
        df["b"] = [random.binomialvariate(p=0.001) for _ in range(3650)]
        df["c"] = [random.binomialvariate(p=0.001) for _ in range(3650)]
        df.index = utils.get_dates(start_dt, days=3650,str_format=r'%Y-%m-%d')
        df.index.name = "Date"
        df_annual=df.groupby(utils.get_wy(df.index)).max()
        plots.wy_event_heatmap(df_annual)

    def test_plot_flow(self):
        df = io.read_ts_csv("./src/odhpy/io/tests/test_data2.csv")
        plots.plot_flow(df)


