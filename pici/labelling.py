from itertools import combinations

import pandas as pd
import janitor
import numpy as np
from abc import ABC, abstractmethod
from typing import overload
from sklearn.decomposition import FactorAnalysis, PCA
from sklearn.preprocessing import StandardScaler
import sklearn.metrics
import statsmodels.stats.inter_rater
from pandas.api.types import CategoricalDtype
from pici.datatypes import CommunityDataLevel
import os
import plotly.graph_objects as go
import plotly.express as px
from statsmodels.stats import inter_rater
import krippendorff
import simpledorff
import matplotlib.pyplot as plt
import seaborn as sns


class LabelStats:
    """
    This class provides metrics and visualizations to analyze the annotations
    made by the labellers.

    Available metrics are:
        - % agreement ("a_0")
        - Cohen's kappa (two labellers)
        - Fleiss' kappa (multiple labellers)
        - Krippendorff's alpha (multiple labellers, missing data)

    Labellers' annotations can furthermore be evaluated against a subsample of
    "goldstandard" annotations, allowing to associate labellers with a quality-
    score.

    TODO refactor --> move visualizations to visualizations.py ?

    See *Xinshu Zhao, Jun S. Liu & Ke Deng (2013) Assumptions behind Intercoder
    Reliability Indices, Annals of the International Communication Association,
    36:1, 419-480, DOI: 10.1080/23808985.2013.11679142* for a comparison of
    inter-rater agreement metrics.
    """

    def __init__(self, labels):
        self.labels = labels

    def plot_latent_model(self, n_comps=None):
        feature_names = None
        if hasattr(self.labels, 'original_labels'):
            feature_names = self.labels.original_labels
        else:
            feature_names = self.labels.labels

        if n_comps is None:
            n_comps = round(len(feature_names) / 2)

        data = self.labels.data[feature_names].dropna(axis=0)

        X = StandardScaler().fit_transform(
            data.apply(pd.to_numeric).to_numpy().astype(float)
        )

        feat_corr = plt.axes()

        im = feat_corr.imshow(np.corrcoef(X.T), cmap="RdBu_r", vmin=-1, vmax=1)

        feat_corr.set_xticks(range(len(feature_names)))
        feat_corr.set_xticklabels(list(feature_names), rotation=90)
        feat_corr.set_yticks(range(len(feature_names)))
        feat_corr.set_yticklabels(list(feature_names))

        plt.colorbar(im).ax.set_ylabel("$r$", rotation=0)
        feat_corr.set_title("Label correlation matrix")

        methods = [
            ("PCA", PCA()),
            ("Unrotated FA", FactorAnalysis()),
            ("Varimax FA", FactorAnalysis(rotation="varimax")),
        ]
        factor_loadings, axes = plt.subplots(
            ncols=len(methods),
            figsize=(10, 8)
        )

        for ax, (method, fa) in zip(axes, methods):
            fa.set_params(n_components=n_comps)
            fa.fit(X)

            components = fa.components_.T
            # print("\n\n %s :\n" % method)
            # print(components)

            vmax = np.abs(components).max()
            ax.imshow(components, cmap="RdBu_r", vmax=vmax, vmin=-vmax)
            ax.set_yticks(np.arange(len(feature_names)))
            if ax.is_first_col():
                ax.set_yticklabels(feature_names)
            else:
                ax.set_yticklabels([])
            ax.set_title(str(method))
            ax.set_xticks(range(n_comps))
            ax.set_xticklabels([f"Comp. {i}" for i in range(1, n_comps+1)])
        factor_loadings.suptitle("Factors")

        return feat_corr, factor_loadings

    def labellers(self):
        return self.labels.data["labeller"].nunique()

    def unique_cases(self):
        return self.labels.data["url"].nunique()

    def label_counts(self, normalize=False):
        d = self.labels.data[self.labels.labels.keys()]
        if not normalize:
            return d.sum()
        else:
            return d.sum() / d.shape[0]

    def label_counts_by_labeller(self, normalize=False):
        d = self.labels.data[list(self.labels.labels.keys()) + ["labeller"]]
        d = d.groupby(by="labeller")

        if normalize:
            return d.mean()
        else:
            return d.sum()

    def label_correlation(self):
        return self.labels.data[list(self.labels.labels.keys())].corr()

    def plot_label_correlation(self):
        corr = self.label_correlation()
        fig = go.Figure()
        fig.add_trace(
            go.Heatmap(
                x=corr.columns,
                y=corr.index,
                z=np.array(corr),
                text=corr.values,
                texttemplate='%{text:.2f}'
            )
        )
        return fig

    def plot_label_counts_by_labeller(self, normalize=True):
        cts = self.label_counts_by_labeller(normalize)
        fig = go.Figure()
        fig.add_trace(
            go.Heatmap(
                x=cts.columns,
                y=cts.index,
                z=np.array(cts),
                text=cts.values,
                texttemplate='%{text:.2f}'
            )
        )
        return fig

    def plot_interrater_agreement(self, data=None):
        ira = None
        if data is None:
            ira = self.interrater_agreement()
        else:
            ira = data
        cols = list(ira.columns)
        fig = px.bar(
            ira,
            x=ira.index,
            y=cols,
            barmode='group'
        )
        return fig

    def complete_agreement(self):
        """
        Get percentage of cases where all labellers agree (per label).

        Returns:
            agreement: Pandas.DataFrame with 'label', '% perfect agreement',
            '% n'

        """
        agree = {}
        base = {}
        for label_name, label_type in self.labels.labels.items():
            a = self.labels.data.drop_duplicates(subset=['url', 'labeller'],
                                                 keep='last')
            a = a.pivot(index="url", columns="labeller", values=label_name)
            # .dropna()

            if not a.empty:

                a = a.reset_index().drop(columns="url")
                b = a.copy()
                b['unique_value'] = a.nunique(axis=1) == 1
                b['num_labellers'] = a.count(axis=1)
                b['valid'] = b.num_labellers >= 2
                b['all_agree'] = b.unique_value.where(b.valid, np.nan)

                if 'all_agree' in b.columns:
                    n_all = b.all_agree.count()
                    n_agree = b.all_agree.sum()
                    agree[label_name] = n_agree / n_all
                    base[label_name] = n_all # /len(a.index)

        return agree, base

    def cohen_kappa(self):
        """
        Get Cohen's kappa for all labels, using scikit-learn implementation
        [``sklearn.metrics.cohen_kappa_score``](
        https://scikit-learn.org/stable/modules/generated/sklearn.metrics
        .cohen_kappa_score.html).
        Returns NaN if number of labellers != 2.

        Returns:
            dict of (label name, kappa)
        """
        kappas = {}
        for lname, l in self.labels.data_by_label(
                format='sklearn', dropna='cases').items():
            k = np.nan
            if len(l['data']) == 2:
                dat = [arr.astype(float) for arr in l['data']]
                k = sklearn.metrics.cohen_kappa_score(
                    *dat,
                    **{'labels': l['labels']}
                )
            kappas[lname] = k

        return kappas

    def fleiss_kappa(self):
        """
        Get Fleiss kappa for all labels, based on Statsmodels
        implementation (``statsmodels.stats.inter_rater.fleiss_kappa``).
        Returns NaN if number of labellers < 2.

        Returns:
            dict of (label name, kappa)
        """
        kappas = {}
        for lname, l in self.labels.data_by_label(format='statsmodels_fleiss',
                                                  dropna='cases').items():
            if len(l['data'][0]) > 0:
                k = statsmodels.stats.inter_rater.fleiss_kappa(
                    table=l['data'][0],
                    method='fleiss'
                )
            else:
                k = np.nan
            kappas[lname] = k

        return kappas

    def krippendorff_alpha(self):
        """
        Get Krippendorff alphas using the ''krippendorff'' package.

        See also:
        *Andrew F. Hayes & Klaus Krippendorff (2007) Answering the Call for a
        Standard Reliability Measure for Coding Data, Communication Methods
        and Measures, 1:1, 77-89, DOI: 10.1080/19312450709336664*

        Returns:
            Pandas.DataFrame
        """
        alphas = {}
        for lname, l in self.labels.data_by_label(format='sklearn',
                                                  dropna=False).items():
            level_of_measurement = "nominal"
            ltype = self.labels.labels[lname]
            dat = l['data']
            if ltype == 'bool':
                dat = [arr.astype(float) for arr in dat]
            if isinstance(ltype, CategoricalDtype) and ltype.ordered:
                level_of_measurement = "ordinal"
            # TODO: implement interval, ratio label types

            try:
                a = krippendorff.alpha(
                    reliability_data=dat,
                    level_of_measurement=level_of_measurement
                )
            except AssertionError:
                a = np.nan
            alphas[lname] = a

        return alphas

    # def gwet_ac1(self):
        # Do we really need another inter-rater metric?
        """

        See: *Gwet KL. Computing inter-rater reliability and its variance in
        the presence of high agreement. Br J Math Stat Psychol. 2008 May;
        61(Pt 1):29-48. doi: 10.1348/000711006X126600.*

        Returns:

        """
        # TODO: find implementation or pseudo-code

    def interrater_agreement(self):
        """
        Calculated the overall interrater agreement for all labellers in
        data. If number of labellers > 2, all values for Cohen/Fleiss kappa
        will be NaN.

        Returns:
            agreement dataframe
        """
        agree, base = self.complete_agreement()
        c_kappa = self.cohen_kappa()
        f_kappa = self.fleiss_kappa()
        k_alpha = self.krippendorff_alpha()
        df = pd.DataFrame(
            [agree, base, c_kappa, f_kappa, k_alpha],
        ).T
        df.columns = [
            "% complete agreement", "base n", "Cohen kappa", "Fleiss kappa",
            "Krippendorff alpha"
        ]

        return df

    def pairwise_interrater_agreement(self, goldstandard=None,
                                      min_comparisons=1):
        """
        Calculates the agreement metrics for all combinations of two
        labellers. If goldstandard is set (name of labeller),
        only comparisons with the goldstandard are calculated.

        Args:
            goldstandard: Name of labeller
            min_comparisons: Minimum number of shared labelled cases
            required to include labeller-pair in results.

        Returns:
            Agreement dataframe with "labellers" column that contains
            - (labeller A, labeller B) tuples (default), or
            - labeller B strings (if labeller A is set as goldstandard)

        """
        old_filter = self.labels._filter

        df = None
        for l1, l2 in combinations(self.labels.labellers, 2):
            if goldstandard is None or goldstandard in (l1, l2):
                self.labels.set_filter(f"labeller=='{l1}' or labeller=='{l2}'")
                current_df = self.interrater_agreement()
                other = None
                if goldstandard is not None:
                    other = l1 if goldstandard == l2 else l2
                current_df["labellers"] = current_df.apply(
                    lambda x: (l1, l2), 1) if goldstandard is None \
                else current_df.apply(
                    lambda x: other, 1)
                if df is None:
                    df = current_df
                else:
                    df = pd.concat([df, current_df])

        if df is not None:
            df = df[df["base n"] >= min_comparisons]

        self.labels.set_filter(old_filter)

        return df

    def plot_goldstandard_agreement(self,
                                    kind='label_boxplots', goldstandard=None,
                                    data=None):
        """
        Plot the labellers' agreement with goldstandard. Provides different
        plots through ``kind``:
        - label_boxplots: values: each labeller's agreement with
        goldstandard, x: metric, y: boxplot of values
        - labellers_points: values: each labeller's agreement with
        goldstandard, grid, col per metric, x: labels, y: values

        Args:
            kind: One of {'label_boxplots','labellers_points'}
            goldstandard: Name of labeller to use as goldstandard
                (used if data is None, generates data)
            data: agreement dataframe generated by
                ``pairwise_interrater_agreement``

        Returns: Figure

        """
        if data is None:
            agreement = self.pairwise_interrater_agreement(
                goldstandard=goldstandard)
        else:
            agreement = data

        d = self._melt_goldstandard_agreement(agreement)

        g = None

        if kind=='label_boxplots':
            g = sns.catplot(x="variable", y="value", hue="index", data=d,
                            kind="box", aspect=2.5)
            ax1 = g.axes.flatten()[0]
            ax1.axhline(0, ls='--')

        elif kind=='labeller_points':
            g = sns.catplot(x="index", y="value", hue="labellers",
                            col='variable', data=d, kind="point",
                            aspect=0.7)
            for ax in g.axes.flatten():
                ax.axhline(0, ls='--')
        else:
            raise Exception(f"Kind {kind} not recognized")

        return g


    def _melt_goldstandard_agreement(self, data):
        """
        Prepares ``interrater_agreement`` dataframe for plotting (e.g., with
        seaborn): wide format to long format, shorten label names.

        Args:
            data: Pandas.DataFrame with label names as index, "labellers"-
            and metrics-columns.

        Returns:
            Pandas.DataFrame with columns:
                - index: shortened label names
                - labellers: labeller names
                - variable: metric name
                - value: metric value
        """
        if "base n" in data.columns:
            agr = data.drop("base n", axis=1)
        else:
            agr = data
        ix = ["index", "labellers"]
        vv = [c for c in agr.columns if c not in ix]
        agr = agr.reset_index().melt(id_vars=ix, value_vars=vv)
        agr['index'] = agr['index'].map(lambda x: x.split("_")[1][:4])

        return agr



