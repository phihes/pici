import pandas as pd
from abc import ABC, abstractmethod
from typing import overload
from pandas.api.types import CategoricalDtype
from pici.datatypes import CommunityDataLevel


class Labels(ABC):
    DEFAULT_COLS = {
        'community': 'community',
        'id': 'id',
        'labeller': 'labeller'
    }

    def __init__(self, data: pd.DataFrame, cols: dict = DEFAULT_COLS):
        """

        Args:
            data:
            cols:
        """
        for c in cols:
            if c not in data.columns:
                raise KeyError(f"Required column {c} not in data")
        self._data = data.astype(self.labels)
        self._data = self._generate_extra_labels(self._data)
        self._cols = cols

    @property
    def data(self):
        return self._data

    @overload
    def data(self, community_name):
        return self.data[
            self.data[self._cols['community'] == community_name]
        ]

    @property
    def _required_cols(self):
        return self._cols.values() + self.labels.keys()

    @property
    def labels(self) -> dict:
        raise NotImplementedError

    @property
    def level(self) -> CommunityDataLevel:
        raise NotImplementedError

    @abstractmethod
    def _generate_extra_labels(self, data):
        pass


class InnovationLabels(Labels):
    POTENTIAL_DTYPE = CategoricalDtype(
        categories=[0, 1, 2], ordered=True
    )

    labels = {
        'label_idea': 'bool',
        'label_evaluation': 'bool',
        'label_implementation': 'bool',
        'label_modification': 'bool',
        'label_improvement': 'bool',
        'label_potential': POTENTIAL_DTYPE,
    }

    level = CommunityDataLevel.TOPICS

    def _generate_extra_labels(self, data):
        try:
            activities = data[[
                'label_idea', 'label_evaluation', 'label_implementation',
                'label_modification', 'label_improvement'
            ]]
            data["label_any_activity"] = activities.any()
            self.labels['label_any_activity'] = 'bool'
        except KeyError:
            pass

        try:
            data["label_has_potential"] = data["label_potential"] > 0
            self.labels["label_has_potential"] = "bool"
        except KeyError:
            pass

        return data
