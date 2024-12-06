import dataclasses
from typing import Optional

import pandas as pd


@dataclasses.dataclass
class SimulationResult:
    timeseries: Optional[pd.Series] = None
    T: Optional[pd.Series] = None
    P: Optional[pd.Series] = None
    E: Optional[pd.Series] = None
    Q_obs: Optional[pd.Series] = None
    U_soil: Optional[pd.Series] = None
    S_snow: Optional[pd.Series] = None
    Q_snow: Optional[pd.Series] = None
    Q_inter: Optional[pd.Series] = None
    E_eal: Optional[pd.Series] = None
    Q_of: Optional[pd.Series] = None
    Q_g: Optional[pd.Series] = None
    Q_bf: Optional[pd.Series] = None
    Q_sim: Optional[pd.Series] = None
    L_soil: Optional[pd.Series] = None

    def to_dataframe(self):
        data = {field.name: getattr(self, field.name) for field in dataclasses.fields(self)}
        if any(value is None for value in data.values()):
            return None
        return pd.DataFrame(data)
