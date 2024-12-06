from datetime import datetime
from typing import List

import pandas as pd

from hydnam.columns_constants import TIME_SERIES, TEMPERATURES, PRECIPITATIONS, EVAPOTRANSPIRATIONS, DISCHARGES


class Dataset:
    def __init__(self, time_series: List[datetime], temperatures: List[float],
                 precipitations: List[float], evapotranspirations: List[float],
                 discharges: List[float]):
        self._time_series = time_series
        self._temperatures = temperatures
        self._precipitations = precipitations
        self._evapotranspirations = evapotranspirations
        self._discharges = discharges

    def to_dataframe(self):
        dataset_dict = {
            TIME_SERIES: self._time_series,
            TEMPERATURES: self._temperatures,
            PRECIPITATIONS: self._precipitations,
            EVAPOTRANSPIRATIONS: self._evapotranspirations,
            DISCHARGES: self._discharges
        }

        df = pd.DataFrame(dataset_dict)
        df[TIME_SERIES] = pd.to_datetime(df[TIME_SERIES])
        return df
