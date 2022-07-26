import pandas as pd
import janitor
from abc import ABC, abstractmethod
from typing import overload
from pandas.api.types import CategoricalDtype
from pici.datatypes import CommunityDataLevel
import os


class Labels(ABC):
    """
    TODO: add documentation
    """

    DEFAULT_COLS = {
        'community': 'community_name',
        'url': 'url',
        'labeller': 'labeller'
    }

    def __init__(self, data: pd.DataFrame = None, cols: dict = DEFAULT_COLS):
        """

        Args:
            data:
            cols:
        """
        # for c in cols.keys():
        #     if c not in data.columns:
        #         raise KeyError(f"Required column {c} not in data")
        self._data = None
        if data is not None:
            self.append(data, cols)

    def append(self, data: pd.DataFrame, cols: dict = DEFAULT_COLS):
        data = self._generate_extra_labels(data)
        data = data.astype(self.labels)
        data = data.rename(columns=cols)
        if self._data is None:
            self._data = data
        elif isinstance(self._data, pd.DataFrame) and isinstance(data, pd.DataFrame):
            self._data = pd.concat([self._data, data])
        else:
            raise Exception("Could not add data, wrong type(s)")

        return self

    @property
    def data(self):
        return self._data

    def data_by_community(self, community_name):
        return self.data[
            self.data['community_name'] == community_name
        ]

    """
    @property
    def _required_cols(self):
        return self._cols.values() + self.labels.keys()
    """

    @property
    def labels(self) -> dict:
        raise NotImplementedError

    @property
    def level(self) -> CommunityDataLevel:
        raise NotImplementedError

    @abstractmethod
    def _generate_extra_labels(self, data):
        pass

    def __str__(self):
        return (
            f"{type(self)}\n"
            f"   Level: {self.level.value}\n"
            f"   Labelled entities: {self.data.shape[0]}\n"
            f"   Labels (cols): {len(self.labels.values())}\n"
            f"   Labellers: {len(self.data['labeller'].unique())}\n"
            f"   Communities: {len(self.data['community_name'].unique())}\n"
        )


class LabelCollection:
    """
    TODO: add documentation
    """

    def __init__(self, labels=[]):
        self._labels = labels

    @property
    def labels(self):
        return self._labels

    def by_level(self, level):
        data = [l.data for l in self.labels if l.level == level]
        if len(data) == 1:
            return data[0]
        elif len(data) > 1:
            return pd.merge(data)
        else:
            return None

    @property
    def all_label_names(self):
        return [k for l in self.labels for k in l.labels.keys()]

    def add(self, labels: Labels):
        ln = set(self.all_label_names)
        new_ln = set(labels.labels.keys())
        duplicates = set.intersection(ln, new_ln)
        if len(duplicates) > 0:
            raise Exception(f"Could not add labels, labels {duplicates} already exist!")
        else:
            self._labels.append(labels)

    def append(self, labels: Labels):
        appended = False
        for l in self._labels:
            if type(labels) is type(l) and labels.level == l.level:
                l.append(labels.data)
                appended = True
        if not appended:
            try:
                self.add(labels)
            except:
                raise Exception("Could not append or add labels.")

        return self.labels

    def __str__(self):
        s = ""
        for l in self.labels:
            s += l.__str__()

        return s



class InnovationLabels(Labels):
    """
    TODO: add documentation
    """

    LIMESURVEY_LABELLER = 'userid'
    LIMESURVEY_COMMUNITY = 'community'
    LIMESURVEY_URL = 'thread{}'

    LIMESURVEY_LABEL_COLS = {
        'labelling[t{}_idea]': 'label_idea',
        'labelling[t{}_eval]': 'label_evaluation',
        'labelling[t{}_impl]': 'label_implementation',
        'labelling[t{}_mod]': 'label_modification',
        'labelling[t{}_impro]': 'label_improvement',
        'labelling[t{}_inno]': 'label_potential'
    }

    LIMESURVEY_NUM_THREADS = 5

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

        # TODO: this belongs somewhere else...
        def id_from_url(url:str):
            id = None
            if "openenergymonitor.org" in url:
                id = url.split("/")[-1]
            elif "openstreetmap.org" in url:
                id = url.split("=")[-1]
            elif "davehakkens.nl" in url:
                id = url.split("/")[-1]

            return id

        data["id"] = data["url"].apply(id_from_url)

        return data

    """
    @staticmethod
    def _ls_label_map(thread_number):
        ls_col_map = {}
        for sh, label in InnovationLabels.LIMESURVEY_LABEL_SHORTHANDS.items():
            ls_col = InnovationLabels.LS_LABEL_COL_TEMPLATE.format(thread_number, sh)
            col = InnovationLabels.LABEL_COL_TEMPLATE.format(label)
            ls_col_map[ls_col] = col

        return ls_col_map
    """

    def from_limesurvey(self, limesurvey_results):
        """
        Adds label entries from Limesurvey results format. Limesurvey results can contain multiple
        labelled threads per response. For each thread i and associated url and labels, the data
        must contain one column, e.g.:
        "thread1" (=url), "labelA1", "labelB1", ..., "thread2", "labelA2", "labelB2", ...

        Args:
            limesurvey_results: String (path to file) or Pandas.DataFrame

        Returns:

        """
        df = None
        if isinstance(limesurvey_results, pd.DataFrame):
            df = limesurvey_results
        elif isinstance(limesurvey_results, str):
            filename, ext = os.path.splitext(limesurvey_results)
            if ext == ".csv":
                df = pd.read_csv(filename + ext)
            elif ext == ".xlsx":
                df = pd.read_excel(filename + ext)

        dfs = []
        # split df by thread number, rename cols, then re-concat parts
        for i in range(1, self.LIMESURVEY_NUM_THREADS+1):
            label_cols = {
                k.format(i): v for k, v in self.LIMESURVEY_LABEL_COLS.items()
            }
            id_cols = {
                self.LIMESURVEY_LABELLER: 'labeller',
                self.LIMESURVEY_COMMUNITY: 'community_name',
                self.LIMESURVEY_URL.format(i): 'url'
            }
            df_i = df.rename(columns=label_cols).rename(columns=id_cols)[
                list(label_cols.values()) + list(id_cols.values())
            ]
            dfs.append(df_i)

        data = pd.concat(dfs)

        return self.append(data, cols={c: c for c in id_cols.values()})