class Labels(ABC):
    """
    TODO: add documentation
    """

    DEFAULT_COLS = {
        'community': 'community_name',
        'url': 'url',
        'labeller': 'labeller'
    }

    def __init__(self, data: pd.DataFrame = None, cols: dict = DEFAULT_COLS,
                 filter = None):
        """

        Args:
            data:
            cols:
        """
        # for c in cols.keys():
        #     if c not in data.columns:
        #         raise KeyError(f"Required column {c} not in data")
        self._data = None
        self._filter = filter
        if data is not None:
            self.append(data, cols)
        self.stats = LabelStats(self)

    def append(self, data: pd.DataFrame, cols: dict = DEFAULT_COLS,
               drop_labellers=None):
        """
        TODO: add documentation

        Args:
            data:
            cols:
            drop_labellers:

        Returns:

        """
        bool_cols = [
            l for l, t in self.labels.items() if
            l in data.columns and t == "bool"
        ]
        # TODO: test if this works --> see if right number of cases are dropped
        data[bool_cols] = data[bool_cols].fillna(0)
        data = data.astype(object)
        data = data.astype({
            l: t for l, t in self.labels.items() if l in data.columns
        })
        data = self._generate_extra_labels(data)
        data = data.astype(self.labels)
        data = data.rename(columns=cols)
        if drop_labellers is not None:
            data = data[~data["labeller"].isin(drop_labellers)]
        if self._data is None:
            self._data = data
        elif isinstance(self._data, pd.DataFrame) and isinstance(data,
                                                                 pd.DataFrame):
            self._data = pd.concat([self._data, data])
        else:
            raise Exception("Could not add data, wrong type(s)")

        return self

    @property
    def data(self):
        if self._filter is None:
            return self._data
        else:
            return self._data.query(self._filter)
        return self._data

    def set_filter(self, f):
        """
        TODO: add documentation

        Args:
            f:

        Returns:

        """
        self._filter = f

    def data_by_label(self, format='sklearn', dropna=False):
        """
        TODO: add documentation

        Args:
            dropna:

        Returns:

        """
        d = {}
        for lname, ltype in self.labels.items():
            lvalues = None
            if ltype == 'bool':
                lvalues = [True, False]
            elif isinstance(ltype, CategoricalDtype):
                lvalues = ltype.categories

            dat = self.data.drop_duplicates(subset=["url","labeller"])
            ld = dat.pivot(index='url', columns='labeller', values=lname)
            # ld:
            #         | labeller A | labeller B |  ...
            #   ______|____________|____________|_________
            #   url 1 |            |            |           --- axis 1 --->
            #   url 2 |            |            |
            #   url 3 |            |            |
            #     ... |            |            |
            #                |
            #                |
            #             axis 0
            #                |
            #                ↓
            #
            if dropna == 'labellers':
                # dropna(axis=0): drop columns that contain NaN
                ld = ld.dropna(axis=1)
            elif dropna == 'cases':
                # dropna(axis=0): drop rows that contain NaN
                ld = ld.dropna(axis=0)

            np_data = []
            if format == 'sklearn':
                np_data = [ld[c].to_numpy() for c in ld.columns]
            elif format == 'statsmodels_fleiss':
                np_data = statsmodels.stats.inter_rater.aggregate_raters(
                    data=ld.to_numpy()
                )

            d[lname] = {
                'data': np_data,
                'labels': lvalues
            }

        return d

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
    def labellers(self) -> list:
        """
        TODO: add documentation

        Returns:

        """
        if isinstance(self.data, pd.DataFrame):
            return list(self.data['labeller'].unique())
        else:
            return []

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

    def rating_table(self, label_name, communities=None, custom_filter=None,
                     allow_missing_data=False):
        """
        Get the rating table for one label to be used, e.g.,
        with ``statsmodels.stats.inter_rater``.

        Args:
            communities: List of communities to include in table,
            if ``None``, include all communities
            label_name: label to be returned in table
            allow_missing_data: whether to drop columns with missing ratings

        Returns:
            rating table: labels as 2-dim table with raters (labellers) in
            rows and ratings in columns.
        """
        d = self.data
        if communities is not None:
            d = self.data[self.data['community_name'].isin(communities)]
        if custom_filter is not None:
            d = self.data[custom_filter]


