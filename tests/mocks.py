from typing import Iterable

import dask.dataframe as dd
import pandas as pd
from strawman import dummy_df, dummy_triples
from util import DatasetStatistics

from sylloge.base import EA_SIDE_LEFT, EA_SIDE_RIGHT, EA_SIDES


class DataPathMocker:
    def __init__(self, data_path):
        self.data_path = data_path

    def mock_data_path(self):
        return self.data_path


class ResourceMocker:
    def __init__(self, statistic: DatasetStatistics, fraction: float, seed: int = 17):
        self.statistic = statistic
        self.fraction = fraction
        self.seed = seed

    def mock_read(self, path: str, names: Iterable):
        return self.mock_read_zipfile_csv(path="", inner_path=path)

    def mock_read_zipfile_csv(self, inner_path: str, **kwargs) -> pd.DataFrame:
        if "rel_triples_1" in inner_path:
            return dummy_triples(
                int(self.statistic.num_rel_triples_left * self.fraction),
                entity_prefix=EA_SIDE_LEFT,
                seed=self.seed,
            )
        elif "rel_triples_2" in inner_path:
            return dummy_triples(
                int(self.statistic.num_rel_triples_right * self.fraction),
                entity_prefix=EA_SIDE_RIGHT,
                seed=self.seed,
            )
        elif "attr_triples_1" in inner_path:
            return dummy_triples(
                int(self.statistic.num_attr_triples_left * self.fraction),
                entity_prefix=EA_SIDE_LEFT,
                relation_triples=False,
                seed=self.seed,
            )
        elif "attr_triples_2" in inner_path:
            return dummy_triples(
                int(self.statistic.num_attr_triples_right * self.fraction),
                entity_prefix=EA_SIDE_RIGHT,
                relation_triples=False,
                seed=self.seed,
            )
        elif "_links" in inner_path:
            return dummy_df(
                shape=(int(self.statistic.num_ent_links * self.fraction), 2),
                content_length=100,
                columns=list(EA_SIDES),
                seed=self.seed,
            )

    def mock_read_dask_df_archive_csv(self, inner_path: str, **kwargs) -> dd.DataFrame:
        return dd.from_pandas(
            self.mock_read_zipfile_csv(inner_path=inner_path), npartitions=1
        )
