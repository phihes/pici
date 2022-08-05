import numpy as np
import pandas as pd
from sklearn.base import BaseEstimator, TransformerMixin
from sklearn.pipeline import Pipeline, FeatureUnion
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import FunctionTransformer
from collections import ChainMap

from pici.datatypes import CommunityDataLevel


class CommunitySetter(BaseEstimator, TransformerMixin):
    def __init__(self, community_name):
        self.community_name = community_name

    def fit(self, x, y=None):
        return self

    def transform(self, df):
        return df.assign(community_name=self.community_name).set_index([
            "community_name"], append=True)


class ItemSelector(BaseEstimator, TransformerMixin):
    def __init__(self, key):
        self.key = key

    def fit(self, x, y=None):
        return self

    def transform(self, data_dict):
        return data_dict[self.key]


class Pipelines:

    def __init__(self, pici):
        self._pici = pici

    def topics(self):
        level = CommunityDataLevel.TOPICS
        metrics = self._pici.get_metrics(
            level=level,
            unwrapped=True
        ).values()
        feature_pipeline = self.generate_features_pipeline(
            level=level,
            metrics=metrics
        )
        pipe = self.generate_community_pipeline(
            communities=self._pici.communities,
            feature_pipeline=feature_pipeline
        )

        return pipe

    @staticmethod
    def keep_features(X, view, keep):
        return {
            f: getattr(X, view)[f] for f in keep
        }

    @staticmethod
    def generate_community_pipeline(communities, feature_pipeline):
        community_transformers = [
            (community.name, Pipeline([
                ('selector', ItemSelector(key=community.name)),
                ('features', feature_pipeline),
                ('add_community_name',
                 CommunitySetter(community_name=community.name)),
                ('package', FunctionTransformer(
                    lambda df: {'features': df}
                ))
            ]))
            for community in communities.values()
        ]

        pipe = Pipeline([
            ('community_features',
             FeatureUnion(transformer_list=community_transformers)),
            ('stack_communities', FunctionTransformer(lambda arr: pd.concat(
                [res['features'] for res in arr.tolist()],
                axis=0
            ))),
        ])

        return pipe

    @staticmethod
    def generate_features_pipeline(
            level: CommunityDataLevel,
            metrics: list = None,
            keep: list = [],
            metric_params: dict = {},
            pipe_params: dict = {}
    ):
        feature_transformers = [
            (f.__name__, FunctionTransformer(f)) for f in metrics
        ]
        pipe = Pipeline([
            (f'{level.value}_features', FeatureUnion(
                feature_transformers + [
                    ('keep_features', FunctionTransformer(
                        Pipelines.keep_features))
                ]
            )),
            ('feature_rows_to_df', FunctionTransformer(
                lambda feats: pd.DataFrame(dict(ChainMap(*feats))))),
        ])

        # TODO: set params for each community, in the right place...
        """
        pipe.set_params(**dict(ChainMap(
            {
                f'{level.value}_features__keep_features__kw_args': {
                    'view': level.value,
                    'keep': keep
                }
            },
            {
                f'{level.value}_features__{m_name}__kw_args': m_params
                for m_name, m_params in metric_params.items()
            },
            pipe_params
        )))
        """

        return pipe

"""
https://stackoverflow.com/questions/43366561/use-sklearns-gridsearchcv-with-a-pipeline-preprocessing-just-once

clf = make_pipeline(StandardScaler(), 
                    GridSearchCV(LogisticRegression(),
                                 param_grid={'logisticregression__C': [0.1, 10.]},
                                 cv=2,
                                 refit=True))

clf.fit()
clf.predict()

More relevant stuff:
https://stackoverflow.com/questions/55609339/how-to-perform-feature-selection-with-gridsearchcv-in-sklearn-in-python
"""
