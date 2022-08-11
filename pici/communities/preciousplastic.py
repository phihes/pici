from pici.helpers import create_co_contributor_graph, create_commenter_graph
import pandas as pd
import scrapy
from scrapyscript import Job, Processor
import logging
import numpy as np
import json
from urllib.parse import urlparse
from pici.community import Community, CommunityFactory


class PPCommunity(Community):
    name = "PreciousPlastic"
    date_column = "date"
    contributor_column = "author"
    topic_column = "topic"
    text_column = "text"

    DEFAULT_ATTRIBUTES = {
        "yesterday": "2021-07-11",
        "today": "2021-07-12",
        "node_data": [
            'age',
            'badges',
            'topics',
            'dedication',
            'name'
        ],
        "original_date_column": "date"
    }

    def _set_data(self, data, start, end):

        d = {}

        if 'posts' in data.keys():
            if isinstance(data['posts'], pd.DataFrame):

                p = data['posts']

                # prepare date column in post data
                p["date"] = pd.to_datetime(
                    p[self._attr["original_date_column"]]
                )

                # set time slice
                d['posts'] = self.timeslice(p, self.date_column, start, end)

            else:
                raise TypeError("posts are not a pandas dataframe")
        else:
            raise ValueError("posts are missing in data")

        if 'users' in data.keys():
            if isinstance(data['users'], pd.DataFrame):
                c = data["users"].rename(columns={"id": self.contributor_column})

                relevant_users = d["posts"][self.contributor_column]
                d["contributors"] = c[c[self.contributor_column].isin(relevant_users.tolist())].set_index(
                    self.contributor_column)
            else:
                raise TypeError("users are not a pandas dataframe")
        else:
            raise ValueError("users are missing in data")

        if 'topics' in data.keys():
            if isinstance(data['topics'], pd.DataFrame):

                tp = data["topics"].drop_duplicates(subset=['id']).rename(
                    columns={"id": self.topic_column}).drop(['Unnamed: 0'], axis=1)

                relevant_topics = d["posts"][self.topic_column]
                d["topics"] = tp[tp[self.topic_column].isin(relevant_topics.tolist())].set_index(self.topic_column)

            else:
                raise TypeError("posts are not a pandas dataframe")
        else:
            raise ValueError("posts are missing in data")

        self._data = d
        self._posts = d['posts']
        self._contributors = d['contributors']
        self._topics = d['topics']

    def _generate_co_contributor_graph(self):
        return create_co_contributor_graph(
            self.posts,
            self.contributors,
            self.contributor_column,
            self.topic_column,
            self.contributors.columns
        )

    def _generate_commenter_graph(self):
        return create_commenter_graph(
            self.posts,
            self.contributors,
            self.contributor_column,
            self.topic_column,
            self.contributors.columns
        )


class PPCommunityFactory(CommunityFactory):
    name = "pp"
    cache_data = ['posts', 'users', 'topics']

    def _create_community(self, name, start, end):
        try:
            self._data
        except:
            raise Exception("No community data found, can not set up community.")

        return PPCommunity(name, self._data, start, end)

    def scrape_data(self):
        raise NotImplementedError
