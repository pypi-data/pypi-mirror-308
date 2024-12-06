import numpy as np
import pandas as pd
import odhpy.io as oio

class TimeseriesDataframe(pd.DataFrame):

    def __init__(self) -> None:
        """
        A TimeseriesDataframe is thinly extended pd.Dataframe. In addition to the
        normal dataframe stuff, it also has:
            a name (str)
            a source (str)
            a description (str)
            a string of tags (str)
            some useful methods.
        
        Args:
            None
        """
        super().__init__()
        self.name = ""
        self.source = ""
        self.description = ""
        self.tag = ""

    def copy_from_dataframe(self, df):
        super().__init__(df)

    def copy_from_file(self, filename):
        super().__init__(oio.read(filename))
        self.source = filename

    def print_summary(self):
        print(f"Name: {self.name}")
        print(f"Source: {self.source}")
        print(f"Description: {self.description}")
        print(f"Tag: {self.tag}")
        print(self.describe())

    @classmethod
    def from_dataframe(cls, df):
        tsdf = cls()
        tsdf.copy_from_dataframe(df)
        return tsdf

    @classmethod
    def from_file(cls, filename):
        tsdf = cls.from_dataframe(oio.read(filename))
        return tsdf


class DataframeEnsemble:

    def __init__(self) -> None:
        """
        A DataframeEnsemble is an collection of odhpy-style timeseries dataframes, which might represent collected results from a set of model runs.
        Each timeseries dataframe is stored in an internal object, with a little attached metadata. 
        All timeseries in the ensemble are expected to have the same index, and the same columns.
        
        Args:
            None
        """        
        self.ensemble = {}

    def add_dataframe(self, df, key=None, tag=None):
        if (not isinstance(df, TimeseriesDataframe)):
            df = TimeseriesDataframe.from_dataframe(df)
        if tag is not None:
            df.tag = tag
        self.assert_df_shape_matches_ensemble(df)
        if key is None:
            # Automatically pick the next available integer to use as a key
            key = 0
            while key in self.ensemble:
                key += 1
        self.ensemble[key] = df

    def add_dataframe_from_file(self, filename, key=None, tag=None):
        df = TimeseriesDataframe.from_file(filename)
        self.add_dataframe(df, key, tag)

    def print_summary(self):
        for key in self.ensemble:
            print(f"Key: {key}, Shape: {self.ensemble[key].shape}")

    def df_shape_matches_ensemble(self, new_df) -> bool:
        if len(self.ensemble) > 0:
            first_shape = list(self.ensemble.values())[0].shape
            new_df_shape = new_df.shape
            if first_shape != new_df_shape:
                return False
        return True
        
    def assert_df_shape_matches_ensemble(self, new_df):
        if len(self.ensemble) > 0:
            first_shape = list(self.ensemble.values())[0].shape
            new_df_shape = new_df.shape
            if first_shape != new_df_shape:
                raise Exception(f"ERROR: New Dataframe has shape {new_df_shape} but the ensemble members have shape {first_shape}!")
            