class LabelCollection:
    """
    TODO: add documentation
    """

    def __init__(self, labels=[]):
        self._labels = []
        for l in labels:
            self.append(l)

    @property
    def labels(self):
        """
        TODO: add documentation

        Returns:

        """
        return self._labels

    def by_level(self, level):
        """
        TODO: Add documentation

        Args:
            level:

        Returns:

        """
        data = [l.data for l in self.labels if l.level == level]
        if len(data) == 1:
            return data[0]
        elif len(data) > 1:
            return pd.merge(data)
        else:
            return None

    @property
    def all_label_names(self):
        """
        TODO: add documentation

        Returns:

        """
        return [k for l in self.labels for k in l.labels.keys()]

    def add(self, labels: Labels):
        ln = set(self.all_label_names)
        new_ln = set(labels.labels.keys())
        duplicates = set.intersection(ln, new_ln)
        if len(duplicates) > 0:
            raise Exception(
                f"Could not add labels, labels {duplicates} already exist!")
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

    original_labels = [
        'label_idea','label_evaluation','label_implementation',
        'label_modification', 'label_improvement', 'label_potential'
    ]

    level = CommunityDataLevel.TOPICS

    def _generate_extra_labels(self, data):
        try:
            act_labels = [
                'label_idea', 'label_evaluation', 'label_implementation',
                'label_modification', 'label_improvement'
            ]

            # TODO: this should already be done in abstract class...
            data[act_labels] = data[act_labels].fillna(False)

            activities = data[act_labels]
            data["label_any_activity"] = activities.any(axis=1)
            self.labels['label_any_activity'] = 'bool'
        except KeyError:
            pass

        try:
            data["label_has_potential"] = data["label_potential"] > 0
            self.labels["label_has_potential"] = 'bool'
        except KeyError:
            pass

        # TODO: refactoring --> this belongs somewhere else... (communities)
        def id_from_url(url: str):
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

    def from_limesurvey(self, limesurvey_results, drop_labellers=None):
        """
        Adds label entries from Limesurvey results format. Limesurvey
        results can contain multiple
        labelled threads per response. For each thread i and associated url
        and labels, the data
        must contain one column, e.g.:
        "thread1" (=url), "labelA1", "labelB1", ..., "thread2", "labelA2",
        "labelB2", ...

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
        for i in range(1, self.LIMESURVEY_NUM_THREADS + 1):
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

        return self.append(
            data,
            cols={c: c for c in id_cols.values()},
            drop_labellers=drop_labellers
        )
